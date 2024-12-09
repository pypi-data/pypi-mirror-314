-- Get users associated with a group by group_id.
select
	u.id
  , u.name
  , u.email
  , u.enabled
  , u.super
  , u.password_hash is not null as password_set
  , u.login_at
  , u.updated_at
from
	access_user_group_relations as ugr
left join
	access_users as u
on
	u.id = ugr.user_id
where
	ugr.group_id = %(group_id)s
order by
	u.updated_at desc
limit
	%(limit)s
;
