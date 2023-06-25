from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

dag = DAG(
    'dummy_parallel_example',
    start_date=datetime(2023, 6, 24),
    schedule_interval=None
)

dummy_task_1 = DummyOperator(
    task_id='dummy_task_1',
    dag=dag
)

dummy_task_2 = DummyOperator(
    task_id='dummy_task_2',
    dag=dag
)

dummy_parallel_task = DummyOperator(
    task_id='dummy_parallel_task',
    dag=dag
)

dummy_task_1 >> dummy_parallel_task
dummy_task_2 >> dummy_parallel_task
