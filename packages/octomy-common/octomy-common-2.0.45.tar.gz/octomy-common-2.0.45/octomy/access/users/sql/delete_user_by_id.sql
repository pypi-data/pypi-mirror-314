-- Delete the user by id
delete from
	access_users
where
	id = %(id)s
;
