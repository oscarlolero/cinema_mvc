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

CREATE TABLE movie_schedules (
	movie_schedule_id INT NOT NULL AUTO_INCREMENT,
	hall_id INT NOT NULL,
	movie_id INT NOT NULL,
    time VARCHAR(50),
    PRIMARY KEY (movie_schedule_id),
    FOREIGN KEY (hall_id) REFERENCES halls(hall_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    ON DELETE CASCADE
);
CREATE TABLE function_schedules (
	function_schedule_id INT NOT NULL AUTO_INCREMENT,
	movie_schedule_id INT NOT NULL,
    date VARCHAR(50),
    PRIMARY KEY (function_schedule_id, movie_schedule_id, date),
    FOREIGN KEY (movie_schedule_id) REFERENCES movie_schedules(movie_schedule_id)
    ON DELETE CASCADE
);

CREATE TABLE tickets (
	ticket_id INT NOT NULL AUTO_INCREMENT,
    function_schedule_id INT NOT NULL,
    seat VARCHAR(25) NOT NULL,
	PRIMARY KEY (ticket_id),
    FOREIGN KEY (function_schedule_id) REFERENCES function_schedules(function_schedule_id)
    ON DELETE CASCADE
);

CREATE TABLE user_tickets (
	ticket_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (ticket_id, user_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (`username`, `password`, `is_admin`) VALUES('user', '123', false);
INSERT INTO users (`username`, `password`, `is_admin`) VALUES('admin', 'password', true);
INSERT INTO movies (`name`, `rating`) VALUES('Avengers', 'B');
INSERT INTO movies (`name`, `rating`) VALUES('Lolita', 'C');
INSERT INTO halls (`name`, `seats_x`, `seats_y`) VALUES ('SALA 1', 5, 3);
INSERT INTO halls (`name`, `seats_x`, `seats_y`) VALUES ('SALA 2', 5, 3);

INSERT INTO movie_schedules (`hall_id`, `movie_id`, `time`) VALUES(1, 1, '10:00 pm');
INSERT INTO movie_schedules (`hall_id`, `movie_id`, `time`) VALUES(1, 1, '11:00 pm');
INSERT INTO movie_schedules (`hall_id`, `movie_id`, `time`) VALUES(2, 2, '09:00 pm');
INSERT INTO movie_schedules (`hall_id`, `movie_id`, `time`) VALUES(2, 2, '12:00 pm');
INSERT INTO function_schedules (`movie_schedule_id`, `date`) VALUES(1, '04-05-2020');
INSERT INTO function_schedules (`movie_schedule_id`, `date`) VALUES(3, '04-04-2020');
INSERT INTO function_schedules (`movie_schedule_id`, `date`) VALUES(3, '05-04-2020');
INSERT INTO tickets (`function_schedule_id`, `seat`) VALUES(1, 'A2');
INSERT INTO tickets (`function_schedule_id`, `seat`) VALUES(1, 'A3');
INSERT INTO tickets (`function_schedule_id`, `seat`) VALUES(2, 'A1');
INSERT INTO user_tickets(`ticket_id`, `user_id`) VALUES (1, 1);
-- DELETE FROM movie_schedules WHERE movie_schedule_id = 1;
-- GET FUNC SCHEDULE ID
-- SELECT movie_schedules.movie_schedule_id FROM movie_schedules
 -- JOIN movies ON movies.movie_id = movie_schedules.movie_id
 -- AND movies.name = 'Lolis 2' AND movie_schedules.time = '12:00 pm'
-- SELECT * FROM movies;
-- SELECT * FROM halls;
-- SELECT * FROM movie_schedules;
-- SELECT * FROM function_schedules;
 -- SELECT * FROM tickets;

-- Get movie schedules
 -- SELECT movie_schedules.movie_schedule_id,movies.name, halls.name, movie_schedules.time FROM movies JOIN movie_schedules ON movies.movie_id = movie_schedules.movie_id JOIN halls ON halls.hall_id = movie_schedules.hall_id;

-- Get user tickets
SELECT movies.name, function_schedules.date, movie_schedules.time, halls.name, GROUP_CONCAT(tickets.seat SEPARATOR ", ") AS seats FROM user_tickets
JOIN tickets ON user_tickets.user_id = tickets.user_id
JOIN function_schedules ON tickets.function_schedule_id = function_schedules.function_schedule_id
JOIN movie_schedules ON function_schedules.movie_schedule_id = movie_schedules.movie_schedule_id
JOIN movies ON movie_schedules.movie_id = movies.movie_id
JOIN halls ON movie_schedules.hall_id = halls.hall_id
AND user_tickets.user_id = 1 GROUP BY function_schedules.function_schedule_id ORDER BY function_schedules.date
-- GROUP_CONCAT(tickets.seat SEPARATOR ",")
-- SELECT function_schedules.function_schedule_id, GROUP_CONCAT(tickets.seat SEPARATOR ",") as seats FROM tickets
-- JOIN function_schedules ON function_schedules.function_schedule_id = tickets.function_schedule_id
-- JOIN movie_schedules ON movie_schedules.movie_schedule_id = function_schedules.movie_schedule_id
-- JOIN movies ON movies.movie_id = movie_schedules.movie_id
-- AND movies.name = 'Lolis 2' AND function_schedules.date = '28-04-2020' AND movie_schedules.time = '09:00 pm';



-- Get hall capacity from movie and time
-- SELECT halls.seats_x, halls.seats_y, movie_schedules.movie_schedule_id FROM halls JOIN movie_schedules ON movie_schedules.hall_id = halls.hall_id AND movie_schedules.time = '11:00 pm' JOIN movies ON movies.movie_id = movie_schedules.movie_id AND movies.name = 'Lolis';

-- schedule exists?
-- SELECT function_schedules.function_schedule_id FROM function_schedules 
-- JOIN movie_schedules ON movie_schedules.movie_schedule_id = function_schedules.movie_schedule_id
-- AND function_schedules.date = '28-04-2020' AND movie_schedules.time = '09:00 pm'

-- SELECT halls.seats_x, halls.seats_y, halls.name FROM halls JOIN movie_schedules ON movie_schedules.hall_id = halls.hall_id AND movie_schedules.time = '10:00 pm'JOIN movies ON movies.name = 'Lolis'; 

-- SELECT movies.name, movies.rating, GROUP_CONCAT(movie_schedules.time SEPARATOR ', ') time FROM movies JOIN movie_schedules ON movies.movie_id = movie_schedules.movie_id GROUP BY movies.name;