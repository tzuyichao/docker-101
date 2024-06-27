
```
docker build . -t lab
```


```
docker run --rm -p 8888:8888 -e JUPYTER_TOKEN=your_token_value -v e:\lab\docker\docker-101\python\jupyter\notebooks:/notebooks lab
```