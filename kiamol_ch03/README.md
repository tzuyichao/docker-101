# Memo

## describe pod via selector

```
kubectl describe pod -l app=sleep-1
```

## execute ping to other pod

### name

```
kubectl exec deploy/sleep-1 -- ping -c 2 $(kubectl get pods -l app=sleep-2 -o jsonpath='{.items[0].metadata.name}')
```

Result:

```
PS C:\GitHub\docker-101\kiamol_ch03> kubectl exec deploy/sleep-1 -- ping -c 2 $(kubectl get pods -l app=sleep-2 -o jsonpath='{.items[0].metadata.name}')
ping: bad address 'sleep-2-bd8bc78c7-xsckk'
command terminated with exit code 1
```

### Pod IP

```
kubectl exec deploy/sleep-1 -- ping -c 2 $(kubectl get pods -l app=sleep-2 -o jsonpath='{.items[0].status.podIP}')
```

Result:

```
PS C:\GitHub\docker-101\kiamol_ch03> kubectl exec deploy/sleep-1 -- ping -c 2 $(kubectl get pods -l app=sleep-2 -o jsonpath='{.items[0].status.podIP}')
PING 172.17.0.4 (172.17.0.4): 56 data bytes
64 bytes from 172.17.0.4: seq=0 ttl=64 time=0.059 ms
64 bytes from 172.17.0.4: seq=1 ttl=64 time=0.068 ms

--- 172.17.0.4 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.059/0.063/0.068 ms
```
