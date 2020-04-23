from model.model import Model
from view.view import View
from datetime import date

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
        if type(user) == tuple:
            print(user[3])
            self.view.main_menu(user[3])
        else: 
            if user == None:
                self.view.error('El usuario no existe o la contraseña es incorrecta')
            else:
                self.view.error('Error interno')
        return
