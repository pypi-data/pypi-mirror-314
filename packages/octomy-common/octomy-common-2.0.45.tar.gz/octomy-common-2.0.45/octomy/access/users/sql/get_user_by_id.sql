-- Return user by id
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
	id = %(id)s
limit 1;
