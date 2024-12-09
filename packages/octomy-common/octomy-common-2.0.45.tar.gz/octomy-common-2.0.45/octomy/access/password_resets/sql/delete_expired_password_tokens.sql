-- Delete all exired password resets.
delete from
	access_password_resets as pr
where
	pr.created_at + pr.time_limit < now()
;
