-- ======================================================== --
-- Check the number of tuples for status code.
-- via stanrd join operation.
-- ======================================================== --
select status, count(status)
from table_runs_logged as trl, table_code_status_runs as tcsr
where tcsr.code = trl.status
group by trl.status;

-- ======================================================== --
-- Check the number of tuples for status code
-- by means of nested queries and IN/NOT IN SQL statements.
-- ======================================================== --
select status, count(status)
from table_runs_logged as trl
where trl.status in (select tcsr.code
                    from table_code_status_runs as tcsr)
group by trl.status;
