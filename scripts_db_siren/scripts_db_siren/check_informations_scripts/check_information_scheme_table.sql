SELECT *
FROM sqlite_master
WHERE type='table';

SELECT *
FROM sqlite_master
WHERE type='table' AND name = 'table_runs_logged';

SELECT *
FROM sqlite_master
WHERE type='table' AND name = 'table_code_status_runs';

pragma table_info('table_runs_logged');
pragma table_info('table_code_status_runs');