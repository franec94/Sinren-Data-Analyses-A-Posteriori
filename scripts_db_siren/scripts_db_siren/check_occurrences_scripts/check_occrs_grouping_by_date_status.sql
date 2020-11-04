-- ======================================================== --
-- Check number of trials grouping by date and status.
-- ======================================================== --
-- v1:
select trl.date, trl.status, count(trl.status) as ocrrs
from table_runs_logged as trl, table_code_status_runs as tcsr
where tcsr.code = trl.status
group by trl.date, trl.status
order by trl.date, trl.status;

-- v2:
select trl.date, trl.status, count(trl.status) as ocrrs
from table_runs_logged as trl
where trl.status in (select tcsr.code
                    from table_code_status_runs as tcsr)
group by trl.date, trl.status
order by trl.date, trl.status;

-- ======================================================== --
-- Check number of trials grouping by date.
-- ======================================================== --
-- v1:
select trl.date, count(trl.status) as ocrrs
from table_runs_logged as trl, table_code_status_runs as tcsr
where tcsr.code = trl.status
group by trl.date
order by trl.date;

-- v2:
select trl.date, count(trl.status) as ocrrs
from table_runs_logged as trl
where trl.status in (select tcsr.code
                    from table_code_status_runs as tcsr)
group by trl.date
order by trl.date;