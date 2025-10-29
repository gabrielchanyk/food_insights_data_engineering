from airflow import DAG
from airflow.providers.amazon.aws.operators.batch import AwsBatchOperator
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
    'main_batch_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

base_path = os.path.dirname(__file__)
steps_yaml_path = os.path.join(base_path, 'maps/steps.yaml')

# AWS Batch job
batch_job = AwsBatchOperator(
    task_id='trigger_batch_job',
    job_name='data_processing_batch_job',
    job_queue='my-batch-queue',       # replace with your Batch job queue name
    job_definition='data_processing_job_def:1',  # replace with your job definition name and revision
    overrides={                        # optional, e.g., environment variables
        'environment': [
            {'name': 'S3_SCRIPT_PATH', 'value': 's3://my-batch-scripts/data_processing.py'},
        ]
    },
    aws_conn_id='aws_default',
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

batch_job >> trigger_athena_dag
