-- Return id if the supplied email and password hash match for user
update
	access_users
set
	login_at = now()
where
	enabled = true
and
	password_hash is not null
and
	email = %(email)s
and
	password_hash = crypt(%(password)s, password_hash)
returning
	id
;
