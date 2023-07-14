import sys
import os
import sqlite3
from os import walk, system

try:
    from PyQt5 import uic, QtCore
    from PIL.ImageQt import ImageQt
    from PIL import Image, ImageDraw, ImageFont
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QInputDialog
    from PyQt5.QtGui import QPixmap
except ModuleNotFoundError:
    system("pip install -r requirements.txt")
    from PyQt5 import uic, QtCore
    from PIL.ImageQt import ImageQt
    from PIL import Image, ImageDraw, ImageFont
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QInputDialog
    from PyQt5.QtGui import QPixmap

id_null = 0
lvl_null = 0
login_null = 0
password_null = 0
name_null = 0


class Intro(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/intro.ui', self)


class Menu(QWidget):
    def __init__(self):
        global id_null

        self.praise = None
        self.logiin = None
        self.lvvl = None
        self.hi = None
        self.pic = None
        self.userpic = None
        self.change = None

        super().__init__()
        uic.loadUi('designs/menu.ui', self)

        self.change.clicked.connect(self.change_password)
        self.userpic.clicked.connect(self.change_userpic)
        self.conn = sqlite3.connect('rabochka/persons.db')

        self.cur = self.conn.cursor()
        self.picture = self.cur.execute(f'''SELECT avatarka FROM menu WHERE idshka = {id_null}''').fetchall()

        if self.picture[0][0] is not None and self.picture[0][0] != '1':
            img = Image.open(self.picture[0][0])
            img_clone = ImageQt(img)
            pixmap = QPixmap.fromImage(img_clone)
            self.pic.setPixmap(pixmap)
        else:
            img = Image.open('rabochka/kot_spit.jpg')
            img_clone = ImageQt(img)
            pixmap = QPixmap.fromImage(img_clone)
            self.pic.setPixmap(pixmap)

        self.text_in_menu()

    def change_userpic(self):
        global id_null

        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            img = Image.open(fname)

            size = 250, 250
            img.thumbnail(size, Image.Resampling.LANCZOS)

            img.save(f'rabochka/avatars/{id_null}.png')

            self.cur.execute(f'''UPDATE menu SET avatarka = 
            'rabochka/avatars/{id_null}.png' WHERE idshka = {id_null}''')
            self.conn.commit()

            img_clone = ImageQt(img)
            pixmap = QPixmap.fromImage(img_clone)
            self.pic.setPixmap(pixmap)
        except:
            img = Image.open('rabochka/kot_spit.jpg')
            img_clone = ImageQt(img)
            pixmap = QPixmap.fromImage(img_clone)
            self.pic.setPixmap(pixmap)

    def text_in_menu(self):
        global id_null, lvl_null, login_null, password_null, name_null

        _translate = QtCore.QCoreApplication.translate
        self.hi.setText(_translate('MainWindow',
                                       f'<html><head/><body><p align="center"><span style=" font-size:24pt; '
                                       f'font-weight:600;">Привет, {name_null}!</span></p></body></html>'))
        self.lvvl.setText(_translate('MainWindow',
                                    f'<html><head/><body><p><span style=" font-size:9pt; font-weight:600;'
                                    f'">Твой уровень: {lvl_null}</span></p></body></html>'))
        self.logiin.setText(_translate('MainWindow',
                                      f'<html><head/><body><p><span style=" font-size:9pt; font-weight:600;'
                                      f'">Твой логин: {login_null}</span></p></body></html>'))
        if lvl_null < 10:
            file = open('text/lvl1.txt', mode='r', encoding="utf-8")

        elif 10 <= lvl_null < 50:
            file = open('text/lvl2.txt', mode='r', encoding="utf-8")

        else:
            file = open('text/lvl3.txt', mode='r', encoding="utf-8")

        text_from_file = file.read()
        self.praise.setText(_translate('MainWindow',
                                       f'<html><head/><body><p><span style=" font-size:9pt; font-weight:600;'
                                       f'">{text_from_file}</span></p></body></html>'))

    def change_password(self):
        chng = Change_password()
        chng.show()
        self.close()


class Change_password(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/chng.ui', self)

        self.save.clicked.connect(self.change_password)

    def change_password(self):
        if self.pswrd1.toPlainText() == self.pswrd2.toPlainText():
            conn = sqlite3.connect('rabochka/persons.db')
            cur = conn.cursor()

            if self.pswrd1.toPlainText() == '' or self.pswrd2.toPlainText() == '':
                QMessageBox.critical(self, "А ты шутник", "Вы ничего не ввели в поле", QMessageBox.Ok)

            else:
                cur.execute(f'''UPDATE users SET parol = {self.pswrd2.toPlainText()} WHERE idshka = {id_null}''')
                conn.commit()

                QMessageBox.critical(self, "Готово!", "Пароль был изменен", QMessageBox.Ok)

                menu = Menu()
                menu.show()
                self.close()
        else:
            QMessageBox.critical(self, "Упс!", "Пароли не совпадают", QMessageBox.Ok)


class Registr(QWidget):
    def __init__(self):
        super().__init__()

        self.login = None
        self.name = None
        self.ok = None
        self.backk = None
        self.paswrd = None
        self.paswrd_2 = None

        uic.loadUi('designs/regg.ui', self)

        self.ok.clicked.connect(self.user_reg)
        self.backk.clicked.connect(self.back)

        self.main = Main()

    def back(self):  # Вернуться назад
        self.main.login()
        self.close()

    def user_reg(self):  # Регистрация пользователя
        if self.paswrd.toPlainText() == self.paswrd_2.toPlainText():

            conn = sqlite3.connect('rabochka/persons.db')  # База данных
            cur = conn.cursor()
            result = cur.execute(f'''SELECT idshka FROM users''').fetchall()
            logins = cur.execute(f'''SELECT login FROM users''').fetchall()
            log = []
            for elem in logins:
                log.append(*elem)

            # Проверка на наличие веденного текста в полях
            if self.login.toPlainText() == '' or self.paswrd.toPlainText() == '' or self.name.toPlainText() == '':
                QMessageBox.critical(self, "А ты шутник", "Вы ничего не ввели в поле", QMessageBox.Ok)

            elif self.login.toPlainText() not in log:
                try:
                    cur.execute(f'''INSERT INTO users(login,parol,idshka,name)
                    VALUES('{self.login.toPlainText()}','{self.paswrd.toPlainText()}',{int(*result[-1]) + 1},
                     '{self.name.toPlainText()}')''')
                    cur.execute(f'''INSERT INTO levels(id,lvl) VALUES({int(*result[-1]) + 1},1)''')
                    cur.execute(f'''INSERT INTO menu(idshka,avatarka) VALUES({int(*result[-1]) + 1},'1')''')

                except:
                    cur.execute(f'''INSERT INTO users(login,parol,idshka,name)
                    VALUES('{self.login.toPlainText()}','{self.paswrd.toPlainText()}',1,'{self.name.toPlainText()}')''')
                    cur.execute(f'''INSERT INTO levels(id,lvl)
                                                    VALUES(1,1)''')
                    cur.execute(f'''INSERT INTO menu(idshka,avatarka) VALUES(1,'1')''')

                QMessageBox.critical(self, "Готово!", "Поздравляю с регистрацией!", QMessageBox.Ok)
                conn.commit()

                self.main.login()
                self.close()
            else:
                QMessageBox.critical(self, "Кудааааа", "Такой пользователь уже есть!", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Упс!", "Пароли не совпадают", QMessageBox.Ok)


class Loginn(QWidget):
    def __init__(self):
        super().__init__()

        self.login = None
        self.regist = None
        self.main = None
        self.loginn = None
        self.passwordd = None

        uic.loadUi('designs/log.ui', self)

        self.login.clicked.connect(self.checck)


    def checck(self):
        global id_null, lvl_null, login_null, password_null, name_null

        conn = sqlite3.connect('rabochka/persons.db')  # База данных
        cur = conn.cursor()
        logins = cur.execute(f'''SELECT login FROM users''').fetchall()
        passwords = cur.execute(f'''SELECT login,parol FROM users''').fetchall()
        ids = cur.execute(f'''SELECT idshka FROM users''').fetchall()
        names = cur.execute(f'''SELECT name FROM users''').fetchall()
        lvls = cur.execute(f'''SELECT lvl FROM levels''').fetchall()
        log = []
        for elem in logins:
            log.append(*elem)

        if self.loginn.toPlainText() not in log:  # Проверка на наличие веденных данных в базе
            QMessageBox.critical(self, "Кудааааа", "Такого пользователя нет", QMessageBox.Ok)

        elif (self.loginn.toPlainText(), self.passwordd.toPlainText()) not in passwords:
            QMessageBox.critical(self, "Кудааааа", "Пароль не правильный)))", QMessageBox.Ok)

        elif (self.loginn.toPlainText(), self.passwordd.toPlainText()) in passwords:  # Вход в аккаунт
            self.main = Main()

            id_null = ids[passwords.index((self.loginn.toPlainText(), self.passwordd.toPlainText()))][0]
            lvl_null = lvls[passwords.index((self.loginn.toPlainText(), self.passwordd.toPlainText()))][0]
            login_null = self.loginn.toPlainText()
            password_null = self.passwordd.toPlainText()
            name_null = names[passwords.index((self.loginn.toPlainText(), self.passwordd.toPlainText()))][0]

            self.close()
            self.main.show()


class Library(QWidget):
    def __init__(self):
        super().__init__()

        self.choose = None

        uic.loadUi('designs/sbl.ui', self)

        self.main = Main()

        self.choose.clicked.connect(self.choose_mem)

        self.flag = False

    def choose_mem(self):
        self.f1 = self.pic1.isChecked()
        self.f2 = self.pic2.isChecked()
        self.f3 = self.pic3.isChecked()
        self.f4 = self.pic4.isChecked()
        self.f5 = self.pic5.isChecked()
        self.f6 = self.pic6.isChecked()

        if self.f1:
            self.main.lib_pic = 'sbln/1.jpg'
            self.flag = True
        elif self.f2:
            self.main.lib_pic = 'sbln/2.jpg'
            self.flag = True
        elif self.f3:
            self.main.lib_pic = 'sbln/3.jpg'
            self.flag = True
        elif self.f4:
            self.main.lib_pic = 'sbln/4.jpg'
            self.flag = True
        elif self.f5:
            self.main.lib_pic = 'sbln/5.jpg'
            self.flag = True
        elif self.f6:
            self.main.lib_pic = 'sbln/6.jpg'
            self.flag = True

        else:
            QMessageBox.critical(self, "Эм", "Вы не выбрали шаблон", QMessageBox.Ok)

        if self.flag:
            self.main.show()
            self.main.flag_for_template = True
            self.main.paste_pic()
            self.close()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.demotivator = None
        self.name2 = "None"
        self.name1 = "None"
        self.paste_pic = None
        self.save = None
        self.degree_pic = None
        self.size_pic = None
        self.visibility = None
        self.save_action = None
        self.button_ok = None
        self.degree_text = None
        self.size_text = None
        self.paste_text = None
        self.library = None
        self.pic = None
        self.meme = None
        self.logg = None
        self.regg = None
        self.intro = None
        self.lib_pic = None

        uic.loadUi('designs/main.ui', self)

        self.conn = sqlite3.connect('rabochka/persons.db')
        self.cur = self.conn.cursor()

        self.pic.clicked.connect(self.choose_pic)
        self.library.clicked.connect(self.show_library)
        self.paste_text.clicked.connect(self.ask_text)
        self.paste_pic.clicked.connect(self.ask_pic)
        self.demotivator.clicked.connect(self.create_demotivator)
        self.save.clicked.connect(self.save_meme)
        self.save_action.clicked.connect(self.flagok)
        self.menu.clicked.connect(self.show_menu)

        self.save_action.hide()

        self.x1 = 30
        self.y1 = 30
        self.flag_text = True
        self.flag_pic = True
        self.flag_dmtvtr = True
        self.flag_action = True

        # Функции для редактирования текста
        self.size_text.valueChanged[int].connect(self.change_size_text)
        self.size_text_null = 18

        self.degree_text.valueChanged[int].connect(self.change_degree_text)
        self.degree_text_null = 0

        self.font.currentTextChanged.connect(self.change_font)
        self.font_null = 'Arial.ttf'

        # Функции для редактирования картинок
        self.size_pic.valueChanged[int].connect(self.change_size_pic)
        self.size_pic_null = 40

        self.degree_pic.valueChanged[int].connect(self.change_degree_pic)
        self.degree_pic_null = 0

        self.visibility.valueChanged.connect(self.change_visibility)
        self.visibility_null = 255

        self.flag_for_combbox = True
        self.flag_for_template = False

    def flagok(self):
        self.flag_text = True
        self.flag_pic = True
        if self.flag_dmtvtr is False:
            self.flag_dmtvtr = True
            self.width, self.height = self.img.size
        self.flag_action = True
        self.button_ok.hide()
        self.save_action.show()
        try:
            self.img = self.back.copy()
        except:
            None

    def combbox(self):
        global lvl_null
        listt = []

        for (dirpath, dirnames, filenames) in walk('shrifts/'):
            listt.extend(filenames)
            break

        if self.flag_for_combbox:
            if lvl_null < 10:
                self.font.addItems(listt[:3])
                self.flag_for_combbox = False
            elif lvl_null >= 10 and lvl_null < 50:
                self.font.addItems(listt[:6])
                self.flag_for_combbox = False
            else:
                self.font.addItems(listt[:15])
                self.flag_for_combbox = False

    def mousePressEvent(self, event):
        self.x1 = event.x()
        self.y1 = event.y()
        if self.flag_text is False:
            self.pst_text()
        if self.flag_pic is False:
            self.pst_pic()

    def save_meme(self):
        global id_null, lvl_null

        name, ok = QInputDialog.getText(self, "Имя файла", "Как назвать файл?")

        try:
            if name:
                self.img.save(f'mem/{name}.png')
                QMessageBox.critical(self, "Ура", f'Мем сохранен в папке .../memcreator/mem/{name}.png',
                                     QMessageBox.Ok)
            else:
                self.img.save('mem/Вы_не_ввели_название.png')
                QMessageBox.critical(self, "Ура", 'Мем сохранен в папке .../memcreator/mem/Вы_не_ввели_название.png',
                                     QMessageBox.Ok)
            lvl_null += 1

            self.cur.execute(f'''UPDATE levels SET lvl = {lvl_null} WHERE id = {id_null}''')
            self.conn.commit()
            _translate = QtCore.QCoreApplication.translate
        except:
            _translate = QtCore.QCoreApplication.translate
            self.meme.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                          font-weight:600;\">Ой, нет мема! Нечего сохранять</span></p></body></html>"))

    def choose_pic(self):  # Выбрать стоковую картинку для редактирования
        global lvl_null, id_null
        try:
            if self.flag_for_template:
                self.fname = self.lib_pic
                self.flag_for_template = False

            elif self.flag_for_template is False:
                self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

            self.img = Image.open(self.fname)

            self.size = 400, 400
            self.img.thumbnail(self.size, Image.Resampling.LANCZOS)
            self.width, self.height = self.img.size

            self.img_clone = ImageQt(self.img)
            self.pixmap = QPixmap.fromImage(self.img_clone)
            self.meme.setPixmap(self.pixmap)
        except:
            _translate = QtCore.QCoreApplication.translate
            self.meme.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                          font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def ask_text(self):  # Получение текста
        if self.flag_action:
            self.text_mem, self.ok_pressed = QInputDialog.getText(self, "Текст", "Введите текст")
            self.combbox()
            self.pst_text()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака",
                                 QMessageBox.Ok)

    def change_size_text(self, value):  # Изменение размера текста
        if self.flag_text is False:
            self.size_text_null = (value + 1) * 4
            self.pst_text()

    def change_degree_text(self):  # Изменение градуса наклона текста
        if self.flag_text is False:
            self.degree_text_null = 360 - int(self.degree_text.value())
            self.pst_text()

    def change_font(self):  # Изменение шрифта текста
        if self.flag_text is False:
            self.font_null = str(self.font.currentText())
            self.pst_text()

    def pst_text(self):  # Внесение изменений (работа текста)
        if self.ok_pressed:
            try:
                self.back = self.img.copy()  # Копия

                name = self.text_mem

                font = ImageFont.truetype(font=f'shrifts/{self.font_null}', size=self.size_text_null)
                line_height = sum(font.getmetrics())

                fontimage = Image.new('L', (font.getsize(name)[0], line_height))
                x, y = fontimage.size
                ImageDraw.Draw(fontimage).text((0, 0), name, fill=255, font=self.font)
                fontimage = fontimage.rotate(self.degree_text_null, resample=Image.BICUBIC, expand=True)

                x = self.x1 - 30 - (x // 2)
                y = self.y1 - 30 - ((400 - self.height) // 2) - (y // 2)

                self.button_ok.show()
                self.save_action.hide()

                for i in range(3):
                    self.back.paste((0, 0, 0), (x - i, y), mask=fontimage)
                    self.back.paste((0, 0, 0), (x + i, y), mask=fontimage)
                    self.back.paste((0, 0, 0), (x, y + i), mask=fontimage)
                    self.back.paste((0, 0, 0), (x, y - i), mask=fontimage)
                    self.back.paste((0, 0, 0), (x - i, y + i), mask=fontimage)
                    self.back.paste((0, 0, 0), (x + i, y + i), mask=fontimage)
                    self.back.paste((0, 0, 0), (x - i, y - i), mask=fontimage)
                    self.back.paste((0, 0, 0), (x + i, y - i), mask=fontimage)
                self.back.paste((255, 255, 255), (x, y), mask=fontimage)

                img_clone = ImageQt(self.back)
                pixmap = QPixmap.fromImage(img_clone)
                self.meme.setPixmap(pixmap)

                self.flag_text = False
                self.flag_action = False
            except:
                _translate = QtCore.QCoreApplication.translate
                self.meme.setText(_translate("MainWindow",
                                             "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                              font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def ask_pic(self):
        if self.flag_action:
            self.fname_1 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.pst_pic()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака",
                                 QMessageBox.Ok)

    def change_size_pic(self, value):
        if self.flag_pic is False:
            self.size_pic_null = (value + 1) * 4
            self.pst_pic()

    def change_degree_pic(self):
        if self.flag_pic is False:
            self.degree_pic_null = 360 - int(self.degree_pic.value())
            self.pst_pic()

    def change_visibility(self):
        if self.flag_pic is False:
            self.visibility_null = int(self.visibility.value())
            self.pst_pic()

    def pst_pic(self):
        try:
            self.back = self.img.copy()
            pic = Image.open(self.fname_1)

            size_1 = self.size_pic, self.size_pic
            pic.thumbnail(size_1, Image.Resampling.LANCZOS)

            pic = pic.rotate(self.degree_pic_null, resample=Image.Resampling.BICUBIC, expand=True,
                             fillcolor=(0, 0, 255))

            rgba = pic.convert("RGBA")
            dat = rgba.getdata()
            newdata = []
            for item in dat:
                if item[0] == 0 and item[1] == 0 and item[2] == 255:
                    newdata.append((255, 255, 255, 0))
                else:
                    newdata.append((item[0], item[1], item[2], self.visibility_null))
            rgba.putdata(newdata)
            rgba.save("rabochka/transparent_image.png", "PNG")

            pic = Image.open('rabochka/transparent_image.png', 'r')

            width, height = pic.size
            x = self.x1 - 30 - (width // 2)
            y = self.y1 - 30 - ((400 - self.height) // 2) - (height // 2)
            coord = (x, y)

            self.button_ok.show()
            self.save_action.hide()

            self.back.paste(pic, coord, mask=self.pic)

            img_clone = ImageQt(self.back)
            pixmap = QPixmap.fromImage(img_clone)
            self.meme.setPixmap(pixmap)

            self.flag_pic = False
            self.flag_action = False

            os.remove("rabochka/transparent_image.png")
        except:
            _translate = QtCore.QCoreApplication.translate
            self.meme.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                          font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def create_demotivator(self):
        if self.flag_action:
            self.name1, o = QInputDialog.getText(self, "Введите заголовок", "пиши")
            self.create_demotivator_step2()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def create_demotivator_step2(self):
        if self.flag_action:
            self.name2, o = QInputDialog.getText(self, "Текст", "Введите текст")
            self.create_demotivator_step3()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def create_demotivator_step3(self):
        try:
            width, height = self.img.size

            font = ImageFont.truetype(f'shrifts/Times_new_roman.ttf', size=30)
            line_height1 = sum(font.getmetrics())
            fontimage1 = Image.new('L', (font.getsize(self.name1)[0], line_height1))
            x, y = fontimage1.size
            ImageDraw.Draw(fontimage1).text((0, 0), self.name1, fill=255, font=font)

            font1 = ImageFont.truetype(f'shrifts/Arial.ttf', size=15)
            line_height = sum(font1.getmetrics())
            fontimage = Image.new('L', (font1.getsize(self.name2)[0], line_height))
            x1, y1 = fontimage.size
            ImageDraw.Draw(fontimage).text((0, 0), self.name2, fill=255, font=font1)

            dmtvtr = Image.new('RGBA', (width + 50, height + 10 + y + 15 + y1 + 40), 'black')
            idraw = ImageDraw.Draw(dmtvtr)

            idraw.rectangle((20, 20, width + 30, height + 30), fill='white')
            idraw.rectangle((23, 23, width + 27, height + 27), fill='black')

            dmtvtr.paste((255, 255, 255), ((width + 50 - x) // 2, (height + 40)),
                         mask=fontimage1)
            dmtvtr.paste((255, 255, 255), ((width + 50 - x1) // 2, (height + 40 + y + 10)),
                         mask=fontimage)
            dmtvtr.paste(self.img, (25, 25))

            dmtvtr.thumbnail(self.size, Image.Resampling.LANCZOS)

            self.button_ok.show()
            self.save_action.hide()

            self.flag_action = False
            self.flag_dmtvtr = False

            self.back = dmtvtr.copy()

            img_copy = ImageQt(self.back)
            pixmap = QPixmap.fromImage(img_copy)
            self.meme.setPixmap(pixmap)
        except:
            _translate = QtCore.QCoreApplication.translate
            self.meme.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                          font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def show_menu(self):
        self.menu = Menu()
        self.menu.show()

    def show_library(self):
        self.lib = Library()

        self.lib.show()
        self.close()

    def show_intro(self):  # Показ начального экрана (заставка, интро)
        self.intro = Intro()

        self.intro.pushButton.clicked.connect(self.intro.close)  # Реакции на нажатие кнопок
        self.intro.pushButton.clicked.connect(self.login)  # При нажатии кнопки открывает логин

        self.intro.show()

    def login(self):
        self.logg = Loginn()
        self.regg = Registr()

        self.logg.regist.clicked.connect(self.regg.show)  # Реакции на нажатие кнопок
        self.logg.regist.clicked.connect(self.logg.close)

        self.logg.show()


if __name__ == '__main__':  # Запуск приложения
    app = QApplication(sys.argv)
    ex = Main()
    ex.show_intro()
    sys.exit(app.exec_())
