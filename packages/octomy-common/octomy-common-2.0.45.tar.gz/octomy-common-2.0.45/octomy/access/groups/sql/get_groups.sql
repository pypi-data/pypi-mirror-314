-- Return groups.
select
	id
  , name
  , description
  , enabled
  , updated_at
  , created_at
from
	access_groups
order by
	updated_at desc
limit %(limit)s
;
