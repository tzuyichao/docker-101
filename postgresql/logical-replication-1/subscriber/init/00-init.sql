
CREATE DATABASE lab;

\c lab

CREATE TABLE public.items (
  id        bigint PRIMARY KEY,
  name      text NOT NULL,
  qty       int  NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);
