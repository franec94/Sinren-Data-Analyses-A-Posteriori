-----------------------------------------------------------------------------------------------------------------------------
-- Query:
-- show model type paired with more convenient
-- quantization technique.
-- Results shown in alphabetic and numeric increasing order, if any.
-----------------------------------------------------------------------------------------------------------------------------
SELECT tmtqt.model_type, tqt.quantization
FROM
	table_quantization_techniques AS tqt,
	table_model_type_quantization_tech AS tmtqt
WHERE
	tqt.id = tmtqt.qunatization_tech_id
ORDER BY 
	tmtqt.model_type, tqt.quantization
;

-----------------------------------------------------------------------------------------------------------------------------
-- Query:
-- show quantization techniques
-- available but not yet paired with
-- any kind of (Machine/Deep Learining) model.
-- Results shown in alphabetic and numeric increasing order, if any.
-----------------------------------------------------------------------------------------------------------------------------
SELECT tqt.id, tqt.quantization
FROM
	table_quantization_techniques AS tqt
WHERE
	tqt.id NOT IN ( SELECT DISTINCT tmtqt.qunatization_tech_id
		FROM table_model_type_quantization_tech AS tmtqt
	)
ORDER BY 
	tqt.id, tqt.quantization
;

-----------------------------------------------------------------------------------------------------------------------------
-- Query:
-- show number of occurences 
-- for quantization techniques
-- employed pairing them with a given (Machine/Deep Learining) model.
-- Results shown in alphabetic and numeric increasing order, if any.
-----------------------------------------------------------------------------------------------------------------------------
SELECT tqt.id, tqt.quantization, COUNT(*) AS occrs_no
FROM
	table_quantization_techniques AS tqt,
	table_model_type_quantization_tech AS tmtqt
WHERE
	tqt.id = tmtqt.qunatization_tech_id
GROUP BY
	tqt.id, tqt.quantization
ORDER BY 
	tqt.id, tqt.quantization
;

-----------------------------------------------------------------------------------------------------------------------------
-- Query:
-- show number of occurences 
-- for (Machine/Deep Learining) model
-- employed pairing them with a given quantization techniques.
-- Results shown in alphabetic and numeric increasing order, if any.
-----------------------------------------------------------------------------------------------------------------------------
SELECT tmtqt.model_type, COUNT(*) AS occrs_no
FROM
	table_quantization_techniques AS tqt,
	table_model_type_quantization_tech AS tmtqt
WHERE
	tqt.id = tmtqt.qunatization_tech_id
GROUP BY
	tmtqt.model_type
ORDER BY 
	tmtqt.model_type, (SELECT COUNT(*) AS occrs_no_2        -- Sub query needed for guaranteeing a given
		FROM                                                -- dispalying order.
			table_quantization_techniques AS tqt_2,
			table_model_type_quantization_tech AS tmtqt_2
		WHERE
			tqt_2.id = tmtqt_2.qunatization_tech_id
		GROUP BY
			tmtqt_2.model_type
	)
;
