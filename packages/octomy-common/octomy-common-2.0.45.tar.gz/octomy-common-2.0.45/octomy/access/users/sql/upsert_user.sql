-- Update or insert user, return user's id.
insert into access_users
	(
	  id, 
	, name
	, email
	, enabled
	, super
	, data
	, login_at
	, updated_at
	)
values
	(
	  %(id)s
	, %(name)s
	, %(email)s
	, %(enabled)s
--                , (super)s NOT ALLOWED FOR SECURITY
	, %(data)s
	, null
	, now()
	)
on
	conflict (id)
do
	update
set
	  name = %(name)s
	, email = %(email)s
	, enabled = %(enabled)s
--                , super = (super)s NOT ALLOWED FOR SECURITY
	, data = %(data)s
	, updated_at = now()
returning id
;
