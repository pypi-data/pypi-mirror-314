-- This code creates or resets the database.

DROP TABLE IF EXISTS Equivalence;
DROP TABLE IF EXISTS Ephemeral;

CREATE TABLE Ephemeral (
    key TEXT PRIMARY KEY,
    val TEXT
);

CREATE TABLE Equivalence (
    greg_year INT,
    greg_month INT,
    greg_day INT,
    cyprian_year INT,
    cyprian_month INT,
    cyprian_day INT,
    PRIMARY KEY(greg_year, greg_month, greg_day)
);
