-- Insert user.
insert into access_users
	(
	  name
	, email
	, password_hash
	, enabled
	, super
	, data
	, password_changed_at
	, login_at
	, updated_at
	)
values
	(
	  %(name)s
	, %(email)s
	, null
	, %(enabled)s
	, false
	, %(data)s
	, now()
	, null
	, now()
	)
returning id
;
