-- Delete user's password given id.
update access_users
set
	  password_hash = null
	, password_changed_at = now()
	, updated_at = now()
where
	id = %(id)s
returning
	id
;
