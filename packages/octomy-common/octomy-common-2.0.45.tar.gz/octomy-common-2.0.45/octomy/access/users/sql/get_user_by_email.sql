-- Return user by email
select
	  id
	, name
	, email
	, enabled
	, super
	, password_hash is not null as password_set
	, data
	, updated_at
	, password_changed_at
	, login_at
	, created_at
from
	access_users
where
	email = %s
limit 1;
