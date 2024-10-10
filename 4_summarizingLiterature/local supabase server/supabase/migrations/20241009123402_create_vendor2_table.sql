CREATE TABLE vendor2 (
  vendor_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  vendor_name varchar,
  vendor_location varchar,
  total_employees bigint,
  created_at TIMESTAMPTZ DEFAULT NOW()
);