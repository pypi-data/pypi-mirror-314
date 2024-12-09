-- Create a table to keep user group relations.
create table if not exists access_user_group_relations (
	  user_id uuid
	, group_id uuid
	, created_at timestamptz not null default now()
	, primary key(user_id, group_id)
);
comment on column access_user_group_relations.user_id is 'The group to which the user belongs in this relation.';
comment on column access_user_group_relations.group_id is 'The user that is related to the group in this relation.';
comment on column access_user_group_relations.created_at is 'The time this group relation was first registered in our system';
