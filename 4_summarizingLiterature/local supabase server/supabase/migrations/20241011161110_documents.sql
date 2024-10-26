create extension if not exists pg_net with schema extensions;
create extension if not exists vector with schema extensions;


CREATE TABLE documents (
  id VARCHAR PRIMARY KEY, -- GENERATED ALWAYS AS IDENTITY
  topic VARCHAR NOT NULL,
  subtopic VARCHAR,
  select_bool BOOLEAN DEFAULT TRUE,
  num_pages BIGINT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);


CREATE TABLE documents_chunks (
  document_id VARCHAR DEFAULT md5(random()::text || clock_timestamp()::text), -- Unique hash for each row
  id VARCHAR REFERENCES documents(id) ON DELETE CASCADE, -- id as a foreign key referencing documents
  order_chunks BIGINT,
  section VARCHAR,
  content VARCHAR NOT NULL, -- Changed from TEXT to VARCHAR
  embedding VECTOR(384),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (document_id, id) -- Composite primary key combining document_id and id
);