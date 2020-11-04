select trl.timestamp, count(*) as no_ts
from table_runs_logged as trl, table_backuped_runs tbr
where trl.timestamp = tbr.timestamp
group by trl.timestamp;

select *
from table_runs_logged as trl, table_backuped_runs tbr
where trl.timestamp = tbr.timestamp;