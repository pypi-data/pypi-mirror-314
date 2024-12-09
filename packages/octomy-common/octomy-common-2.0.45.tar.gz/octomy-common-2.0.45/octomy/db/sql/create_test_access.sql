-- Create a table to keep track of test items 
create table if not exists "test_access" (
	id serial primary key,
	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now()
);
comment on column test_access.id is 'Unique internal id for this item';
comment on column test_access.created_at is 'When the item was first created';
comment on column test_access.updated_at is 'When the item was last updated';
