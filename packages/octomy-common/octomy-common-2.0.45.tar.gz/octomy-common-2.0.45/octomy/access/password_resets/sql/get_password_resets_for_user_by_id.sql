-- Get password_resets for user given user_id
select
	  pr.token
	, pr.time_limit
	, pr.created_at
from
	access_password_resets as pr
where
	pr.user_id = %(user_id)s
group by
	pr.token
order by
	pr.created_at desc
limit
	 %(limit)s
;
