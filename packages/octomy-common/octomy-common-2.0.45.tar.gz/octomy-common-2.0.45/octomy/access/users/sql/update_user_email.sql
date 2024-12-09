-- Update user's email from old_email to new_email.
update access_users
set
	  email =  %(new_email)s
	, updated_at = now()
where
	email = %(old_email)s
returning
	id
;
