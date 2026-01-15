CREATE ROLE repl_r2_phy WITH LOGIN REPLICATION PASSWORD 'repl_r2_phy_pwd';

-- region2 這邊要接收 region1 的 logical replication，所以也要先建表結構
CREATE TABLE IF NOT EXISTS public.items (
  id   int PRIMARY KEY,
  name text NOT NULL
);
