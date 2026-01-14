## 驗證standby

```
docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT pg_is_in_recovery();"
```

```
 pg_is_in_recovery
-------------------
 t
(1 row)
```

## 驗證primary replication

```
docker exec -it pg_primary psql -U postgres -d appdb -c "SELECT client_addr, state FROM pg_stat_replication;"
```

```
 client_addr |   state
-------------+-----------
 172.22.0.4  | streaming
(1 row)
```

## 驗證CREATE PUBLICATION會出現在standby

primary create publication

```
docker exec -it pg_primary psql -U postgres -d appdb -c "CREATE PUBLICATION pub_items FOR TABLE public.items;"
```

standby確認

```
docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT pubname FROM pg_publication;"
```

```
  pubname
-----------
 pub_items
(1 row)
```

## 驗證 standby 不能建立 logical replication slot

```
docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT pg_create_logical_replication_slot('s1','pgoutput');"
```

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-slot-1> docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT version();"
                                                       version
----------------------------------------------------------------------------------------------------------------------
 PostgreSQL 16.11 (Debian 16.11-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
(1 row)


What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug pg_standby
    Learn more at https://docs.docker.com/go/debug-cli/
PS E:\lab\docker\docker-101\postgresql\logical-replication-slot-1> docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT pg_is_in_recovery();"
 pg_is_in_recovery
-------------------
 t
(1 row)


What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug pg_standby
    Learn more at https://docs.docker.com/go/debug-cli/
PS E:\lab\docker\docker-101\postgresql\logical-replication-slot-1> docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT slot_name, slot_type, plugin, database, active FROM pg_replication_slots;"
 slot_name | slot_type |  plugin  | database | active
-----------+-----------+----------+----------+--------
 s1        | logical   | pgoutput | appdb    | f
(1 row)
```

PostgreSQL 16.11有支援在standby建立logic replication slot，換句話說可以繼續嘗試建立subscription到standby db。

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-slot-1> docker exec -it pg_primary psql -U postgres -d appdb -c "SELECT slot_name, slot_type FROM pg_replication_slots WHERE slot_name='s1';"
 slot_name | slot_type
-----------+-----------
(0 rows)
```

### 看decode

primary 做一筆寫入（產 WAL）

```
docker exec -it pg_primary psql -U postgres -d appdb -c "INSERT INTO public.items VALUES (1001, 'from-primary');"
```

standby

```
docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT pg_create_logical_replication_slot('s_txt', 'test_decoding');"
```

primary 再寫一筆：

```
docker exec -it pg_primary psql -U postgres -d appdb -c "INSERT INTO public.items VALUES (1002, 'decode-me');"
```

standby 讀 changes：

```
docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT * FROM pg_logical_slot_get_changes('s_txt', NULL, NULL);"
```

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-slot-1> docker exec -it pg_standby psql -U postgres -d appdb -c "SELECT * FROM pg_logical_slot_get_changes('s_txt', NULL, NULL);"
    lsn    | xid |                                data
-----------+-----+--------------------------------------------------------------------
 0/3047980 | 750 | BEGIN 750
 0/3047980 | 750 | table public.items: INSERT: id[integer]:1002 val[text]:'decode-me'
 0/3047B70 | 750 | COMMIT 750
(3 rows)
```

## 驗證「standby 可以 decoding」不等於「standby 可以當 publisher 給 CREATE SUBSCRIPTION」

### 對standby 建 subscription

```
docker exec -it pg_subscriber psql -U postgres -c "CREATE DATABASE appdb;"
```

```
docker exec -it pg_subscriber psql -U postgres -d appdb -c "CREATE TABLE public.items (id  int primary key,
  val text);"
```

```
docker exec -it pg_subscriber psql -U postgres -d appdb -c "CREATE SUBSCRIPTION sub_to_standby CONNECTION 'host=standby port=5432 dbname=appdb user=repl password=replpw' PUBLICATION pub_items;"
```

結果可以建

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-slot-1> docker exec -it pg_subscriber psql -U postgres -d appdb -c "CREATE SUBSCRIPTION sub_to_standby CONNECTION 'host=standby port=5432 dbname=appdb user=repl password=replpw' PUBLICATION pub_items;"

NOTICE:  created replication slot "sub_to_standby" on publisher
CREATE SUBSCRIPTION
```