-- Table intended for keeping trace of
-- different trials,, when training Siren-based models.
CREATE TABLE table_runs_logged (
    image           STRING (1, 256) NOT NULL,
    date            STRING (8, 8)   NOT NULL,
    timestamp       STRING (17, 17) NOT NULL
                                    PRIMARY KEY,
    hidden_features INT             NOT NULL,
    image_size      STRING (1, 256) NOT NULL,
    status          STRING          NOT NULL
);


-- Table intended for defining different
-- possible status, represented by a string code,
-- in which a trial migth be.
CREATE TABLE table_code_status_runs (
    code STRING (1, 256) NOT NULL
                       PRIMARY KEY
);
