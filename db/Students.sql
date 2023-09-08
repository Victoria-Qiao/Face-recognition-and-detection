CREATE DATABASE Students;

CREATE TABLE students(
	studentId char NOT NULL UNIQUE,
	studentName varchar(50) NOT NULL,
	matrix blob NOT NULL,
	CONSTRAINT sId PRIMARY KEY (studentId) 
);