FROM python:3.10-slim

RUN apt-get update 

RUN mkdir /notebooks

WORKDIR /notebooks

RUN pip install jupyter

EXPOSE 8888

ENV JUPYTER_TOKEN=091d52f275d2193aff3d7c53608f7be0e529028cb12c7c952ac561f4956ec684

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=091d52f275d2193aff3d7c53608f7be0e529028cb12c7c952ac561f4956ec684"]
