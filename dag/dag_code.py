from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'main_glue_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

base_path = os.path.dirname(__file__)
steps_yaml_path = os.path.join(base_path, 'maps/steps.yaml')

# Glue job
glue_job = AwsGlueJobOperator(
    task_id='trigger_glue_job',
    job_name='data_processing_glue_job',
    script_location='s3://my-glue-scripts/data_processing.py',
    region_name='us-east-1',
    iam_role_name='AWSGlueServiceRole',
    wait_for_completion=True,
    dag=dag,
)

# Trigger Athena DAG
trigger_athena_dag = TriggerDagRunOperator(
    task_id='trigger_athena_steps_dag',
    trigger_dag_id='athena_steps_dag',
    conf={
        'steps_yaml_path': steps_yaml_path,
        's3_staging_dir': 's3://my-athena-query-results/staging/',
        'athena_database': 'analytics_db',
        'workgroup': 'primary'
    },
    wait_for_completion=True,
    dag=dag,
)

glue_job >> trigger_athena_dag
