# https://github.com/apache/superset/issues/18867
FROM apache/superset
USER root
RUN apt-get update -y && apt-get install -y python3-dev libldap2-dev libsasl2-dev ldap-utils tox lcov valgrind
RUN pip install python-ldap
RUN pip install Flask-ldap
COPY superset_config.py .
RUN  mv ./superset_config.py /app/superset/
USER superset