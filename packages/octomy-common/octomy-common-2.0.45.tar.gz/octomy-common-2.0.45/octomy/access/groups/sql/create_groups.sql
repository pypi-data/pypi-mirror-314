-- Create a table to keep groups.
create table if not exists access_groups (
	  id uuid DEFAULT uuid_generate_v4 () primary key
	, name varchar(1023)
	, description text
	, enabled boolean not null default false
	, data json default '{}'::json
	, created_at timestamptz not null default now()
	, updated_at timestamptz not null default now()
);
comment on column access_groups.id is 'The unique id of the group.';
comment on column access_groups.name is 'The full name (informal identifier) of the group.';
comment on column access_groups.description is 'The description of the group.';
comment on column access_groups.enabled is 'Wether or not users of this group are able to log in.';
comment on column access_groups.data is 'The preferences and other data for the group as json.';
comment on column access_groups.created_at is 'The time this group was first registered in our system';
comment on column access_groups.updated_at is 'The last time data about this group was udpated in our system';
