CREATE TABLE searches (
  topic VARCHAR PRIMARY KEY, -- GENERATED ALWAYS AS IDENTITY
  subtopic VARCHAR,
  search_query text,
  search_plattform text,
  comment text,
  created_at TIMESTAMPTZ DEFAULT NOW()
);