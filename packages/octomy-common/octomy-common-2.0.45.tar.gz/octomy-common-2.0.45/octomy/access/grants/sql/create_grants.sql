-- Create a table to keep group grants.
create table if not exists access_grants (
	  group_id uuid
	, key varchar(1023) not null
	, created_at timestamptz not null default now()
	, primary key(group_id, key)
);
comment on column access_grants.group_id is 'The group for this grant.';
comment on column access_grants.key is 'The key by which this grant is identified';
comment on column access_grants.created_at is 'The time this group grant was first registered in our system';
