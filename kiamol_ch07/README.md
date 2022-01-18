# Ambassadors Pattern Example

numbers

Related Patterns: Sidecard

# shareProcessNamespace

before

```
PS C:\GitHub\docker-101\kiamol_ch07> kubectl exec deploy/sleep -c sleep -- ps
PID   USER     TIME  COMMAND
    1 root      0:00 /bin/sh -c trap : TERM INT; (while true; do sleep 1000; done) & wait
    7 root      0:00 /bin/sh -c trap : TERM INT; (while true; do sleep 1000; done) & wait
   29 root      0:00 sleep 1000
   30 root      0:00 ps
PS C:\GitHub\docker-101\kiamol_ch07> kubectl exec deploy/sleep -c server -- ps
PID   USER     TIME  COMMAND
    1 root      0:00 sh -c while true; do echo -e "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 62\n\n$(cat /data-ro/index.html)" | nc -l -p 8080; done
    8 root      0:00 nc -l -p 8080
   10 root      0:00 ps
```

after

```
PS C:\GitHub\docker-101\kiamol_ch07> kubectl exec deploy/sleep -c sleep -- ps
PID   USER     TIME  COMMAND
    1 65535     0:00 /pause
    7 root      0:00 /bin/sh -c trap : TERM INT; (while true; do sleep 1000; done) & wait
   14 root      0:00 /bin/sh -c trap : TERM INT; (while true; do sleep 1000; done) & wait
   15 root      0:00 sleep 1000
   16 root      0:00 sh -c while true; do echo -e 'HTTP/1.1 200 OK Content-Type: text/plain Content-Length: 7  kiamol'| nc -l -p 8080; done
   23 root      0:00 nc -l -p 8080
   24 root      0:00 ps
PS C:\GitHub\docker-101\kiamol_ch07> kubectl exec deploy/sleep -c server -- ps
PID   USER     TIME  COMMAND
    1 65535     0:00 /pause
    7 root      0:00 /bin/sh -c trap : TERM INT; (while true; do sleep 1000; done) & wait
   14 root      0:00 /bin/sh -c trap : TERM INT; (while true; do sleep 1000; done) & wait
   15 root      0:00 sleep 1000
   16 root      0:00 sh -c while true; do echo -e 'HTTP/1.1 200 OK Content-Type: text/plain Content-Length: 7  kiamol'| nc -l -p 8080; done
   23 root      0:00 nc -l -p 8080
   31 root      0:00 ps
```