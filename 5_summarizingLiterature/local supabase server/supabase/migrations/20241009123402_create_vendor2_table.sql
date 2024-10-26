-- Create a new table 'vendor2'
CREATE TABLE vendor2 (
  vendor_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  vendor_name VARCHAR,
  vendor_location VARCHAR,
  total_employees BIGINT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create or replace function 'hello_world2'
CREATE OR REPLACE FUNCTION hello_world2()
RETURNS TEXT
LANGUAGE SQL
AS $$
  SELECT 'hello world 2';
$$;

-- Create or replace function 'hello_world3'
CREATE OR REPLACE FUNCTION hello_world3()
RETURNS TEXT
LANGUAGE SQL
AS $$
  SELECT 'hello world 3';
$$;