FROM python:3.10-slim

RUN apt-get update 

RUN mkdir /notebooks

WORKDIR /notebooks

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=<YOUR_TOKEN>"]
