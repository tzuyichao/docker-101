from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import pyodbc

# 定義連接資料庫的相關資訊
db_connection_string = "DRIVER={SQL Server Native Client 11.0};SERVER=<server_name>;DATABASE=<database_name>;UID=<username>;PWD=<password>"

# 定義要執行的查詢
query = "SELECT COUNT(*) AS total_rows FROM tableA"

# 定義每個平行任務要處理的筆數
total_splits = 10

# 定義處理每個分段的任務
def process_data(start_row, num_rows):
    # 建立資料庫連線
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()

    # 執行分段查詢
    offset_query = f"SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY <your_column>) AS RowNum, * FROM tableA) AS subquery WHERE RowNum > {start_row} AND RowNum <= {start_row + num_rows}"
    cursor.execute(offset_query)
    rows = cursor.fetchall()

    # 關閉資料庫連線
    cursor.close()
    conn.close()

    # 將結果寫入 tableB
    # ...

# 定義 DAG
dag = DAG(
    'split_and_process_data',
    start_date=datetime(2023, 6, 24),
    schedule_interval=None
)

# 查詢資料筆數任務
def get_row_count():
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    row_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return row_count

# 建立查詢任務
get_row_count_task = PythonOperator(
    task_id='get_row_count',
    python_callable=get_row_count,
    dag=dag
)

# 建立平行任務
split_and_process_tasks = []
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

# 建立 DummyOperator 以作為任務間的依賴關係
dummy_task = DummyOperator(task_id='dummy_task', dag=dag)

# 設定任務間的依賴關係
get_row_count_task >> dummy_task >> split_and_process_tasks
