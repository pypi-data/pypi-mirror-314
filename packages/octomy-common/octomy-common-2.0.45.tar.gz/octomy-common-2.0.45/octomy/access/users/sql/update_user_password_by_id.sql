-- Update user's password given id.
update access_users
set
	  password_hash = crypt(%(password)s, gen_salt('bf', %(cost_factor)s))
	, password_changed_at = now()
	, updated_at = now()
where
	id = %(id)s
returning
	id
;
