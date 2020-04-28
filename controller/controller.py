from model.model import Model
from view.view import View
import string
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
    
    def start(self):
        self.view.start()
        self.login_user()

    "Login controllers"

    def login_user(self):
        self.view.msg('Introduce tu usuario')
        username = input()
        self.view.msg('Introduce tu contraseña')
        password = input()
        user = self.model.auth_user(username, password)
        self.user_id = user[0]
        if type(user) == tuple:
            self.main_menu(user[3])
        else:
            if user == None:
                self.view.error('El usuario no existe o la contraseña es incorrecta')
            else:
                self.view.error('Error interno')
        return
    "Menus"
    def main_menu(self, isAdmin):
        if not isAdmin:
            o = '0'
            while o != '2':
                self.view.main_menu(isAdmin)
                o = input()
                if o == '1':
                    self.show_schedules()
                elif o == '2':
                    self.buy_ticket_menu()
                elif o == '3':
                    self.view.end()
                else:
                    self.view.not_valid_option()
            return

    def show_schedules(self):
        schedules = self.model.get_schedules_list()
        if type(schedules) == list:
            self.view.show_schedules(schedules)
        else:
            self.view.error('Error interno')
        return
    
    def buy_ticket_menu(self):
        movies = self.model.get_schedules_list()
        self.view.show_movies(movies)
        self.view.msg('Introduce el numero de la pelicula para la que deseas comprar el boleto:')
        number_selected = input()
        movie_selected = movies[int(number_selected)-1][0]

        self.view.msg('Introduce el numero del horario en la que quieres reservar:')
        movie_schedules = movies[int(number_selected)-1][2]
        self.view.show_movie_schedules(movie_schedules)
        number_selected = input()
        schedule_selected = movie_schedules.split(',')[int(number_selected)-1]

        self.view.msg('Introduce el numero de la fecha en la que quieres reservar:')
        next_days = self.model.get_next_days()
        self.view.show_next_days(next_days)
        number_selected = input()
        date_selected = next_days[int(number_selected)-1]

        self.view.msg('Introduce el asiento que quieres reservar, ejemplo: B6')
        schedule_exists = self.model.schedule_exists(date_selected, schedule_selected)
        occupied_seats = ''
        if schedule_exists:
            data = self.model.get_occupied_seats(movie_selected, date_selected, schedule_selected)
            occupied_seats = data[1].split(',')
        else:
            occupied_seats = ['ZZZ',]
        seats = []
        hall_capacity = self.model.get_hall_capacity(movie_selected,schedule_selected.strip())
        for x in range(hall_capacity[0]):
            for y in range(hall_capacity[1]):
                seats.append(f'{string.ascii_lowercase[x].upper()}{y+1}')
        available_seats = [b for b in seats if
            all(a not in b for a in occupied_seats)]
        self.view.msg(', '.join(available_seats))
        seat_selected = '0'
        while seat_selected.upper() not in available_seats:
            seat_selected = input().upper()
            if seat_selected == '0':
                seat_selected = input().upper()
            elif seat_selected.upper() not in available_seats:
                self.view.error('El asiento no está disponible, escoge otro:')
                self.view.msg(', '.join(available_seats))

        if not schedule_exists:
            movie_schedule_id = hall_capacity[2]
            self.model.create_function_schedule(movie_schedule_id, date_selected)
        function_schedule_id = self.model.get_function_schedule_id(movie_selected, date_selected, schedule_selected.strip())
        self.model.create_ticket(function_schedule_id, self.user_id, seat_selected)
        self.view.show_order_details(movie_selected, date_selected, schedule_selected, seat_selected)
        self.view.msg('¡Compraste el boleto de manera exitosa!')