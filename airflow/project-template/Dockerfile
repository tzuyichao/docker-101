FROM apache/airflow:2.8.1-python3.11

USER root

RUN apt-get update && apt-get install -y gcc libaio1 wget unzip
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linux.zip
RUN unzip instantclient-basic-linux.zip -d /opt/oracle
RUN sh -c "echo /opt/oracle/instantclient_19_3 > /etc/ld.so.conf.d/oracle-instantclient.conf"
RUN ldconfig

RUN mkdir -p /usr/local/airflow && chown -R airflow /usr/local/airflow
RUN chmod -R 775 /usr/local/airflow

USER airflow

RUN touch /usr/local/airflow/airflow.cfg

ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

