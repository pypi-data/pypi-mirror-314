-- Update user's password given email.
update access_users
set
	  password_hash = crypt(%(password)s, gen_salt('bf', %(cost_factor)s))
	, password_changed_at = now()
	, updated_at = now()
where
	email = %(email)s
returning
	id
;
