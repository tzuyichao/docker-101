# About Chart Museum

## Installation

1. official helm repository 和書上不一樣了
2. 使用Minikube測試的話，安裝chart meseum的時候要執行minikube tunnel

## Upload package


```
Invoke-WebRequest -uri http://localhost:8008/api/charts -Method Post -Infile .\web-ping-0.1.0.tgz
```