-- Delete grant by key and group_id.
delete from
	access_grants
where
	group_id = %(group_id)s
and
	key = %(key)s
;
