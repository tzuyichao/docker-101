-- replication user
CREATE ROLE repl WITH LOGIN REPLICATION PASSWORD 'replpass';

-- lab db
CREATE DATABASE lab;

\c lab

CREATE TABLE public.items (
  id        bigint PRIMARY KEY,
  name      text NOT NULL,
  qty       int  NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO public.items (id, name, qty) VALUES
(1, 'apple', 10),
(2, 'banana', 20);

CREATE ROLE repl
  WITH LOGIN
       REPLICATION
       PASSWORD 'replpass';

GRANT USAGE ON SCHEMA public TO repl;
GRANT SELECT ON TABLE public.items TO repl;