from airflow import DAG
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.providers.amazon.aws.hooks.glue import AwsGlueCatalogHook
from airflow.operators.python import PythonOperator
from datetime import timedelta
import json
import os

# ----------------------------
# Default DAG arguments
# ----------------------------
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# ----------------------------
# DAG definition
# ----------------------------
dag = DAG(
    'athena_steps_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

# ----------------------------
# JSON loader
# ----------------------------
def load_json_config(file_path):
    if not os.path.exists(file_path):
        LoggingMixin().log.error(f"JSON file not found: {file_path}")
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        LoggingMixin().log.error(f"Error parsing JSON file {file_path}: {e}")
        raise e

# ----------------------------
# Fetch Glue table schema
# ----------------------------
def get_glue_table_schema(database, table_name, aws_conn_id='aws_default'):
    hook = AwsGlueCatalogHook(aws_conn_id=aws_conn_id)
    columns = hook.get_table(database_name=database, table_name=table_name)['StorageDescriptor']['Columns']
    return {col['Name']: col['Type'] for col in columns}

# ----------------------------
# Validate single table against JSON schema
# ----------------------------
def validate_table(destination_table, athena_database, schema_config):
    """
    Validate a single table against the JSON schema.
    Returns True if valid, False if validation fails.
    """
    if destination_table not in schema_config:
        LoggingMixin().log.info(f"No schema defined for table '{destination_table}', skipping validation.")
        return True  # No schema to check against

    expected_fields = schema_config[destination_table]  # List of dicts with name, datatype, required

    try:
        actual_schema = get_glue_table_schema(athena_database, destination_table)
    except Exception as e:
        LoggingMixin().log.error(f"Failed to fetch Glue schema for '{destination_table}': {e}")
        return False

    for field in expected_fields:
        col_name = field['name']
        col_type = field['datatype'].lower()
        required = field.get('required', True)

        if col_name not in actual_schema:
            if required:
                LoggingMixin().log.error(f"Required column '{col_name}' missing in Glue table '{destination_table}'")
                return False
            else:
                LoggingMixin().log.info(f"Optional column '{col_name}' missing in '{destination_table}', skipping.")
                continue

        actual_type = actual_schema[col_name].lower()
        if col_type not in actual_type:
            LoggingMixin().log.error(f"Column '{col_name}' type mismatch in '{destination_table}': expected {col_type}, got {actual_type}")
            return False

    LoggingMixin().log.info(f"Table '{destination_table}' passed JSON schema validation.")
    return True

# ----------------------------
# Create Athena tasks dynamically with per-table JSON validation
# ----------------------------
def create_athena_tasks(**context):
    conf = context.get('dag_run').conf or {}
    steps_yaml_path = conf['steps_yaml_path']
    s3_staging_dir = conf['s3_staging_dir']
    athena_database = conf['athena_database']
    workgroup = conf.get('workgroup', 'primary')
    schema_json_path = conf.get('schema_json')  # JSON schema path

    base_path = os.path.dirname(steps_yaml_path)
    steps_config = load_json_config(steps_yaml_path) if steps_yaml_path.endswith('.json') else load_yaml_config(steps_yaml_path)

    # Load JSON schema
    schema_config = {}
    if schema_json_path:
        try:
            schema_config = load_json_config(schema_json_path)
        except Exception as e:
            LoggingMixin().log.error(f"Skipping schema load due to error: {schema_json_path}")

    step_tasks = {}

    for step, yaml_files in steps_config['steps'].items():
        step_task_list = []

        for yaml_file in yaml_files:
            yaml_file_path = os.path.join(base_path, 'maps', yaml_file)
            try:
                config = load_yaml_config(yaml_file_path)
            except Exception:
                LoggingMixin().log.error(f"Skipping step YAML due to error: {yaml_file_path}")
                continue

            for index, job in enumerate(config.get('jobs', [])):
                destination_table = job['destination_table']

                # Validate table
                if schema_config:
                    valid = validate_table(destination_table, athena_database, schema_config)
                    if not valid:
                        LoggingMixin().log.warning(f"Skipping Athena job for '{destination_table}' due to schema validation failure.")
                        continue

                task_id = f"{step}_{yaml_file.replace('.yaml','')}_task_{index+1}"
                query = job['query']
                output_location = f"{s3_staging_dir}{destination_table}/"

                transform_task = AthenaOperator(
                    task_id=task_id,
                    query=query,
                    database=athena_database,
                    output_location=output_location,
                    workgroup=workgroup,
                    aws_conn_id='aws_default',
                    dag=dag,
                )

                step_task_list.append(transform_task)

        step_tasks[step] = step_task_list

    # ----------------------------
    # Set step dependencies
    # ----------------------------
    step_keys = list(step_tasks.keys())
    for i in range(len(step_keys) - 1):
        current_step = step_keys[i]
        next_step = step_keys[i + 1]
        for current_task in step_tasks[current_step]:
            for next_task in step_tasks[next_step]:
                current_task >> next_task
