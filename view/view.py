class View:
    def start(self):
        print('------------------------------')
        print('Bienvenido al Cine Los Pibes')
        print('------------------------------')

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
        else:
            print('Bienvenido al Cine Los Pibes')
            print('1. Cartelera')
            print('2. Comprar boleto')

    

