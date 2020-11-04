SELECT COUNT(*)
FROM table_runs_logged AS trl, table_runs_details trd
WHERE trl.timestamp = trd.timestamp
;

SELECT trd.hf, trd.image_name, trd.is_cropped, trd.cropped_heigth, trd.cropped_width,
	COUNT(*) AS trials_done, MIN(trd.hl) AS min_hl, MAX(trd.hl) AS max_hl
FROM table_runs_logged AS trl, table_runs_details trd
WHERE trl.timestamp = trd.timestamp
	AND trd.is_cropped = 'TRUE'
	AND trd.cropped_heigth = 256 AND trd.cropped_width = 256
GROUP BY trd.hf, trd.image_name, trd.is_cropped, trd.cropped_heigth, trd.cropped_width
ORDER BY trd.hf, trd.image_name, MIN(trd.hl)
;

-- SELECT trd.hf, COUNT(*) AS trials_done, MIN(trd.hl) AS min_hl, MAX(trd.hl) AS max_hl, AVG(trd.hl) AS avg_hl
SELECT trd.hf, trd.is_cropped, trd.cropped_heigth, trd.cropped_width,
	COUNT(*) AS trials_done, MIN(trd.hl) AS min_hl, MAX(trd.hl) AS max_hl
FROM table_runs_logged AS trl, table_runs_details trd
WHERE trl.timestamp = trd.timestamp
	AND trd.is_cropped = 'TRUE'
	AND trd.cropped_heigth = 256 AND trd.cropped_width = 256
GROUP BY trd.hf, trd.is_cropped, trd.cropped_heigth, trd.cropped_width
ORDER BY trd.hf, MIN(trd.hl)
;

SELECT trd.hf, trd.hl, COUNT(*) as trials_done
FROM table_runs_logged AS trl, table_runs_details trd
WHERE trl.timestamp = trd.timestamp
GROUP BY trd.hf, trd.hl
;