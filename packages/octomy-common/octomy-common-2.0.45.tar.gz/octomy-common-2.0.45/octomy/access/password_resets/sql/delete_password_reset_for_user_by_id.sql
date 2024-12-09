-- Delete valid password_resets for user given user_id ('use' it).
delete from
	access_password_resets as pr
where
	pr.user_id = %(user_id)s
and
	pr.token  = %(token)s
returning pr.time_limit
;
