## Lab1: publish_via_partition_root=false

### Create publication with publish_via_partition_root=false

```
docker exec -it pg_pub psql -U postgres -d lab -c "CREATE PUBLICATION pub_orders FOR TABLE public.orders"
```

### Create subscription

```
docker exec -it pg_sub psql -U postgres -d lab -c "CREATE SUBSCRIPTION sub_orders CONNECTION 'host=pg_pub port=5432 dbname=lab user=repl password=replpass' PUBLICATION pub_orders;"
```

Result

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-3> docker exec -it pg_sub psql -U postgres -d lab -c "CREATE SUBSCRIPTION sub_orders CONNECTION 'host=pg_pub port=5432 dbname=lab user=repl password=replpass' PUBLICATION pub_orders;"
Password for user postgres:
ERROR:  relation "public.orders_202602" does not exist
```

### Create publication with publish_via_partition_root=false

```
docker exec -it pg_pub psql -U postgres -d lab -c "DROP PUBLICATION IF EXISTS pub_orders;"

docker exec -it pg_pub psql -U postgres -d lab -c "CREATE PUBLICATION pub_orders FOR TABLE public.orders WITH (publish_via_partition_root = true);"
```

### Create subscription

```
docker exec -it pg_sub psql -U postgres -d lab -c "CREATE SUBSCRIPTION sub_orders CONNECTION 'host=pg_pub port=5432 dbname=lab user=repl password=replpass' PUBLICATION pub_orders;"
```

Result

```
PS E:\lab\docker\docker-101\postgresql\logical-replication-3> docker exec -it pg_sub psql -U postgres -d lab -c "CREATE SUBSCRIPTION sub_orders CONNECTION 'host=pg_pub port=5432 dbname=lab user=repl password=replpass' PUBLICATION pub_orders;"
Password for user postgres:
NOTICE:  created replication slot "sub_orders" on publisher
CREATE SUBSCRIPTION
```

### 新增一筆資料在subscription沒有的child partition

```
docker exec -it pg_pub psql -U postgres -d lab -c "INSERT INTO public.orders(order_time, customer, amount) VALUES ('2026-02-10 09:00:00+00', 'GAMMA', 70.00);"
```

```
docker exec -it pg_sub psql -U postgres -d lab -c "SELECT * FROM public.orders;"

docker exec -it pg_sub psql -U postgres -d lab -c "SELECT subname, pid, received_lsn, latest_end_lsn, last_msg_receipt_time, latest_end_time FROM pg_stat_subscription;"


```

```sql
SELECT pid, application_name, state, wait_event_type, wait_event, query
FROM pg_stat_activity
WHERE backend_type LIKE '%logical replication%'
   OR application_name LIKE 'logical replication%';
```

```
 @ ERROR:  no partition of relation "orders" found for row
```

```
lab=# select * from public.orders;
 id | order_time | customer | amount
----+------------+----------+--------
(0 rows)

lab=# CREATE TABLE public.orders_202602
  PARTITION OF public.orders
  FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE
lab=# select * from public.orders;
 id | order_time | customer | amount
----+------------+----------+--------
(0 rows)

lab=# select * from public.orders;
 id | order_time | customer | amount
----+------------+----------+--------
(0 rows)

lab=# select * from public.orders;
 id |       order_time       | customer | amount
----+------------------------+----------+--------
  1 | 2026-02-10 09:00:00+00 | GAMMA    |  70.00
(1 row)
```