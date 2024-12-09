-- Update user's password given email and that the old password matches.
update access_users
set
	  password_hash = crypt(%(password)s, gen_salt('bf', %(cost_factor)s))
	, password_changed_at = now()
	, updated_at = now()
where
	email = %(email)s
and
	password_hash = crypt(%(old_password)s, password_hash)
returning
	id
;
