create or replace function hello_world() -- 1
returns text -- 2
language sql -- 3
as $$  -- 4
  select 'hello world';  -- 5
$$; --6



create or replace function get_vendors()
returns setof vendor2
language sql
as $$
  select * from vendor2;
$$;
