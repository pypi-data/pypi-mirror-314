-- Return time_limit for password_reset by token if it is still valid.
select
	time_limit
from
	access_password_resets as pr
where
	pr.user_id = %(user_id)s
and
	pr.token  = %(token)s
;
