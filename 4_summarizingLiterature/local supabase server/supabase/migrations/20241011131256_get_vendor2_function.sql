create or replace function get_vendors()
returns setof vendor2
language sql
as $$
  select * from vendor2;
$$;