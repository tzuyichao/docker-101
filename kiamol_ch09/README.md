# Memo

```
PS C:\GitHub\docker-101\kiamol_ch09> kubectl get rs -l app=vweb -o=custom-columns=NAME:.metadata.name,REPLICA:.status.replicas,REVISION:.metadata.annotations.deployment\.kubernetes\.io/revision
NAME              REPLICA   REVISION
vweb-69545f4684   0         1
vweb-85fc7c6cf5   3         3
vweb-c6957bcd9    0         2
```


```
PS C:\GitHub\docker-101\kiamol_ch09> kubectl get svc vweb -o jsonpath='http://{.status.loadBalancer.ingress[0].*}:8090/v.txt' > v.txt

PS C:\GitHub\docker-101\kiamol_ch09> curl $(cat v.txt)


StatusCode        : 200
StatusDescription : OK
Content           : v2
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Accept-Ranges: bytes
                    Content-Length: 2
                    Content-Type: text/plain
                    Date: Fri, 21 Jan 2022 08:54:31 GMT
                    ETag: "61e3df49-2"
                    Last-Modified: Sun, 16 Jan 2022 09:...
Forms             : {}
Headers           : {[Connection, keep-alive], [Accept-Ranges, bytes], [Content-Length, 2], [Content-Type,
                    text/plain]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 2

```
