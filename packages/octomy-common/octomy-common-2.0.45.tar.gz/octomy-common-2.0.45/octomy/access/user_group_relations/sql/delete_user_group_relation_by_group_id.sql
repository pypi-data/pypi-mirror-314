--  Delete user group relation by group id
delete from
	access_user_group_relations
where
	group_id = %(group_id)s
;
