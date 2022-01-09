import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from authorization_disgn import *
import sqlite3


def main():
    # создаём приложение и запускаем его
    app = QApplication(sys.argv)
    ex = Authorization()
    ex.show()
    app.exec_()


class Authorization(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_sign_in.clicked.connect(self.run)
        self.ui.btn_sign_up.clicked.connect(self.run)
        self.name = ''
        self.Flag1 = False
        self.Flag2 = False
        f = open('status_start_game.txt', 'w')
        f.write('False')
        f.close()

    def run(self):  # получаем сигнал от кнопок
        # поверяем что пользователь ввёл данные
        # запускаем аунтефикацию или регистрацию
        if self.ui.line_login.text() != '' or self.ui.line_password.text() != '':
            if self.sender().text() == 'Sign in':
                self.auth()
            else:
                self.reg()

    def closed(self):  # если условие верно то
        # закрываем окно авторизации
        if self.Flag1 is True and self.Flag2 is True:
            f = open('status_start_game.txt', 'w')
            f.write('True')
            f.close()
            QApplication.quit()

    def signal_handler(self, value):  # выводим на экран нужные оповещения
        QMessageBox.about(self, 'Оповещение', value)
        self.Flag2 = True
        self.closed()

    def auth(self):  # собираем информацию для аунтефикации
        name = self.ui.line_login.text()
        password = self.ui.line_password.text()
        self.login(name, password)

    def reg(self):  # собираем информацию для регистрации
        name = self.ui.line_login.text()
        password = self.ui.line_password.text()
        self.register(name, password)

    def login(self, login, password):  # ищем пользователя в системе
        # если находим то разрешаем вход иначе не разрешаем
        con = sqlite3.connect("data/database/users.db")
        cur = con.cursor()
        cur.execute(f'SELECT * FROM user WHERE login="{login}";')
        value = cur.fetchall()
        cur.close()
        con.close()

        if value != [] and value[0][2] == password:
            self.Flag1 = True
            self.name = login
            self.signal_handler('Успешная авторизация!')
        else:
            self.signal_handler('Проверте правильность ввода данных')

    def register(self, log, pas):  # регистрируем пользователя в системе
        con = sqlite3.connect("data/database/users.db")
        cur = con.cursor()
        cur.execute(f'SELECT * FROM user WHERE login="{log}";')
        value = cur.fetchall()
        if value != []:
            self.signal_handler('Такой ник уже используется')
        else:
            cur.execute(f"INSERT INTO user(login,password) VALUES ('{log}', '{pas}')")
            self.signal_handler('Вы успешно зарегистрированны!')
            self.name = log
            con.commit()
        cur.close()
        con.close()

main()
