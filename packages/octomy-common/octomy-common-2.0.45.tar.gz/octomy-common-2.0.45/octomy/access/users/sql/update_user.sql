-- Update user.
update access_users
set
	  name = %(name)s
	, email = %(email)s
	, enabled = %(enabled)s
--                , super = (super)s NOT ALLOWED FOR SECURITY
	, data = %(data)s
	, updated_at = now()
where
	id = %(id)s
returning
	id
;
