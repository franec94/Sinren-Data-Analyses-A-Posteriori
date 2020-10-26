-- Trigged aiming at checking out
-- whether new inserted row owns
-- a value for code status that is
-- compliant with available status codes
-- defined ahead of time when db was created.
CREATE TRIGGER check_input_status_value
        BEFORE INSERT
            ON table_runs_logged
      FOR EACH ROW
BEGIN
    SELECT CASE (
                    SELECT count( * ) 
                    FROM table_code_status_runs
                    WHERE code = NEW.status
                )
           WHEN 0 THEN RAISE(ABORT, "Wrong tuple!") END;
END;