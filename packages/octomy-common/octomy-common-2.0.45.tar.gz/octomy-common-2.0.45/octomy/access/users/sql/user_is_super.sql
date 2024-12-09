-- Return if user identified by email is super user.
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
order by
	updated_at desc, password_changed_at desc, login_at desc
limit %(limit)s;
