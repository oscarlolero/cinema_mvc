DROP DATABASE IF EXISTS cinema;
CREATE DATABASE cinema;
USE cinema;

CREATE TABLE users (
	user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    is_admin BOOL,
    PRIMARY KEY (user_id)
);

CREATE TABLE halls (
	hall_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    seats_x INT NOT NULL,
    seats_y INT NOT NULL,
    PRIMARY KEY (hall_id)
);

CREATE TABLE movies (
	movie_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    rating VARCHAR(10) NOT NULL,
    PRIMARY KEY (movie_id)
);

CREATE TABLE schedules (
    hall_id INT NOT NULL,
    movie_id INT NOT NULL,
    date VARCHAR(50),
    time VARCHAR(50),
    PRIMARY KEY (hall_id)
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE seats (
	seat_id VARCHAR(10) NOT NULL,
    schedule_id INT NOT NULL,
	PRIMARY KEY (seat_id),
	FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id)
);


INSERT INTO users (`username`, `password`, `is_admin`) VALUES('user', 'lol', false);
INSERT INTO users (`username`, `password`, `is_admin`) VALUES('admin', 'lol', true);

SELECT * FROM users;