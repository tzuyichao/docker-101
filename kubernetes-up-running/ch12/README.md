## One shot


```
kubectl run -i oneshot --image=gcr.io/kuar-demo/kuard-amd64:1 --restart=OnFailure -- --keygen-enable --keygen-exit-on-complete --keygen-num-to-gen 10
```

書上例子打錯image，會看到pod status "CrashLoopBackOff"，此時可用kubectl describe pod oneshot看一下訊息。
