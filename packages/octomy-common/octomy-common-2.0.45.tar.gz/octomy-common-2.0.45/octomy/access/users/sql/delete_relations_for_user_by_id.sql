-- Delete any groups relations for user with id
delete from
	access_user_group_relations
where
	user_id = %(id)s
;
