# Memo

'''
PS C:\GitHub\docker-101\kiamol_ch09> kubectl get rs -l app=vweb -o=custom-columns=NAME:.metadata.name,REPLICA:.status.replicas,REVISION:.metadata.annotations.deployment\.kubernetes\.io/revision
NAME              REPLICA   REVISION
vweb-69545f4684   0         1
vweb-85fc7c6cf5   3         3
vweb-c6957bcd9    0         2
'''