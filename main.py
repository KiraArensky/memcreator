import sys
import os
import sqlite3
from os import walk
from PyQt5 import uic, QtCore
from PIL.ImageQt import ImageQt
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap

id = 0
lvl = 0
logiin = 0
password = 0
namee = 0


class Zastavka(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/vkl.ui', self)


class Menu(QWidget):
    def __init__(self):
        global id

        super().__init__()
        uic.loadUi('designs/menu.ui', self)

        self.smen_prl.clicked.connect(self.smena_password)
        self.avatarka.clicked.connect(self.smen_avatar)
        self.conn = sqlite3.connect('rabochka/persons.db')

        self.cur = self.conn.cursor()
        self.avatr = self.cur.execute(f'''SELECT avatarka FROM menu WHERE idshka = {id}''').fetchall()

        if self.avatr[0][0] != None and self.avatr[0][0] != '1':
            self.img = Image.open(self.avatr[0][0])
            self.a = ImageQt(self.img)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)
        else:
            self.img = Image.open('rabochka/kot_spit.jpg')
            self.a = ImageQt(self.img)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)

        self.text_v_menu()

    def smen_avatar(self):
        global id

        try:
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.img = Image.open(self.fname)

            self.size = 250, 250
            self.img.thumbnail(self.size, Image.Resampling.LANCZOS)

            self.img.save(f'rabochka/avatars/{id}.png')

            self.cur.execute(f'''UPDATE menu SET avatarka = 'rabochka/avatars/{id}.png' WHERE idshka = {id}''')
            self.conn.commit()

            self.a = ImageQt(self.img)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)
        except:
            self.img = Image.open('rabochka/kot_spit.jpg')
            self.a = ImageQt(self.img)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)

    def text_v_menu(self):
        global id, lvl, logiin, password, namee

        _translate = QtCore.QCoreApplication.translate
        self.privet.setText(_translate('MainWindow',
                                       f'<html><head/><body><p align="center"><span style=" font-size:24pt; '
                                       f'font-weight:600;">Привет, {namee}!</span></p></body></html>'))
        self.lvl.setText(_translate('MainWindow',
                                    f'<html><head/><body><p><span style=" font-size:9pt; font-weight:600;'
                                    f'">Твой уровень: {lvl}</span></p></body></html>'))
        self.login.setText(_translate('MainWindow',
                                      f'<html><head/><body><p><span style=" font-size:9pt; font-weight:600;'
                                      f'">Твой логин: {logiin}</span></p></body></html>'))
        if lvl < 10:
            file = open('text/lvl1.txt', mode='r', encoding="utf-8")

        elif lvl >= 10 and lvl < 50:
            file = open('text/lvl2.txt', mode='r', encoding="utf-8")

        elif lvl >= 50:
            file = open('text/lvl3.txt', mode='r', encoding="utf-8")

        text_from_file = file.read()
        self.pohvala.setText(_translate('MainWindow',
                                        f'<html><head/><body><p><span style=" font-size:9pt; font-weight:600;'
                                        f'">{text_from_file}</span></p></body></html>'))

    def smena_password(self):
        self.smn = Smena_prl()
        self.smn.show()
        self.close()


