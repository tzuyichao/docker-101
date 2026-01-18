CREATE DATABASE lab;

\c lab

DROP TABLE IF EXISTS public.orders CASCADE;

CREATE TABLE public.orders (
  id         bigint generated always as identity,
  order_time timestamptz NOT NULL,
  customer   text NOT NULL,
  amount     numeric(12,2) NOT NULL,
  PRIMARY KEY (id, order_time)
) PARTITION BY RANGE (order_time);

CREATE TABLE public.orders_202601
  PARTITION OF public.orders
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE public.orders_202602
  PARTITION OF public.orders
  FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE ROLE repl
  WITH LOGIN
       REPLICATION
       PASSWORD 'replpass';

GRANT USAGE ON SCHEMA public TO repl;
GRANT SELECT ON TABLE public.orders TO repl;
GRANT SELECT ON TABLE public.orders_202601 TO repl;
GRANT SELECT ON TABLE public.orders_202602 TO repl;