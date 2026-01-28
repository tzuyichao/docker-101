
```
\d pg_buffercache;
                 View "public.pg_buffercache"
      Column      |   Type   | Collation | Nullable | Default
------------------+----------+-----------+----------+---------
 bufferid         | integer  |           |          |
 relfilenode      | oid      |           |          |
 reltablespace    | oid      |           |          |
 reldatabase      | oid      |           |          |
 relforknumber    | smallint |           |          |
 relblocknumber   | bigint   |           |          |
 isdirty          | boolean  |           |          |
 usagecount       | smallint |           |          |
 pinning_backends | integer  |           |          |
```

```
CREATE FUNCTION buffercache(rel regclass)
RETURNS TABLE(
  bufferid integer, relfork text, relblk bigint,
  isdirty boolean, usagecount smallint, pins integer
) AS $$
SELECT bufferid,
  CASE relforknumber
    WHEN 0 THEN 'main'
    WHEN 1 THEN 'fsm'
    WHEN 2 THEN 'vm'
  END,
  relblocknumber,
  isdirty,
  usagecount,
  pinning_backends
FROM pg_buffercache
WHERE relfilenode = pg_relation_filenode(rel)
ORDER BY relforknumber, relblocknumber;
$$ LANGUAGE sql;
```

```
SELECT * FROM buffercache('cacheme');
 bufferid | relfork | relblk | isdirty | usagecount | pins
----------+---------+--------+---------+------------+------
      575 | main    |      0 | t       |          1 |    0
(1 row)

EXPLAIN (analyze, buffers, costs off, timing off, summary off)
  SELECT * FROM cacheme;
                 QUERY PLAN
---------------------------------------------
 Seq Scan on cacheme (actual rows=1 loops=1)
   Buffers: shared hit=1 dirtied=1
 Planning:
   Buffers: shared hit=3 read=1
   I/O Timings: shared read=0.028
(5 rows)

SELECT * FROM buffercache('cacheme');
 bufferid | relfork | relblk | isdirty | usagecount | pins
----------+---------+--------+---------+------------+------
      575 | main    |      0 | t       |          2 |    0
(1 row)
````