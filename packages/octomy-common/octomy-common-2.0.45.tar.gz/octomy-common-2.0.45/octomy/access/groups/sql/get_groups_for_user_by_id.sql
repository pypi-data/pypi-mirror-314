-- Return groups for user by user_id.
select
	g.id
  , g.name
  , g.description
  , g.enabled
  , g.updated_at
  , g.created_at
from
	access_user_group_relations as ugr
inner join
	access_groups as g
on
	g.id = ugr.group_id
where
	ugr.user_id = %(user_id)s
order by
	g.updated_at desc
limit
	 %(limit)s
;
