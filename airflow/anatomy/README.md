
```
docker run -ti -p 8080:8080 -v E:/lab/docker/docker-101/airflow/anatomy/dags/download_rocket_launches.py:/opt/airflow/dags/download_rocket_launches.py --entrypoint=/bin/bash --name airflow apache/airflow:2.5.3-python3.10 -c "(airflow db init && airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.org); 
airflow webserver & \
airflow scheduler"
```