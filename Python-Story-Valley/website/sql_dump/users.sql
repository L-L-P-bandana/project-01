-- SQLite
CREATE TABLE IF NOT EXISTS users (
userid INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, account INTEGER NOT NULL);

INSERT INTO users(userid,name,password,email,account)
VALUES (1, 'Admin', 'Admin', 'Admin@Admin.com', 2),
(2, 'Teacher', 'Teacher', 'Teacher@Teacher.com', 1),
(3, 'Student', 'Student', 'Student@Student.com', 0);