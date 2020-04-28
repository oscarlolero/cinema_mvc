from prettytable import PrettyTable


class View:
    def start(self):
        print('------------------------------')
        print('Bienvenido al Cine Los Pibes')
        print('------------------------------')

    def end(self): 
        print('Saliendo...')

    def msg(self, output):
        print(output)

    def error(self, err):
        print('ERROR: '+ err)

    def main_menu(self, is_admin):
        if is_admin:
            print('Bienvenido al panel de administracion')
            print('1. Peliculas')
            print('2. Salas')
            print('3. Horarios')
            print('4. Administradores')
            print('5. Salir')
            self.option('5')
        else:
            print('Bienvenido al Cine Los Pibes')
            print('1. Cartelera')
            print('2. Comprar boleto')
            print('3. Salir')
            self.option('3')

    def option(self, last):
        print('Selecciona una opcion (1-'+last+'):', end = '')

    "Users methods"
    "Schedules"

    def show_schedules(self, schedules):
        table = PrettyTable(['Pelicula', 'Clasificacion', 'Horarios'])
        for schedule in schedules:
            table.add_row([schedule[0], schedule[1], schedule[2]])
        print(table)

    "Movies methods"
    def show_movies(self, movies):
        table = PrettyTable(['Numero', 'Pelicula', 'Clasificacion'])
        index = 1
        for movie in movies:
            table.add_row([index, movie[0], movie[1]])
            index += 1
        print(table)

    def show_next_days(self, next_days):
        table = PrettyTable(['Numero', 'Fecha'])
        table.add_row([1, next_days[0]])
        table.add_row([2, next_days[1]])
        table.add_row([3, next_days[2]])
        print(table)

    def show_movie_schedules(self, movie_schedules):
        schedules_array = movie_schedules.split(',')
        table = PrettyTable(['Numero', 'Horario'])
        index = 1
        for schedule in schedules_array:
            table.add_row([index, schedule])
            index += 1
        print(table)
    
    "Tickets"
    def show_order_details(self, movie_selected, date_selected, schedule_selected, seat_selected):
        table = PrettyTable(['Dato', 'Descripción'])
        table.add_row(['Película:', movie_selected])
        table.add_row(['Fecha:', date_selected])
        table.add_row(['Hora:', schedule_selected])
        table.add_row(['Asiento:', seat_selected])
        print(table)


