CREATE DATABASE user_auth;
USE user_auth;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(50),
    marks INT
);

INSERT INTO grades(subject, marks) VALUES
('Maths', 85),
('DBMS', 78),
('OS', 88),
('CN', 80);
