-- Matches document sections using vector similarity search on embeddings
--
-- Returns a setof documents_chunks so that we can use PostgREST resource embeddings (joins with other tables)
-- Additional filtering like limits can be chained to this function call
create or replace function match_documents_chunks(embedding vector(384), match_threshold float)
returns setof documents_chunks
language plpgsql
as $$
#variable_conflict use_variable
begin
  return query
  select *
  from documents_chunks

  -- The inner product is negative, so we negate match_threshold
  where documents_chunks.embedding <#> embedding < -match_threshold

  -- Our embeddings are normalized to length 1, so cosine similarity
  -- and inner product will produce the same query results.
  -- Using inner product which can be computed faster.
  --
  -- For the different distance functions, see https://github.com/pgvector/pgvector
  order by documents_chunks.embedding <#> embedding;
end;
$$;
