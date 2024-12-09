-- Delete grant by key alone.
delete from
	access_grants
where
	key = %(key)s
;
