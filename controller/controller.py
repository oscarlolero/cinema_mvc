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
        self.is_admin = user[3]
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
        if isAdmin:
            o = '0'
            while o != '5':
                self.view.main_menu(isAdmin)
                o = input()
                if o == '1':
                    self.movies_menu()
                elif o == '2':
                    self.halls_menu()
                elif o == '3':
                    self.schedules_menu()
                elif o == '4':
                    self.admins_menu()
                elif o == '5':
                    return self.view.end()
                else:
                    self.view.not_valid_option()
            return
        else:
            o = '0'
            while o != '4':
                self.view.main_menu(isAdmin)
                o = input()
                if o == '1':
                    self.show_schedules()
                elif o == '2':
                    self.buy_ticket_menu()
                elif o == '3':
                    self.show_user_tickets(self.user_id)
                elif o == '4':
                    return self.view.end()
                else:
                    self.view.not_valid_option()
            return

    "** Admin methods"
    "Granted users"
    def admins_menu(self):
        o = '0'
        while o == '0':
            self.view.show_admin_methods()
            o = input()
            if o == '1':
                self.show_admins()
            if o == '2':
                self.add_admin()
            elif o == '3':
                self.delete_admin()
            elif o == '4':
                self.main_menu(1)
        return
    def delete_admin(self):
        admins = self.model.get_admins_list()
        self.view.show_indexed_admins(admins)
        self.view.msg('Selecciona un numero de administrador')
        number_selected = input()
        admin_selected = admins[int(number_selected)-1][0]

        result = self.model.delete_admin(admin_selected)
        self.view.success('eliminar administrador') if result else self.view.error('eliminar administrador')

    def show_admins(self):
        admins = self.model.get_admins_list()
        self.view.show_admins(admins)

    def add_admin(self):
        self.view.msg('Introduce el nombre de usuario del administrador')
        new_user = input()
        self.view.msg('Introduce la contraseña del administrador nuevo')
        new_password = input()

        result = self.model.add_admin(new_user, new_password)
        self.view.success('agregar administrador') if result else self.view.error('agregar administrador')
        self.admins_menu()
        
    "Halls"
    def halls_menu(self):
        o = '0'
        while o == '0':
            self.view.show_halls_methods()
            o = input()
            if o == '1':
                self.show_halls()
            if o == '2':
                self.add_hall()
            elif o == '3':
                self.edit_hall()
            elif o == '4':
                self.delete_hall()
            elif o == '5':
                self.main_menu(1)
        return

    def show_halls(self):
        halls = self.model.get_halls_list()
        self.view.show_halls(halls)
        self.halls_menu()

    def add_hall(self):
        self.view.msg('Introduce el nombre de la sala')
        new_name = input()
        self.view.msg('Introduce el numero de columnas de asientos')
        new_x = input()
        self.view.msg('Introduce el numero de filas de asientos')
        new_y = input()

        result = self.model.insert_hall(new_name, new_x, new_y)
        self.view.success('agregar sala') if result else self.view.error('agregar sala')

    def edit_hall(self):
        halls = self.model.get_halls_list()
        self.view.show_halls(halls)
        self.view.msg('Selecciona un numero de sala a editar')
        number_selected = input()
        hall_selected = halls[int(number_selected)-1][0]
        seats_x = halls[int(number_selected)-1][1]
        seats_y = halls[int(number_selected)-1][2]

        self.view.msg('Introduce el nuevo nombre de la sala: (deja en blanco para dejar igual)')
        input_text = input()
        new_name = input_text if input_text != '' else hall_selected
        self.view.msg('Introduce el nuevo numero de columnas: (deja en blanco para dejar igual)')
        input_text = input()
        new_seats_x = input_text if input_text != '' else seats_x
        self.view.msg('Introduce el nuevo numero de filas: (deja en blanco para dejar igual)')
        input_text = input()
        new_seats_y = input_text if input_text != '' else seats_y

        result = self.model.update_hall(hall_selected, new_name, new_seats_x, new_seats_y)
        self.view.success('modificar sala') if result else self.view.error('modificar sala')

    def delete_hall(self):
        halls = self.model.get_halls_list()
        self.view.show_halls(halls)
        self.view.msg('Selecciona un numero de sala a eliminar')
        number_selected = input()
        hall_selected = halls[int(number_selected)-1][0]

        result = self.model.delete_hall(hall_selected)
        self.view.success('eliminar sala') if result else self.view.error('eliminar sala')

    "Schedules"
    def schedules_menu(self):
        o = '0'
        while o == '0':
            self.view.show_schedules_methods()
            o = input()
            if o == '1':
                self.show_schedules()
            if o == '2':
                self.add_schedule()
            elif o == '3':
                self.edit_schedule()
            elif o == '4':
                self.delete_schedule()
            elif o == '5':
                self.main_menu(1)
        return
    def delete_schedule(self):
        movie_schedules = self.model.get_detailed_schedules_list()
        self.view.show_detailed_movie_schedules(movie_schedules)
        self.view.msg('Selecciona el numero de horario a eliminar')
        number_selected = input()
        movie_schedule_id = movie_schedules[int(number_selected)-1][0]
        result = self.model.delete_schedule(movie_schedule_id)
        self.view.success('eliminar horario') if result else self.view.error('eliminar horario')
        self.schedules_menu()
    def add_schedule(self):
        movies = self.model.get_movies_list()
        self.view.show_movies(movies)
        self.view.msg('Introduce el numero de la pelicula a asignar horario')
        number_selected = input()
        movie_selected = movies[int(number_selected)-1][0]
        halls = self.model.get_halls_list()
        self.view.show_halls(halls)
        self.view.msg('Selecciona un numero de sala a asignar horario')
        number_selected = input()
        hall_selected = halls[int(number_selected)-1][0]
        self.view.msg('Introduce un horario a asignar con el formato hh:mm pm/am (ejemplo: 08:10 pm)')
        date = input()
        result = self.model.insert_schedule(movie_selected, hall_selected, date)
        self.view.success('agregar horario') if result else self.view.error('agregar horario')
        self.schedules_menu()
    def edit_schedule(self):
        movie_schedules = self.model.get_detailed_schedules_list()
        self.view.show_detailed_movie_schedules(movie_schedules)
        self.view.msg('Selecciona el numero de horario a editar')
        number_selected = input()
        movie_schedule_id = movie_schedules[int(number_selected)-1][0]
        movie_selected = movie_schedules[int(number_selected)-1][1]
        hall_selected = movie_schedules[int(number_selected)-1][2]
        schedule_selected = movie_schedules[int(number_selected)-1][3]

        movies = self.model.get_movies_list()
        self.view.show_movies(movies)
        self.view.msg('Selecciona un numero de pelicula en caso de querer cambiarla: (deja en blanco para no hacer cambios)')
        input_text = input()
        new_movie = movies[int(input_text)-1][0] if input_text != '' else movie_selected

        halls = self.model.get_halls_list()
        self.view.show_halls(halls)
        self.view.msg('Selecciona un numero de sala nuevo: (deja en blanco para no hacer cambios)')
        input_text = input()
        new_hall = halls[int(input_text)-1][0] if input_text != '' else hall_selected

        self.view.msg('Introduce el horario nuevo: (deja en blanco para no hacer cambios)')
        input_text = input()
        new_schedule = input_text if input_text != '' else schedule_selected

        result = self.model.update_schedule(movie_schedule_id, new_hall, new_movie, new_schedule)
        self.view.success('modificar horario') if result else self.view.error('modificar horario')

    "Movies"
    def movies_menu(self):
        o = '0'
        while o == '0':
            self.view.show_movies_methods()
            o = input()
            if o == '1':
                self.show_movies()
            if o == '2':
                self.add_movie()
            elif o == '3':
                self.edit_movie()
            elif o == '4':
                self.delete_movie()
            elif o == '5':
                self.main_menu(1)
        return

    def show_movies(self):
        movies = self.model.get_movies_list()
        self.view.show_movies(movies)
        self.movies_menu()

    def delete_movie(self):
        movies = self.model.get_movies_list()
        self.view.show_movies(movies)
        self.view.msg('Selecciona un numero de pelicula a eliminar')
        number_selected = input()
        movie_selected = movies[int(number_selected)-1][0]

        result = self.model.delete_movie(movie_selected)
        self.view.success('eliminar película') if result else self.view.error('eliminar película')

    def add_movie(self):
        self.view.msg('Introduce el nombre de la pelicula')
        new_name = input()
        self.view.msg('Introduce la clasificacion de la pelicula')
        new_classification = input()

        result = self.model.insert_movie(new_name, new_classification)
        self.view.success('agregar película') if result else self.view.error('agregar película')

    def edit_movie(self):
        movies = self.model.get_movies_list()
        self.view.show_movies(movies)
        self.view.msg('Selecciona un numero de pelicula a editar')
        number_selected = input()
        movie_selected = movies[int(number_selected)-1][0]
        movie_classification = movies[int(number_selected)-1][1]

        self.view.msg('Introduce el nuevo nombre de la pelicula: (deja en blanco para dejar igual)')
        input_text = input()
        new_name = input_text if input_text != '' else movie_selected
        self.view.msg('Introduce la nueva clasificacion de la pelicula: (deja en blanco para dejar igual)')
        input_text = input()
        new_classification = input_text if input_text != '' else movie_classification
        result = self.model.update_movie(movie_selected, new_name, new_classification)
        self.view.success('modificar película') if result else self.view.error('modificar película')

    "User methods"
    def show_schedules(self):
        schedules = self.model.get_schedules_list()
        if type(schedules) == list:
            self.view.show_schedules(schedules)
        else:
            self.view.error('Error interno')
        return
    
    def buy_ticket_menu(self):
        movies = self.model.get_schedules()
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
        self.view.msg('¡Compraste el boleto de manera exitosa!, presiona cualquier tecla para continuar.')
        tmp = input()
        self.main_menu(self.is_admin)

    def show_user_tickets(self, user_id):
        user_tickets = self.model.get_user_tickets(user_id)
        self.view.msg('A continuación se muestran tus boletos reservados:')
        self.view.show_user_tickets(user_tickets)