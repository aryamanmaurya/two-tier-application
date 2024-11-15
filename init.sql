-- init.sql

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS appData;

-- Use the created database
USE appData;

-- Create the `userdata` table
CREATE TABLE IF NOT EXISTS userdata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT CHECK (age >= 0 AND age <= 100) NOT NULL
);
