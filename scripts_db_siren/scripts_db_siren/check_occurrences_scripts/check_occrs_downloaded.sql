select upper(trl.status) as status, count(*) ocrrs_not_downloaded
from table_runs_logged as trl
where trl.data_downloaded is FALSE
group by trl.status;