# Resource

## nodes allocatable

get cpu

```
PS C:\GitHub\docker-101\kiamol_ch12> kubectl get nodes -o jsonpath='{.items[].status.allocatable.cpu}'
8

```

get cpu, memory and pods

```
PS C:\GitHub\docker-101\kiamol_ch12> kubectl get nodes -o jsonpath='{range .items[*]}{@.status.allocatable.cpu} {@.status.allocatable.memory} {@.status.allocatable.pods}{end}'
8 16230900Ki 110
```