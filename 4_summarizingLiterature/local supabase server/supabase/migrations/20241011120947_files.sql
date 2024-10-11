create schema private;

insert into storage.buckets (id, name)
values ('files', 'files');



create policy "Users can upload files"
ON storage.objects
for insert with check (
  true
);

create policy "Users can download files"
ON storage.objects
for select using (
  true
);

create policy "Users can delete files"
ON storage.objects
for delete using (
  true
);



-- create policy "Users can delete their own files"
-- on storage.objects for delete to authenticated using (
--  bucket_id = 'files' and owner = auth.uid()
--);