-- Delete grant by group_id alone.
delete from
	access_grants
where
	group_id = %(group_id)s
;
