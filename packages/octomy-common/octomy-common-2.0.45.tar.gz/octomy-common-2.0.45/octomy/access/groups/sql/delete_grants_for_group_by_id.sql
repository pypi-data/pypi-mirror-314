-- Delete associated grants
delete from
	access_grants
where
	group_id = %(id)s
;
