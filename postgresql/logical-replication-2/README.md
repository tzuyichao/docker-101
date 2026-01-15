# 目的

兩個primary-standby之間建立logical replication確認功能符合預期。

## 步驟

1. 啟動兩組primary-stanby的replicaion postgreSQL db

```
docker compose up -d
```

2. 在 region2_primary 建 subscription（publisher 指向 region1_standby1）

```
docker exec -it pg_region2_primary psql -U postgres -d appdb -c "CREATE SUBSCRIPTION sub_from_r1 CONNECTION 'host=region1_standby1 port=5432 dbname=appdb user=repl_r1_log password=repl_r1_log_pwd' PUBLICATION pub_items WITH (copy_data = true);"
```

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-2> docker exec -it pg_region2_primary psql -U postgres -d appdb -c "CREATE SUBSCRIPTION sub_from_r1 CONNECTION 'host=region1_standby1 port=5432 dbname=appdb user=repl_r1_log password=repl_r1_log_pwd' PUBLICATION pub_items WITH (copy_data = true);"
NOTICE:  created replication slot "sub_from_r1" on publisher
CREATE SUBSCRIPTION

```

3. 驗證

3.1. region1 primary寫入一筆，region2 standby查詢

```
docker exec -it pg_region2_primary psql -U postgres -d appdb -c "INSERT INTO public.items(id,name) VALUES (100,'r2-hello') ON CONFLICT (id) DO NOTHING;"
```

```
docker exec -it pg_region2_standby1 psql -U postgres -d appdb -c "SELECT * FROM public.items ORDER BY id;"
```

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-2> docker exec -it pg_region2_primary psql -U postgres -d appdb -c "INSERT INTO public.items(id,name) VALUES (100,'r2-hello') ON CONFLICT (id) DO NOTHING;"
INSERT 0 1

What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug pg_region2_primary
    Learn more at https://docs.docker.com/go/debug-cli/
PS E:\lab\docker\docker-101\postgresql\logical-replication-2> docker exec -it pg_region2_standby1 psql -U postgres -d appdb -c "SELECT * FROM public.items ORDER BY id;"
 id  |   name
-----+----------
 100 | r2-hello
(1 row)
```

3.2. 查詢狀態

查詢standby狀態

```sql
docker exec -it pg_region1_primary psql -U postgres -d appdb -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"

docker exec -it pg_region2_primary psql -U postgres -d appdb -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"
```

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-2> docker exec -it pg_region1_primary psql -U postgres -d appdb -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"
 client_addr |   state   | sync_state
-------------+-----------+------------
 172.22.0.4  | streaming | async
(1 row)

PS E:\lab\docker\docker-101\postgresql\logical-replication-2> docker exec -it pg_region2_primary psql -U postgres -d appdb -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"
 client_addr |   state   | sync_state
-------------+-----------+------------
 172.22.0.5  | streaming | async
(1 row)
```

在 subscriber（region2_primary）看 subscription worker：

```sql
docker exec -it pg_region2_primary psql -U postgres -d appdb -c "SELECT * FROM pg_stat_subscription;"
```

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-2> docker exec -it pg_region2_primary psql -U postgres -d appdb -c "SELECT * FROM pg_stat_subscription;"
 subid |   subname   | pid | leader_pid | relid | received_lsn |      last_msg_send_time       |     last_msg_receipt_time     | latest_end_lsn |        latest_end_time
-------+-------------+-----+------------+-------+--------------+-------------------------------+-------------------------------+----------------+-------------------------------
 16397 | sub_from_r1 |  98 |            |       | 0/3047670    | 2026-01-15 10:54:46.550556+00 | 2026-01-15 10:54:46.550952+00 | 0/3047670      | 2026-01-15 10:54:46.550556+00
(1 row)
```

## 後續

### 現在說的HA

原生PostgreSQL primary/standby replication使用上會有一些不便。(不是那麼像現在人聽到HA想到的東西，而且官方文件就在HA章節)


* failover切換人工介入
* remastering之後client也要改設定連另一台

改連線資訊的問題可以在前面加一個連線處理層解決()，standby remaster不須重啟服務。
人工介入的問題目前有open source project協助。比如Patroni之類的。Patroni的做法也會有2n+1的需求和調整作法。

### logical replication

logical replication跟HA章節同級，不是歸到HA裡面。讓我們可以選定資料庫選定table清單進行CDC抄寫的目的。

* logical replication不會複寫DDL，新的table要先在region2建立好。
* 加入新表到原本publication不會做initial copy。