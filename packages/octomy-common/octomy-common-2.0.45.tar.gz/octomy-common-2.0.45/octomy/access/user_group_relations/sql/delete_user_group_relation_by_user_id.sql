--  Delete user group relation by user id
delete from
	access_user_group_relations
where
	user_id = %(user_id)s
;
