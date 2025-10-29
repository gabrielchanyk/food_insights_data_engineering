from airflow import DAG
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

# First 3 DAG triggers
mealdash_task = TriggerDagRunOperator(
    task_id='mealdash_ingest_clean_dag',
    trigger_dag_id='mealdash_ingest_clean_dag',
    conf={
        'steps_yaml_path': steps_yaml_path,
        's3_staging_dir': 's3://my-athena-query-results/staging/',
        'athena_database': 'analytics_db',
        'workgroup': 'primary'
    },
    wait_for_completion=True,
    dag=dag,
)

quickbite_task = TriggerDagRunOperator(
    task_id='quickbite_ingest_clean_dag',
    trigger_dag_id='quickbite_ingest_clean_dag',
    conf={
        'steps_yaml_path': steps_yaml_path,
        's3_staging_dir': 's3://my-athena-query-results/staging/',
        'athena_database': 'analytics_db',
        'workgroup': 'primary'
    },
    wait_for_completion=True,
    dag=dag,
)

foodnow_task = TriggerDagRunOperator(
    task_id='foodnow_ingest_clean_dag',
    trigger_dag_id='foodnow_ingest_clean_dag',
    conf={
        'steps_yaml_path': steps_yaml_path,
        's3_staging_dir': 's3://my-athena-query-results/staging/',
        'athena_database': 'analytics_db',
        'workgroup': 'primary'
    },
    wait_for_completion=True,
    dag=dag,
)

# Final Athena steps DAG trigger
gold_transform = TriggerDagRunOperator(
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

# Set dependencies: first 3 in parallel, then final DAG
[mealdash_task, quickbite_task, foodnow_task] >> gold_transform