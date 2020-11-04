SELECT name
FROM sqlite_master
WHERE type = 'trigger';

SELECT @cnt  = count(name)
FROM sqlite_master
WHERE type = 'trigger' AND name = 'check_compression_tuple_trigger';

IF @cnt > 0 THEN
	DROP TRIGGER 'check_compression_tuple_trigger' ;
END IF;

CREATE TRIGGER check_compression_tuple_trigger BEFORE INSERT
ON compressions_table
BEGIN
	IF (NEW.width < NEW.crop_width) THEN
		ABORT('Error, cropped width is greater than width')
	END IF;
	
	IF (NEW.heigth < NEW.crop_heigth) THEN
		ABORT('Error, cropped heigth is greater than heigth')
	END IF;
	
	IF (NEW.width <= NEW.crop_width OR NEW.crop_heigth <= NEW.crop_heigth)
		IF (NEW.is_cropped = false) THEN
			NEW.is_cropped := true;
		END IF;
	END IF;
	
	IF (NEW.width = NEW.crop_width OR NEW.crop_heigth = NEW.crop_heigth) THEN
		IF (NEW.is_cropped = true) THEN
			SET NEW.is_cropped = false;
		END IF;
	END IF;
END;

CREATE TRIGGER audit_log_compression_tuple_trigger AFTER INSERT 
ON compressions_table
BEGIN
   INSERT INTO audit_compression_table (id, entry_date, code) VALUES (new.ID, datetime('now'), 'insert');
END;

CREATE TRIGGER audit_log_compression_tuple_trigger AFTER UPDATE 
ON compressions_table
BEGIN
   INSERT INTO audit_compression_table (id, entry_date, code) VALUES (new.id, datetime('now'), 'update');
END;

CREATE TRIGGER audit_log_compression_tuple_trigger AFTER DELETE
ON compressions_table
BEGIN
   INSERT INTO audit_compression_table (id, entry_date, code) VALUES (old.id, datetime('now'), 'delete');
END;