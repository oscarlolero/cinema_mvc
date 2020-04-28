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

    "* Users methods"
    "  * Schedules methods"
    def get_schedules_list(self):
        try:
            sql = 'SELECT movies.name, movies.rating, GROUP_CONCAT(movie_schedules.time SEPARATOR ",") time FROM movies JOIN movie_schedules ON movies.movie_id = movie_schedules.movie_id GROUP BY movies.name'
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except connector.Error as err:
            return err


    "Movie schedules"
    # def get_function_schedule_id(self, movie_selected, schedule_selected):
    #     try:
    #         sql = 'SELECT movie_schedules.movie_schedule_id FROM movie_schedules JOIN movies ON movies.movie_id = movie_schedules.movie_id AND movies.name = %s AND movie_schedules.time = %s'
    #         self.cursor.execute(sql, (movie_selected, schedule_selected))
    #         record = self.cursor.fetchone()
    #         return record
    #     except connector.Error as err:
    #         return err


    "Function schedules"
    def schedule_exists(self, date, time):
        converted_date = datetime.strptime(date, '%d de %B del %Y').strftime('%d-%m-%Y')
        sql = 'SELECT function_schedules.function_schedule_id FROM function_schedules JOIN movie_schedules ON movie_schedules.movie_schedule_id = function_schedules.movie_schedule_id AND function_schedules.date = %s AND movie_schedules.time = %s'
        self.cursor.execute(sql, (converted_date, time))
        record = self.cursor.fetchone()
        print(f'schedule exists? {record} from "{date}", "{time}"')
        return type(record) == tuple

    def get_function_schedule_id(self, movie, date, time):
        converted_date = datetime.strptime(date, '%d de %B del %Y').strftime('%d-%m-%Y')
        print(f'"{movie}", "{date}", "{time}"')
        sql = 'SELECT function_schedules.function_schedule_id FROM function_schedules JOIN movies  ON movies.name = %s  JOIN movie_schedules ON movie_schedules.movie_id = movies.movie_id  AND function_schedules.date = %s AND movie_schedules.time = %s'
        self.cursor.execute(sql, (movie, converted_date, time))
        record = self.cursor.fetchall()
        return record[0][0]

    def create_function_schedule(self, movie_schedule_id, date_selected):
        converted_date = datetime.strptime(date_selected, '%d de %B del %Y').strftime('%d-%m-%Y')
        try:
            print(f'se va a create_function_schedule con movie sch {movie_schedule_id}')
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
            print(f'get occupied seats of "{movie}", "{converted_date}", "{time}"')
            sql = 'SELECT function_schedules.function_schedule_id, GROUP_CONCAT(tickets.seat SEPARATOR ",") as seats FROM tickets JOIN function_schedules ON function_schedules.function_schedule_id = tickets.function_schedule_id JOIN movie_schedules ON movie_schedules.movie_schedule_id = function_schedules.movie_schedule_id JOIN movies ON movies.movie_id = movie_schedules.movie_id AND movies.name = %s AND function_schedules.date = %s AND movie_schedules.time = %s'
            self.cursor.execute(sql, (movie, converted_date, time))
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err

    def create_ticket(self, function_schedule_id, user_id, seat_selected):
        try:
            print(f'se va a crear ticket con func sched {function_schedule_id} y {user_id}, {seat_selected}')
            print(f'tipos {type(function_schedule_id)} y {type(user_id)}, {type(seat_selected)}')
            sql = 'INSERT INTO tickets (`function_schedule_id`, `user_id`, `seat`) VALUES(%s, %s, %s)'
            self.cursor.execute(sql, (function_schedule_id, user_id, seat_selected.upper()))
            print('se ejecuta')
            self.cnx.commit()
            print('se hace commit')
            return True
        except connector.Error as err:
            print('error con ticket')
            print(err)
            return err

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

