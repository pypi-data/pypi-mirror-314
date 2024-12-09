-- Delete the actual group
delete from
	access_groups
where
	id = %(id)s
;
