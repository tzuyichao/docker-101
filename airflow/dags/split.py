from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import pymssql

db_connection_string = {
    'host': 'HOST',
    'database': 'DB',
    'user': 'ACC',
    'password': 'PWD'
}

query = "SELECT COUNT(*) AS total_rows FROM dbo.HQ_MARA"

total_splits = 10

def process_data(start_row, num_rows):
    conn = pymssql.connect(**db_connection_string)
    cursor = conn.cursor()

    print(f"start_row: {start_row}, num_rows: {num_rows}")
    while num_rows > 0:
        batch_size = min(2000, num_rows)
        offset_query = f"SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY MANDT, MATNR) AS RowNum, * FROM dbo.HQ_MARA) AS subquery WHERE RowNum > {start_row} AND RowNum <= {start_row + batch_size}"
        cursor.execute(offset_query)
        rows = cursor.fetchall()
        num_rows -= batch_size
        start_row += batch_size
        print(f"remaining rows: {num_rows}")

    cursor.close()
    conn.close()

dag = DAG(
    'split_and_process_data',
    start_date=datetime(2023, 6, 24),
    schedule_interval=None
)

def get_row_count():
    conn = pymssql.connect(**db_connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    row_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return row_count


get_row_count_task = PythonOperator(
    task_id='get_row_count',
    python_callable=get_row_count,
    dag=dag
)


split_and_process_tasks = []
dummy_task = DummyOperator(task_id='dummy_task', dag=dag)
get_row_count_task >> dummy_task
row_count = get_row_count()
for i in range(total_splits):
    start_row = int(i * row_count / total_splits)
    num_rows = int(row_count / total_splits)
    split_and_process_task = PythonOperator(
        task_id=f'split_and_process_{i+1}',
        python_callable=process_data,
        op_kwargs={'start_row': start_row, 'num_rows': num_rows},
        dag=dag
    )
    split_and_process_tasks.append(split_and_process_task)

get_row_count_task >> dummy_task >> split_and_process_tasks
