FROM python:3.10-slim

RUN apt-get update 

RUN mkdir /notebooks

WORKDIR /notebooks

RUN pip install jupyter

EXPOSE 8888

ENV JUPYTER_TOKEN=<YOUR_TOKEN>

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=<YOUR_TOKEN>"]