class Smena_prl(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/chng.ui', self)

        self.sohr.clicked.connect(self.change_password)

    def change_password(self):
        if self.prl1.toPlainText() == self.prl2.toPlainText():
            conn = sqlite3.connect('rabochka/persons.db')
            cur = conn.cursor()

            if self.prl1.toPlainText() == '' or self.prl2.toPlainText() == '':
                QMessageBox.critical(self, "А ты шутник", "Вы ничего не ввели в поле", QMessageBox.Ok)

            else:
                cur.execute(f'''UPDATE users SET parol = {self.prl2.toPlainText()} WHERE idshka = {id}''')
                conn.commit()

                QMessageBox.critical(self, "Готово!", "Пароль был изменен", QMessageBox.Ok)

                self.mnu = Menu()
                self.mnu.show()
                self.close()
        else:
            QMessageBox.critical(self, "Упс!", "Пароли не совпадают", QMessageBox.Ok)


class Registr(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/regg.ui', self)

        self.okk.clicked.connect(self.registr_polzv)
        self.buttonNazad.clicked.connect(self.nazad)

        self.oss = Osnova()

    def nazad(self):
        self.oss.mem()
        self.close()

    def registr_polzv(self):
        if self.prl.toPlainText() == self.prl_2.toPlainText():
            conn = sqlite3.connect('rabochka/persons.db')
            cur = conn.cursor()
            result = cur.execute(f'''SELECT idshka FROM users''').fetchall()
            logins = cur.execute(f'''SELECT login FROM users''').fetchall()
            log = []
            for elem in logins:
                log.append(*elem)

            if self.log.toPlainText() == '' or self.prl.toPlainText() == '' or self.name.toPlainText() == '':
                QMessageBox.critical(self, "А ты шутник", "Вы ничего не ввели в поле", QMessageBox.Ok)

            elif self.log.toPlainText() not in log:
                try:
                    cur.execute(f'''INSERT INTO users(login,parol,idshka,name) 
                    VALUES('{self.log.toPlainText()}','{self.prl.toPlainText()}',{int(*result[-1]) + 1},
                     '{self.name.toPlainText()}')''')
                    cur.execute(f'''INSERT INTO levels(id,lvl) VALUES({int(*result[-1]) + 1},1)''')
                    cur.execute(f'''INSERT INTO menu(idshka,avatarka) VALUES({int(*result[-1]) + 1},'1')''')

                except:
                    cur.execute(f'''INSERT INTO users(login,parol,idshka,name) 
                    VALUES('{self.log.toPlainText()}','{self.prl.toPlainText()}',1,'{self.name.toPlainText()}')''')
                    cur.execute(f'''INSERT INTO levels(id,lvl) 
                                                    VALUES(1,1)''')
                    cur.execute(f'''INSERT INTO menu(idshka,avatarka) VALUES(1,'1')''')

                QMessageBox.critical(self, "Готово!", "Поздравляю с регистрацией!", QMessageBox.Ok)
                conn.commit()

                self.oss.mem()
                self.close()
            else:
                QMessageBox.critical(self, "Кудааааа", "Такой пользователь уже есть!", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Упс!", "Пароли не совпадают", QMessageBox.Ok)


class Loginn(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/log.ui', self)

    def proverka(self):
        global id, lvl, logiin, password, namee

        conn = sqlite3.connect('rabochka/persons.db')
        cur = conn.cursor()
        logins = cur.execute(f'''SELECT login FROM users''').fetchall()
        prls = cur.execute(f'''SELECT login,parol FROM users''').fetchall()
        idd = cur.execute(f'''SELECT idshka FROM users''').fetchall()
        names = cur.execute(f'''SELECT name FROM users''').fetchall()
        lvls = cur.execute(f'''SELECT lvl FROM levels''').fetchall()
        log = []
        for elem in logins:
            log.append(*elem)

        if self.loginn.toPlainText() not in log:
            QMessageBox.critical(self, "Кудааааа", "Такого пользователя нет", QMessageBox.Ok)

        elif (self.loginn.toPlainText(), self.paroll.toPlainText()) not in prls:
            QMessageBox.critical(self, "Кудааааа", "Пароль не правильный)))", QMessageBox.Ok)

        elif (self.loginn.toPlainText(), self.paroll.toPlainText()) in prls:
            self.oss = Osnova()

            id = idd[prls.index((self.loginn.toPlainText(), self.paroll.toPlainText()))][0]
            lvl = lvls[prls.index((self.loginn.toPlainText(), self.paroll.toPlainText()))][0]

            logiin = self.loginn.toPlainText()
            password = self.paroll.toPlainText()
            namee = names[prls.index((self.loginn.toPlainText(), self.paroll.toPlainText()))][0]

            self.close()
            self.oss.show()


class Shbln(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/sbl.ui', self)

        self.osn = Osnova()

        self.button.clicked.connect(self.vibor)

        self.flag = False

    def vibor(self):
        self.f1 = self.radioButton_1.isChecked()
        self.f2 = self.radioButton_2.isChecked()
        self.f3 = self.radioButton_3.isChecked()
        self.f4 = self.radioButton_4.isChecked()
        self.f5 = self.radioButton_5.isChecked()
        self.f6 = self.radioButton_6.isChecked()

        if self.f1:
            self.osn.shbln_pic = 'sbln/1.jpg'
            self.flag = True
        elif self.f2:
            self.osn.shbln_pic = 'sbln/2.jpg'
            self.flag = True
        elif self.f3:
            self.osn.shbln_pic = 'sbln/3.jpg'
            self.flag = True
        elif self.f4:
            self.osn.shbln_pic = 'sbln/4.jpg'
            self.flag = True
        elif self.f5:
            self.osn.shbln_pic = 'sbln/5.jpg'
            self.flag = True
        elif self.f6:
            self.osn.shbln_pic = 'sbln/6.jpg'
            self.flag = True

        else:
            QMessageBox.critical(self, "Эм", "Вы не выбрали шаблон", QMessageBox.Ok)

        if self.flag:
            self.osn.show()
            self.osn.flag_for_shln = True
            self.osn.vstavka_pic()
            self.close()


class Osnova(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/osn.ui', self)

        self.conn = sqlite3.connect('rabochka/persons.db')
        self.cur = self.conn.cursor()

        self.kartinka.clicked.connect(self.vstavka_pic)
        self.bibl.clicked.connect(self.show_sbl)
        self.vst_text.clicked.connect(self.spros_text)
        self.vst_pic.clicked.connect(self.spros_pic)
        self.ramka.clicked.connect(self.mem_ramka_text_zagolovok)
        self.sohranit.clicked.connect(self.sohr)
        self.flag_ok.clicked.connect(self.flagok)
        self.menu.clicked.connect(self.menu_open)

        self.flag_ok.hide()

        self.x1 = 30
        self.y1 = 30
        self.flag = True
        self.flag_1 = True
        self.flag_2 = True
        self.flag_deistv = True

        self.razmer.valueChanged[int].connect(self.changeValue)
        self.size_text = 18

        self.razmer_2.valueChanged[int].connect(self.changeValue_1)
        self.size_pic = 40

        self.gradus.valueChanged[int].connect(self.sliderMoved)
        self.grds_pic = 0

        self.gradus_2.valueChanged[int].connect(self.sliderMoved_1)
        self.grds_txt = 0

        self.prozrach.valueChanged.connect(self.prozr)
        self.prozrachnost = 255

        self.shrift.currentTextChanged.connect(self.srft_changed)
        self.shrft = 'Arial.ttf'

        self.flag_for_combbox = True
        self.flag_for_shln = False

    def menu_open(self):
        self.menu = Menu()
        self.menu.show()

    def combbox(self):
        global lvl

        spisok = []
        for (dirpath, dirnames, filenames) in walk('shrifts/'):
            spisok.extend(filenames)
            break

        if self.flag_for_combbox:
            if lvl < 10:
                self.shrift.addItems(spisok[:3])
                self.flag_for_combbox = False
            elif lvl >= 10 and lvl < 50:
                self.shrift.addItems(spisok[:6])
                self.flag_for_combbox = False
            else:
                self.shrift.addItems(spisok[:15])
                self.flag_for_combbox = False

    def flagok(self):
        self.flag = True
        self.flag_1 = True
        if self.flag_2 is False:
            self.flag_2 = True
            self.width, self.height = self.img.size
        self.flag_deistv = True
        self.flag_ok.hide()
        self.sohranit.show()
        try:
            self.img = self.nazd.copy()
        except:
            None

    def mousePressEvent(self, event):
        self.x1 = event.x()
        self.y1 = event.y()
        if self.flag is False:
            self.vstav_text()
        if self.flag_1 is False:
            self.vstav_pic()

    def sohr(self):
        global id, lvl

        nazvanie, ok = QInputDialog.getText(self, "Имя файла",
                                            "Как назвать файл?")
        try:
            if nazvanie:
                self.img.save(f'mem/{nazvanie}.png')
                QMessageBox.critical(self, "Ура", f'Мем сохранен в папке .../memcreator/mem/{nazvanie}.png',
                                     QMessageBox.Ok)
            else:
                self.img.save('mem/Вы_не_ввели_название.png')
                QMessageBox.critical(self, "Ура", 'Мем сохранен в папке .../memcreator/mem/Вы_не_ввели_название.png',
                                     QMessageBox.Ok)
            lvl += 1

            self.cur.execute(f'''UPDATE levels SET lvl = {lvl} WHERE id = {id}''')
            self.conn.commit()
            _translate = QtCore.QCoreApplication.translate
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                           font-weight:600;\">Ой, нет мема! Нечего сохранять</span></p></body></html>"))

    def vstavka_pic(self):
        global lvl, id
        try:
            if self.flag_for_shln:
                self.fname = self.shbln_pic
                self.flag_for_shln = False

            elif self.flag_for_shln is False:
                self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

            self.img = Image.open(self.fname)

            self.size = 400, 400
            self.img.thumbnail(self.size, Image.Resampling.LANCZOS)
            self.width, self.height = self.img.size

            self.a = ImageQt(self.img)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                           font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def spros_text(self):
        if self.flag_deistv:
            self.text_mem, self.ok_pressed = QInputDialog.getText(self, "Текст", "Введите текст")

            self.combbox()
            self.vstav_text()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def changeValue(self, value):
        if self.flag is False:
            self.size_text = (value + 1) * 4

            self.vstav_text()

    def sliderMoved_1(self):
        if self.flag is False:
            self.grds_txt = 360 - int(self.gradus_2.value())

            self.vstav_text()

    def srft_changed(self, ):
        if self.flag is False:
            self.shrft = str(self.shrift.currentText())

            self.vstav_text()

    def vstav_text(self):
        if self.ok_pressed:
            try:
                self.nazd = self.img.copy()  # self.nazd - типо назад (назд)

                name = self.text_mem

                self.font = ImageFont.truetype(font=f'shrifts/{self.shrft}', size=self.size_text)
                line_height = sum(self.font.getmetrics())

                fontimage = Image.new('L', (self.font.getsize(name)[0], line_height))
                x, y = fontimage.size
                ImageDraw.Draw(fontimage).text((0, 0), name, fill=255, font=self.font)
                fontimage = fontimage.rotate(self.grds_txt, resample=Image.BICUBIC, expand=True)

                x = self.x1 - 30 - (x // 2)
                y = self.y1 - 30 - ((400 - self.height) // 2) - (y // 2)

                self.flag_ok.show()
                self.sohranit.hide()

                for i in range(3):
                    self.nazd.paste((0, 0, 0), (x - i, y), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x + i, y), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x, y + i), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x, y - i), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x - i, y + i), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x + i, y + i), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x - i, y - i), mask=fontimage)
                    self.nazd.paste((0, 0, 0), (x + i, y - i), mask=fontimage)
                self.nazd.paste((255, 255, 255), (x, y), mask=fontimage)

                self.a = ImageQt(self.nazd)
                self.pixmap = QPixmap.fromImage(self.a)
                self.label.setPixmap(self.pixmap)

                self.flag = False
                self.flag_deistv = False
            except:
                _translate = QtCore.QCoreApplication.translate
                self.label.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                               font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def spros_pic(self):
        if self.flag_deistv:
            self.fname_1 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

            self.vstav_pic()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def changeValue_1(self, value):
        if self.flag_1 is False:
            self.size_pic = (value + 1) * 4

            self.vstav_pic()

    def sliderMoved(self):
        if self.flag_1 is False:
            self.grds_pic = 360 - int(self.gradus.value())

            self.vstav_pic()

    def prozr(self):
        if self.flag_1 is False:
            self.prozrachnost = int(self.prozrach.value())

            self.vstav_pic()

    def vstav_pic(self):
        try:
            self.nazd = self.img.copy()

            self.pic = Image.open(self.fname_1)

            self.size_1 = self.size_pic, self.size_pic
            self.pic.thumbnail(self.size_1, Image.Resampling.LANCZOS)

            self.pic = self.pic.rotate(self.grds_pic, resample=Image.Resampling.BICUBIC, expand=True,
                                       fillcolor=(0, 0, 255))

            rgba = self.pic.convert("RGBA")
            dat = rgba.getdata()
            newData = []
            for item in dat:
                if item[0] == 0 and item[1] == 0 and item[2] == 255:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append((item[0], item[1], item[2], self.prozrachnost))
            rgba.putdata(newData)
            rgba.save("rabochka/transparent_image.png", "PNG")

            self.pic = Image.open('rabochka/transparent_image.png', 'r')

            width, height = self.pic.size
            x = self.x1 - 30 - (width // 2)
            y = self.y1 - 30 - ((400 - self.height) // 2) - (height // 2)
            coord = (x, y)

            self.flag_ok.show()
            self.sohranit.hide()

            self.nazd.paste(self.pic, coord, mask=self.pic)

            self.a = ImageQt(self.nazd)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)

            self.flag_1 = False
            self.flag_deistv = False

            os.remove("rabochka/transparent_image.png")
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                           font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def mem_ramka_text_zagolovok(self):
        if self.flag_deistv:
            self.zag_ramk, o = QInputDialog.getText(self, "Введите заголовок", "пиши")

            self.mem_ramka_text()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def mem_ramka_text(self):
        if self.flag_deistv:
            self.text_ramk, o = QInputDialog.getText(self, "Текст", "Введите текст")

            self.mem_ramka()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def mem_ramka(self):
        try:
            width, height = self.img.size

            font = ImageFont.truetype(f'shrifts/Times_new_roman.ttf', size=30)
            line_height1 = sum(font.getmetrics())
            fontimage1 = Image.new('L', (font.getsize(self.zag_ramk)[0], line_height1))
            x, y = fontimage1.size
            ImageDraw.Draw(fontimage1).text((0, 0), self.zag_ramk, fill=255, font=font)

            font1 = ImageFont.truetype(f'shrifts/Arial.ttf', size=15)
            line_height = sum(font1.getmetrics())
            fontimage = Image.new('L', (font1.getsize(self.text_ramk)[0], line_height))
            x1, y1 = fontimage.size
            ImageDraw.Draw(fontimage).text((0, 0), self.text_ramk, fill=255, font=font1)

            self.ramka = Image.new('RGBA', (width + 50, height + 10 + y + 15 + y1 + 40), 'black')
            idraw = ImageDraw.Draw(self.ramka)

            idraw.rectangle((20, 20, width + 30, height + 30), fill='white')
            idraw.rectangle((23, 23, width + 27, height + 27), fill='black')

            self.ramka.paste((255, 255, 255), ((width + 50 - x) // 2, (height + 40)),
                             mask=fontimage1)
            self.ramka.paste((255, 255, 255), ((width + 50 - x1) // 2, (height + 40 + y + 10)),
                             mask=fontimage)
            self.ramka.paste(self.img, (25, 25))

            self.ramka.thumbnail(self.size, Image.Resampling.LANCZOS)

            self.flag_ok.show()
            self.sohranit.hide()

            self.flag_deistv = False
            self.flag_2 = False

            self.nazd = self.ramka.copy()

            self.a = ImageQt(self.nazd)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                           font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def show_sbl(self):
        self.k = Shbln()

        self.k.show()
        self.close()

    def show_zst(self):
        self.w = Zastavka()

        self.w.pushButton.clicked.connect(self.w.close)
        self.w.pushButton.clicked.connect(self.mem)
        self.w.show()

    def mem(self):
        self.osn = Loginn()
        self.regg = Registr()

        self.osn.regist.clicked.connect(self.regg.show)
        self.osn.regist.clicked.connect(self.osn.close)
        self.osn.voity.clicked.connect(self.osn.proverka)
        self.osn.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Osnova()
    ex.show_zst()
    sys.exit(app.exec_())
