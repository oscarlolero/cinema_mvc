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

    def main_menu(self, is_admin):
        if is_admin:
            print('Bienvenido al panel de administración')
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
            print('3. Ver mis boletos')
            print('4. Salir')
            self.option('4')

    def option(self, last):
        print('Selecciona una opcion (1-'+last+'):', end = '')

    def success(self, operation):
        print(f'Operación "{operation}" realizada con éxito.')
    
    def error(self, operation):
        print(f'Hubo un error en la operación "{operation}".')

    
    "** Admin methods"

    "Schedule methods"
    def show_schedules_methods(self):
        print('Menú de horarios')
        print('1. Ver todos los horarios')
        print('2. Agregar horario')
        print('3. Editar horario')
        print('4. Eliminar horario')
        print('5. Regresar')
        self.option('5')
    
    "Halls methods"
    def show_halls_methods(self):
        print('Menú de salas')
        print('1. Ver todas las salas')
        print('2. Agregar sala')
        print('3. Editar sala')
        print('4. Eliminar sala')
        print('5. Regresar')
        self.option('5')
    
    def show_halls(self, halls):
        table = PrettyTable(['Numero', 'Nombre', 'Columnas', 'Filas'])
        index = 1
        for hall in halls:
            table.add_row([index, hall[0], hall[1], hall[2]])
            index += 1
        print(table)
    "Movies methods"
    def show_movies_methods(self):
        print('Menú de películas')
        print('1. Ver todas las películas')
        print('2. Agregar película')
        print('3. Editar película')
        print('4. Eliminar película')
        print('5. Regresar')
        self.option('5')

    "** Users methods"
    "Schedules"
    def show_detailed_movie_schedules(self, movie_schedules):
        table = PrettyTable(['Numero', 'Pelicula', 'Clasificacion', 'Horario'])
        index = 1
        for movie in movie_schedules:
            table.add_row([index, movie[1], movie[2], movie[3]])
            index += 1
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
    
    def show_user_tickets(self, tickets):
        table = PrettyTable(['Película', 'Fecha', 'Hora', 'Sala', 'Asientos'])
        for ticket in tickets:
            table.add_row([ticket[0], ticket[1], ticket[2], ticket[3], ticket[4],])
        print(table)


