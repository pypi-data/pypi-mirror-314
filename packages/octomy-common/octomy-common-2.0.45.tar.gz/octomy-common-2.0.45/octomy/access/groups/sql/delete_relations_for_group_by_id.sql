-- Delete associated user relations
delete from
	access_user_group_relations
where
	group_id = %(id)s
;
