-- Create a table to keep users.
create table if not exists access_users (
	  id uuid DEFAULT uuid_generate_v4 () primary key
	, name varchar(1023)
	, email varchar(1023) not null unique
	, password_hash varchar(1023)
	, enabled boolean not null default false
	, super boolean not null default false
	, data json default '{}'::json
	, created_at timestamptz not null default now()
	, password_changed_at timestamptz
	, login_at timestamptz
	, updated_at timestamptz not null default now()
);
comment on column access_users.id is 'The unique id of the user.';
comment on column access_users.name is 'The full name (informal identifier) of the user.';
comment on column access_users.email is 'The email (username) of the user.';
comment on column access_users.password_hash is 'The salted hash of the user''s password.';
comment on column access_users.enabled is 'Wether or not this user is able to log in.';
comment on column access_users.super is 'Wether or not this user is an super user (all access granted bypassing groups and grants).';
comment on column access_users.data is 'The preferences and other data for the user as json.';
comment on column access_users.created_at is 'The time this user was first registered in our system';
comment on column access_users.password_changed_at is 'The time this user last changed her password';
comment on column access_users.login_at is 'The time this user was last successfully logged in to our system';
comment on column access_users.updated_at is 'The last time data about this user was udpated in our system';
