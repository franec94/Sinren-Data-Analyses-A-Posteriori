SELECT trd.timestamp, trd.hf,
  COUNT(*) as occrs,
  AVG( DISTINCT trd.seed) as avg_seed_vals, AVG( DISTINCT trd.hl) as avg_hl_vals,
  MIN(trd.seed) as min_seed_val, MAX(trd.seed) as max_seed_val,
  MIN(trd.hl) as min_hl_vals, MAX(trd.hl) as max_hl_vals
FROM table_runs_details as trd
GROUP BY trd.timestamp, trd.hf
;

SELECT trd.hf,
  COUNT(*) as occrs,
  AVG( DISTINCT trd.seed) as avg_seed_vals, AVG( DISTINCT trd.hl) as avg_hl_vals,
  MIN(trd.seed) as min_seed_val, MAX(trd.seed) as max_seed_val,
  MIN(trd.hl) as min_hl_vals, MAX(trd.hl) as max_hl_vals
FROM table_runs_details as trd
GROUP BY trd.hf
;

SELECT trd.hf, trd.hl, COUNT(*) as occrs
FROM table_runs_details as trd
WHERE trd.hf IN (SELECT MIN(trd2.hf)
		FROM table_runs_details as trd2
	)
GROUP BY trd.hf, trd.hl
;

SELECT trd.hf, trd.hl, COUNT(*) as occrs
FROM table_runs_details as trd
WHERE trd.hf IN (SELECT MAX(trd2.hf)
		FROM table_runs_details as trd2
	)
GROUP BY trd.hf, trd.hl
;