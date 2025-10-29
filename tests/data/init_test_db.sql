-- Test database initialization script
CREATE DATABASE IF NOT EXISTS ssisdb_test;
USE ssisdb_test;

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY(username)
);

-- Course table
CREATE TABLE IF NOT EXISTS course (
    code VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    college VARCHAR(45) NOT NULL,
    PRIMARY KEY(code)
);

-- College table
CREATE TABLE IF NOT EXISTS college (
    code VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY(code)
);

-- Student table
CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(9) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    middlename VARCHAR(20) NOT NULL,
    lastname VARCHAR(20) NOT NULL,
    year INT(1) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    coursecode VARCHAR(10) NOT NULL,
    collegecode VARCHAR(10),
    photo VARCHAR(500),
    PRIMARY KEY(id),
    FOREIGN KEY(coursecode) REFERENCES course(code),
    FOREIGN KEY(collegecode) REFERENCES college(code)
);

-- Insert test data
INSERT IGNORE INTO admin (username, password) 
VALUES ('test_admin', 'pbkdf2:sha256:260000$test_hash');

INSERT IGNORE INTO college (code, name) 
VALUES ('COL1', 'Test College');

INSERT IGNORE INTO course (code, name, college) 
VALUES ('CRS1', 'Test Course', 'COL1');

INSERT IGNORE INTO students (id, firstname, middlename, lastname, year, gender, coursecode, collegecode) 
VALUES ('2021-0001', 'Test', 'Middle', 'Student', 1, 'Male', 'CRS1', 'COL1');