-- Matches document sections using vector similarity search on embeddings
--
-- Returns a setof documents_chunks so that we can use PostgREST resource embeddings (joins with other tables)
-- Additional filtering like limits can be chained to this function call
create or replace function match_documents_chunks(
  embedding vector(384), 
  match_threshold float, 
  match_count int default 5
)
returns setof documents_chunks
language plpgsql
as $$
#variable_conflict use_variable
begin
  return query
  select document_id, content
  from (
    select document_id, content
    from documents_chunks
    where documents_chunks.embedding <#> embedding < -match_threshold
    order by documents_chunks.embedding <#> embedding
  ) as top_matches
  order by random()
  limit match_count;
end;
$$;
