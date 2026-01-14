-- replication user (for physical streaming replication)
CREATE ROLE repl WITH LOGIN REPLICATION PASSWORD 'replpw';

-- allow repl to read tables later (for initial table copy of logical replication)
GRANT CONNECT ON DATABASE appdb TO repl;
GRANT USAGE ON SCHEMA public TO repl;

-- demo table
CREATE TABLE public.items (
  id  int primary key,
  val text
);

INSERT INTO public.items VALUES (1, 'one'), (2, 'two');

-- grant SELECT so logical initial copy won't fail
GRANT SELECT ON TABLE public.items TO repl;
