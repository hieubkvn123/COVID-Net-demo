-- ## Un-comment when using MySQL ## ---
-- ## Delete database ## --
-- DROP DATABASE IF EXISTS FYP;

-- ## Create database ## --
-- CREATE DATABASE IF NOT EXISTS FYP;
-- USE FYP;

-- Drop all tables if exists ---
DROP TABLE IF EXISTS ACCOUNT;
DROP TABLE IF EXISTS HOSPITAL;
DROP TABLE IF EXISTS PATIENT_RECORD;
DROP TABLE IF EXISTS DIAGNOSIS;

-- Create tables
CREATE TABLE HOSPITAL (
	hospital_name VARCHAR(500) NOT NULL,
	address VARCHAR(500) NOT NULL,
	CONSTRAINT hospital_pkey PRIMARY KEY (hospital_name)
);

CREATE TABLE  ACCOUNT (
	account_id VARCHAR(20) NOT NULL,
	password VARCHAR(100) NOT NULL, 
	fname VARCHAR(500) NOT NULL,
	lname VARCHAR(500) NOT NULL,
	hospital_name VARCHAR(500) NOT NULL,
	CONSTRAINT account_pkey PRIMARY KEY (account_id),
	CONSTRAINT account_fkey FOREIGN KEY (hospital_name) REFERENCES HOSPITAL(hospital_name)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

-- If a new record with the same nric comes
-- No row will be written, only diagnosis will be written
CREATE TABLE PATIENT_RECORD (
	nric_fin VARCHAR(10) NOT NULL,
	phone INT NOT NULL,
	fname VARCHAR(500) NOT NULL,
	lname VARCHAR(500) NOT NULL,
	gender VARCHAR(5) NOT NULL,
	dob DATETIME NOT NULL,
	CONSTRAINT patient_record_pkey PRIMARY KEY (nric_fin)
);

CREATE TABLE DIAGNOSIS (
	patient_nric_fin VARCHAR(10) NOT NULL,
	bystaff_account_id VARCHAR(20) NOT NULL,
	date_time DATETIME NOT NULL,
	result VARCHAR(7) NOT NULL,
	confidence DECIMAL(10, 2) NOT NULL,
	xray_img_url VARCHAR(500) NOT NULL,
	CONSTRAINT diagnosis_fkey FOREIGN KEY (patient_nric_fin) REFERENCES PATIENT_RECORD(nric_fin)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);


-- Insert some test data 
-- Sample hospitals
INSERT INTO HOSPITAL VALUES("Tan Tock Seng Hospital", "11 Jln Tan Tock Seng, Singapore 308433");
INSERT INTO HOSPITAL VALUES("Mount Elizabeth Novena Hospital", "38 Irrawaddy Rd, Singapore 329563");

-- Sample accounts
-- Sample account no. 1 - password = md5("qazwsx007")
INSERT INTO ACCOUNT VALUES("nong003", "8c96d10577e6eb7c2256aedbbb7b0619", "Nong", "Hieu", "Mount Elizabeth Novena Hospital");

-- Sample account no. 2 - password = md5("qwaszx007")
INSERT INTO ACCOUNT VALUES("hieu004", "4de15641236bd29f747d7e5d94f661d1", "Hieu", "Nong", "Tan Tock Seng Hospital");