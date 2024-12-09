--  Delete user group relation by user id and group id
delete from
	access_user_group_relations
where
	group_id = %(group_id)s
and
	user_id = %(user_id)s
;
