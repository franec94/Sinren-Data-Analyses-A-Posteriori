select trl.hidden_features, trl.image, trl.image_size, count(*) occrs
from table_runs_logged as trl, table_code_status_runs as tcsr
where tcsr.code = trl.status
group by trl.hidden_features, trl.image, trl.image_size;


select trl.hidden_features, trl.image, trl.image_size, count(*) occrs, trl.status
from table_runs_logged as trl, table_code_status_runs as tcsr
where tcsr.code = trl.status
group by trl.hidden_features, trl.image, trl.image_size, trl.status;

select trl.hidden_features, trl.image, trl.image_size, count(*) occrs, trl.status
from table_runs_logged as trl
where trl.status = 'done'
group by trl.hidden_features, trl.image, trl.image_size, trl.status;

select trl.hidden_features, trl.image, trl.image_size, count(*) occrs, trl.status, trl.date
from table_runs_logged as trl
where trl.status = 'done'
group by trl.hidden_features, trl.image, trl.image_size, trl.status, trl.date;

select trl.hidden_features, trl.image, trl.image_size, count(*) occrs, trl.status
from table_runs_logged as trl
where trl.status = 'failed'
group by trl.hidden_features, trl.image, trl.image_size, trl.status;

select trl.hidden_features, trl.image, trl.image_size, count(*) occrs, trl.status
from table_runs_logged as trl
where trl.status = 'running'
group by trl.hidden_features, trl.image, trl.image_size, trl.status;
