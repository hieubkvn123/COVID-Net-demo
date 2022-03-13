# Delete database
DROP DATABASE IF EXISTS FYP;

# Create database
CREATE DATABASE IF NOT EXISTS FYP;
USE FYP; 

# Drop all tables if exists 
DROP TABLE IF EXISTS ACCOUNT;
DROP TABLE IF EXISTS HOSPITAL;
DROP TABLE IF EXISTS PATIENT_RECORD;
DROP TABLE IF EXISTS DIAGNOSIS;

# Create tables
CREATE TABLE HOSPITAL (
	hospital_name VARCHAR(500) NOT NULL,
	address VARCHAR(500) NOT NULL,
	CONSTRAINT hospital_pkey PRIMARY KEY (hospital_name)
);

CREATE TABLE  ACCOUNT (
	account_id INT NOT NULL,
	fname VARCHAR(500) NOT NULL,
	lname VARCHAR(500) NOT NULL,
	hospital_name VARCHAR(500) NOT NULL,
	CONSTRAINT account_pkey PRIMARY KEY (account_id),
	CONSTRAINT account_fkey FOREIGN KEY (hospital_name) REFERENCES HOSPITAL(hospital_name)
			ON DELETE CASCADE
);

# If a new record with the same nric comes
# no row will be written, only diagnosis will be written
CREATE TABLE PATIENT_RECORD (
	nric_fin VARCHAR(10) NOT NULL,
	phone INT NOT NULL,
	fname VARCHAR(500) NOT NULL,
	lname VARCHAR(500) NOT NULL,
	gender VARCHAR(5) NOT NULL,
	dob DATETIME NOT NULL,
	xray_img_url VARCHAR(500) NOT NULL,
	CONSTRAINT patient_record_pkey PRIMARY KEY (nric_fin)
);

CREATE TABLE DIAGNOSIS (
	patient_nric_fin VARCHAR(10) NOT NULL,
	bystaff_account_id INT NOT NULL,
	date_time DATETIME NOT NULL,
	result VARCHAR(7) NOT NULL,
	confidence DECIMAL(10, 2) NOT NULL,
	CONSTRAINT diagnosis_fkey FOREIGN KEY (patient_nric_fin) REFERENCES PATIENT_RECORD(nric_fin)
		ON DELETE CASCADE
);


# Insert some test data 
