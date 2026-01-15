-- physical replication user (region1 primary -> region1 standby1)
CREATE ROLE repl_r1_phy WITH LOGIN REPLICATION PASSWORD 'repl_r1_phy_pwd';

-- (可選) 你要做 logical publication 的物件也可以一併放這裡
CREATE TABLE IF NOT EXISTS public.items (
  id   int PRIMARY KEY,
  name text NOT NULL
);

CREATE PUBLICATION pub_items FOR TABLE public.items;

-- 給 logical 用戶的權限：這個不要給 repl_r1_phy
-- 你之後要從 region1_standby1 當 publisher 給 region2_primary subscribe
-- 建議另外建 repl_r1_log，並只給它 SELECT
CREATE ROLE repl_r1_log WITH LOGIN REPLICATION PASSWORD 'repl_r1_log_pwd';
GRANT USAGE ON SCHEMA public TO repl_r1_log;
GRANT SELECT ON public.items TO repl_r1_log;
