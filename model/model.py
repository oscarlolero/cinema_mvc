from mysql import connector

from datetime import datetime, date, time, timedelta 
import locale
locale.setlocale(locale.LC_TIME, '')
class Model:
    def __init__(self, config_db_file='config.txt'):
        self.config_db_file = config_db_file
        self.config_db = self.read_config_db()
        self.connect_to_db()
    
    def read_config_db(self):
        d = {}
        with open(self.config_db_file) as f_r:
            for line in f_r:
                (key, val) = line.strip().split(':')
                d[key] = val
        return d
    
    def connect_to_db(self):
        self.cnx = connector.connect(**self.config_db)
        self.cursor = self.cnx.cursor()
    
    def close_db(self):
        self.cnx.close()
    
    def auth_user(self, username, password):
        sql = 'SELECT * FROM users WHERE username = %s AND password = %s'
        self.cursor.execute(sql, (username, password))
        record = self.cursor.fetchone()
        return record

    "* Admin methods"
    "User granted methods"
    def delete_admin(self, admin):
        try:
            sql = 'DELETE FROM users WHERE username = %s'
            self.cursor.execute(sql, (admin,))
            self.cnx.commit()
            return True
        except connector.Error as err:
            return err

    def get_admins_list(self):
        try:
            sql = 'SELECT username, password FROM users WHERE is_admin = 1'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err

    def add_admin(self, new_user, new_password):
        try:
            sql = 'INSERT INTO users (`username`, `password`, `is_admin`) VALUES(%s, %s, %s)'
            self.cursor.execute(sql, (new_user, new_password, 1))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
    

    "Schedules methods"
    def delete_schedule(self, movie_schedule_id):
        print(movie_schedule_id)
        try:
            sql = 'DELETE FROM movie_schedules WHERE movie_schedule_id = %s'
            self.cursor.execute(sql, (movie_schedule_id,))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
        
    def update_schedule(self, movie_schedule_id, hall_selected, movie_selected, new_schedule):
        try:
            print(movie_schedule_id, hall_selected, movie_selected, new_schedule)
            sql = 'SELECT movies.movie_id FROM movies WHERE name = %s'
            self.cursor.execute(sql, (movie_selected,))
            movie_id = self.cursor.fetchone()[0]
            sql = 'SELECT halls.hall_id FROM halls WHERE name = %s'
            self.cursor.execute(sql, (hall_selected,))
            hall_id = self.cursor.fetchone()[0]

            sql = 'UPDATE movie_schedules SET hall_id = %s, movie_id = %s, time = %s WHERE movie_schedule_id = %s'
            self.cursor.execute(sql, (hall_id, movie_id, new_schedule, movie_schedule_id))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
    def get_detailed_schedules_list(self):
        try:
            sql = 'SELECT movie_schedules.movie_schedule_id,movies.name, halls.name, movie_schedules.time FROM movies JOIN movie_schedules ON movies.movie_id = movie_schedules.movie_id JOIN halls ON halls.hall_id = movie_schedules.hall_id'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err
            
    def get_movie_schedules(self, movie_selected):
        try:
            sql = 'SELECT movies.name, movies.rating FROM movies'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err

    def insert_schedule(self, movie_selected, hall_selected, date):
        try:
            sql = 'SELECT movies.movie_id FROM movies WHERE name = %s'
            self.cursor.execute(sql, (movie_selected,))
            movie_id = self.cursor.fetchone()[0]
            sql = 'SELECT halls.hall_id FROM halls WHERE name = %s'
            self.cursor.execute(sql, (hall_selected,))
            hall_id = self.cursor.fetchone()[0]

            sql = 'INSERT INTO movie_schedules (`hall_id`, `movie_id`, `time`) VALUES(%s, %s, %s)'
            self.cursor.execute(sql, (movie_id, hall_id, date))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err

    "Halls methods"
    def insert_hall(self, new_name, new_x, new_y):
        try:
            sql = 'INSERT INTO halls (`name`, `seats_x`, `seats_y`) VALUES(%s, %s, %s)'
            self.cursor.execute(sql, (new_name, new_x, new_y))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err

    def get_halls_list(self):
        try:
            sql = 'SELECT halls.name, halls.seats_x, halls.seats_y FROM halls'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err

    def update_hall(self, name, new_name, new_seats_x, new_seats_y):
        try:
            sql = 'UPDATE halls SET name = %s, seats_x = %s, seats_y = %s WHERE name = %s'
            self.cursor.execute(sql, (new_name, new_seats_x, new_seats_y, name))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err

    def delete_hall(self, hall):
        try:
            sql = 'DELETE FROM halls WHERE name = %s'
            self.cursor.execute(sql, (hall,))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err

    "Movies methods"
    def get_movies_list(self):
        try:
            sql = 'SELECT movies.name, movies.rating FROM movies'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err

    def update_movie(self, movie_selected, new_name, new_classification):
        try:
            sql = 'UPDATE movies SET name = %s, rating = %s WHERE name = %s'
            self.cursor.execute(sql, (new_name, new_classification, movie_selected))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
    
    def insert_movie(self, new_name, new_classification):
        try:
            sql = 'INSERT INTO movies (`name`, `rating`) VALUES(%s, %s)'
            self.cursor.execute(sql, (new_name, new_classification))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err

    def delete_movie(self, movie):
        try:
            sql = 'DELETE FROM movies WHERE name = %s'
            self.cursor.execute(sql, (movie,))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
    
    "* Users methods"
    "Schedules methods"
    def get_schedules_list(self):
        try:
            sql = 'SELECT movies.name, movies.rating, halls.name, GROUP_CONCAT(movie_schedules.time SEPARATOR ", ") AS time FROM movies JOIN movie_schedules ON movies.movie_id = movie_schedules.movie_id JOIN halls ON movie_schedules.hall_id = halls.hall_id GROUP BY movies.name'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err
    def get_schedules(self):
        try:
            sql = 'SELECT movies.name, movies.rating, GROUP_CONCAT(movie_schedules.time SEPARATOR ", ") AS time FROM movies JOIN movie_schedules ON movies.movie_id = movie_schedules.movie_id GROUP BY movies.name'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err

    "Movie schedules"

    "Function schedules"
    def schedule_exists(self, date, time):
        converted_date = datetime.strptime(date, '%d de %B del %Y').strftime('%d-%m-%Y')
        sql = 'SELECT function_schedules.function_schedule_id FROM function_schedules JOIN movie_schedules ON movie_schedules.movie_schedule_id = function_schedules.movie_schedule_id AND function_schedules.date = %s AND movie_schedules.time = %s'
        self.cursor.execute(sql, (converted_date, time))
        record = self.cursor.fetchone()
        return type(record) == tuple

    def get_function_schedule_id(self, movie, date, time):
        converted_date = datetime.strptime(date, '%d de %B del %Y').strftime('%d-%m-%Y')
        sql = 'SELECT function_schedules.function_schedule_id FROM function_schedules JOIN movies  ON movies.name = %s  JOIN movie_schedules ON movie_schedules.movie_id = movies.movie_id  AND function_schedules.date = %s AND movie_schedules.time = %s'
        self.cursor.execute(sql, (movie, converted_date, time))
        record = self.cursor.fetchall()
        return record[0][0]

    def create_function_schedule(self, movie_schedule_id, date_selected):
        converted_date = datetime.strptime(date_selected, '%d de %B del %Y').strftime('%d-%m-%Y')
        try:
            sql = 'INSERT INTO function_schedules (`movie_schedule_id`, `date`) VALUES(%s, %s)'
            self.cursor.execute(sql, (movie_schedule_id, converted_date))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
    
    "Tickets"
    def get_occupied_seats(self, movie, date, time):
        converted_date = datetime.strptime(date, '%d de %B del %Y').strftime('%d-%m-%Y')
        try:
            sql = 'SELECT function_schedules.function_schedule_id, GROUP_CONCAT(tickets.seat SEPARATOR ",") as seats FROM tickets JOIN function_schedules ON function_schedules.function_schedule_id = tickets.function_schedule_id JOIN movie_schedules ON movie_schedules.movie_schedule_id = function_schedules.movie_schedule_id JOIN movies ON movies.movie_id = movie_schedules.movie_id AND movies.name = %s AND function_schedules.date = %s AND movie_schedules.time = %s'
            self.cursor.execute(sql, (movie, converted_date, time))
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err

    def create_ticket(self, function_schedule_id, user_id, seat_selected):
        try:
            sql = 'INSERT INTO tickets (`function_schedule_id`, `user_id`, `seat`) VALUES(%s, %s, %s)'
            self.cursor.execute(sql, (function_schedule_id, user_id, seat_selected.upper()))
            self.cnx.commit()
            return True
        except connector.Error as err:
            print(err)
            return err
    
    def get_user_tickets(self, user_id):
        sql = 'SELECT movies.name, function_schedules.date, movie_schedules.time, halls.name, GROUP_CONCAT(tickets.seat SEPARATOR ", ") AS seats FROM users JOIN tickets ON users.user_id = tickets.user_id JOIN function_schedules ON tickets.function_schedule_id = function_schedules.function_schedule_id JOIN movie_schedules ON function_schedules.movie_schedule_id = movie_schedules.movie_schedule_id JOIN movies ON movie_schedules.movie_id = movies.movie_id JOIN halls ON movie_schedules.hall_id = halls.hall_id AND users.user_id = %s GROUP BY function_schedules.function_schedule_id ORDER BY function_schedules.date'
        self.cursor.execute(sql, (user_id,))
        records = self.cursor.fetchall()
        return records

    "Halls"
    def get_hall_capacity(self, movie, time):
        sql = 'SELECT halls.seats_x, halls.seats_y, movie_schedules.movie_schedule_id FROM halls JOIN movie_schedules ON movie_schedules.hall_id = halls.hall_id AND movie_schedules.time = %s JOIN movies ON movies.movie_id = movie_schedules.movie_id AND movies.name = %s'
        self.cursor.execute(sql, (time, movie))
        record = self.cursor.fetchone()
        return [record[0], record[1], record[2]]

    "Dates"
    def get_next_days(self):
        today = date.today().strftime('%d de %B del %Y')
        tomorrow = (date.today() + timedelta(days = 1)).strftime('%d de %B del %Y')
        two_days = (date.today() + timedelta(days = 2)).strftime('%d de %B del %Y')
        return [today, tomorrow, two_days]

