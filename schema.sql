-- schema.sql
-- Database Schema for Fitness Tracker App
-- This file defines all tables used in the project.

-- ---------------------------
-- Table: users
-- Stores user login and profile information
-- ---------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INT,
    height FLOAT,
    weight FLOAT,
    gender VARCHAR(255)
);

-- ---------------------------
-- Table: bmi_logs
-- Tracks user's BMI over time
-- ---------------------------
CREATE TABLE bmi_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    bmi FLOAT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ---------------------------
-- Table: meals
-- Logs meals consumed by user
-- ---------------------------
CREATE TABLE meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_time VARCHAR(50),
    items TEXT,
    date DATE,
    calories INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ---------------------------
-- Table: sleep_logs
-- Logs user's sleep duration
-- ---------------------------
CREATE TABLE sleep_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    hours FLOAT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ---------------------------
-- Table: step_logs
-- Logs user's steps per day
-- ---------------------------
CREATE TABLE step_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    steps INT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ---------------------------
-- Table: workout_logs
-- Logs workout sessions
-- ---------------------------
CREATE TABLE workout_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type VARCHAR(100),
    duration INT,
    calories_burned FLOAT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ---------------------------
-- Table: positions
-- (Optional: stores roles/positions for some feature)
-- ---------------------------
CREATE TABLE positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- ---------------------------
-- Table: applications
-- Job application details (possibly from another feature)
-- ---------------------------
CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    position_id INT,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    FOREIGN KEY (position_id) REFERENCES positions(id)
);

-- ---------------------------
-- Table: students
-- (Optional: test/demo data table)
-- ---------------------------
CREATE TABLE students (
    name VARCHAR(99),
    phno VARCHAR(99),
    address VARCHAR(999)
);
