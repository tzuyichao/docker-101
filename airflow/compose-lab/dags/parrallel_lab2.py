from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def child_task(task_id, **kwargs):
    print(f"Running child task with task ID: {task_id}")

dag = DAG(
    'dummy_parallel_dag_example',
    start_date=datetime(2023, 6, 24),
    schedule_interval=None
)

dummy_task = DummyOperator(
    task_id='dummy_task',
    dag=dag
)

parallel_tasks = []
for i in range(5):
    task_id = f'child_task_{i+1}'
    parallel_task = PythonOperator(
        task_id=task_id,
        python_callable=child_task,
        op_kwargs={'task_id': task_id},
        dag=dag
    )
    parallel_tasks.append(parallel_task)

dummy_task >> parallel_tasks
