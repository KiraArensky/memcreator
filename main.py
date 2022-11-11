import sys
import os
from os import system, walk
import sqlite3

try:
    from PyQt5 import uic
except:
    system("pip install PyQt5")
    from PyQt5 import uic

try:
    from PIL.ImageQt import ImageQt
    from PIL import Image, ImageDraw, ImageFont
except:
    system("pip install pillow")
    from PIL.ImageQt import ImageQt
    from PIL import Image, ImageDraw, ImageFont

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog


class Kek(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/vkl.ui', self)


class Registr(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/regg.ui', self)
        self.okk.clicked.connect(self.reg)

    def reg(self):
        if self.prl.toPlainText() == self.prl_2.toPlainText():
            self.oss = Osnova()
            conn = sqlite3.connect('rabochka/persons.db')
            cur = conn.cursor()
            result = cur.execute(f'''SELECT idshka FROM users''').fetchall()
            logins = cur.execute(f'''SELECT login FROM users''').fetchall()
            log = []
            for elem in logins:
                log.append(*elem)
            if self.log.toPlainText() not in log:
                try:
                    cur.execute(f'''INSERT INTO users(login,parol,idshka) 
                    VALUES('{self.log.toPlainText()}','{self.prl.toPlainText()}','{str(int(*result[-1]) + 1)}')''')
                    cur.execute(f'''INSERT INTO levels(id,lvl) 
                                                    VALUES({int(*result[-1]) + 1},1)''')
                except:
                    cur.execute(f'''INSERT INTO users(login,parol,idshka) 
                    VALUES('{self.log.toPlainText()}','{self.prl.toPlainText()}','1')''')
                    cur.execute(f'''INSERT INTO levels(id,lvl) 
                                                    VALUES(1,1)''')

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
        conn = sqlite3.connect('rabochka/persons.db')
        cur = conn.cursor()
        logins = cur.execute(f'''SELECT login FROM users''').fetchall()
        prls = cur.execute(f'''SELECT login,parol FROM users''').fetchall()
        id = cur.execute(f'''SELECT idshka FROM users''').fetchall()
        lvls = cur.execute(f'''SELECT lvl FROM levels''').fetchall()
        log = []
        for elem in logins:
            log.append(*elem)
        if self.loginn.toPlainText() not in log:
            QMessageBox.critical(self, "Кудааааа", "Такого пользователя нет", QMessageBox.Ok)
        elif (self.loginn.toPlainText(), self.paroll.toPlainText()) not in prls:
            QMessageBox.critical(self, "Кудааааа", "Пароль не правильный)))", QMessageBox.Ok)
        elif (self.loginn.toPlainText(), self.paroll.toPlainText()) in prls:
            QMessageBox.critical(self, "Ок", "ок", QMessageBox.Ok)
            self.oss = Osnova()
            self.oss.id = id[prls.index((self.loginn.toPlainText(), self.paroll.toPlainText()))][0]
            self.oss.lvl = lvls[prls.index((self.loginn.toPlainText(), self.paroll.toPlainText()))][0]
            self.close()
            self.oss.show()


class Shbln(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/sbl.ui', self)
        self.x = Image.open('sbln/3.jpg')
        self.size = 150, 150
        self.x.thumbnail(self.size)
        self.a = ImageQt(self.x)
        self.pixmap = QPixmap.fromImage(self.a)
        self.pic_1.setPixmap(self.pixmap)


class Osnova(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/osn.ui', self)  # Загружаем дизайн
        self.conn = sqlite3.connect('rabochka/persons.db')
        self.cur = self.conn.cursor()
        self.kartinka.clicked.connect(self.yo)
        self.bibl.clicked.connect(self.show_sbl)
        self.vst_text.clicked.connect(self.spros_text)
        self.vst_pic.clicked.connect(self.spros_pic)
        self.ramka.clicked.connect(self.mem_zagolovok)
        self.sohranit.clicked.connect(self.sohr)
        self.flag_ok.clicked.connect(self.flgok)
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
        self.przr = 255
        self.shrift.currentTextChanged.connect(self.srft_changed)
        self.shrft = 'Arial.ttf'

    def combbox(self):
        spisok = []
        for (dirpath, dirnames, filenames) in walk('shrifts/'):
            spisok.extend(filenames)
            break
        if self.lvl < 10:
            self.shrift.addItems(spisok[:3])
        elif self.lvl >= 10 and self.lvl < 50:
            self.shrift.addItems(spisok[:6])
        else:
            self.shrift.addItems(spisok[:15])

    def flgok(self):
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
        nazv, ok = QInputDialog.getText(self, "Имя файла",
                                        "Как назвать файл?")
        try:
            sizezz = 1000, 1000
            self.img.resize(sizezz, Image.Resampling.LANCZOS)
            if nazv:
                self.img.save(f'mem/{nazv}.png')
            else:
                self.img.save('Вы_не_ввели_название.png')
            self.lvl += 1
            self.cur.execute(f'''UPDATE levels SET lvl = {self.lvl} WHERE id = {self.id}''')
            self.conn.commit()
            self.img.thumbnail(self.size)
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                           font-weight:600;\">Ой, нет мема! Нечего сохранять</span></p></body></html>"))

    def yo(self):
        self.combbox()
        try:
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
                self.nazd = self.img.copy()
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
                    # move right
                    self.nazd.paste((0, 0, 0), (x - i, y), mask=fontimage)
                    # move left
                    self.nazd.paste((0, 0, 0), (x + i, y), mask=fontimage)
                    # move up
                    self.nazd.paste((0, 0, 0), (x, y + i), mask=fontimage)
                    # move down
                    self.nazd.paste((0, 0, 0), (x, y - i), mask=fontimage)
                    # diagnal left up
                    self.nazd.paste((0, 0, 0), (x - i, y + i), mask=fontimage)
                    # diagnal right up
                    self.nazd.paste((0, 0, 0), (x + i, y + i), mask=fontimage)
                    # diagnal left down
                    self.nazd.paste((0, 0, 0), (x - i, y - i), mask=fontimage)
                    # diagnal right down
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
            self.przr = int(self.prozrach.value())
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
                    newData.append((item[0], item[1], item[2], self.przr))
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

    def mem_zagolovok(self):
        if self.flag_deistv:
            self.zag_ramk, self.oye = QInputDialog.getText(self, "Введите заголовок", "пиши")
            if len(self.zag_ramk) > 20:
                n = len(self.zag_ramk) // 20 + 1
                lst = []
                for i in range(n):
                    lst.append(self.zag_ramk[i * 20:(i + 1) * 20])
                self.zag_ramk = '\n'.join(lst)
            self.mem_text()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def mem_text(self):
        if self.flag_deistv:
            self.text_ramk, self.oey = QInputDialog.getText(self, "Текст", "Введите текст")
            self.mem_ramka()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def mem_ramka(self):
        try:
            font = ImageFont.truetype(f'shrifts/Times_new_roman.ttf', size=50)
            line_height1 = sum(font.getmetrics())
            fontimage1 = Image.new('L', (font.getsize(self.zag_ramk)[0], line_height1))
            x, y = fontimage1.size
            ImageDraw.Draw(fontimage1).text((0, 0), self.zag_ramk, fill=255, font=font)
            font1 = ImageFont.truetype(f'shrifts/Arial.ttf', size=20)
            line_height = sum(font1.getmetrics())
            fontimage = Image.new('L', (font1.getsize(self.text_ramk)[0], line_height))
            x1, y1 = fontimage.size
            ImageDraw.Draw(fontimage).text((0, 0), self.text_ramk, fill=255, font=font1)
            self.ramka = Image.new('RGBA', (self.width + 50, self.height + 10 + y + 15 + y1 + 40), 'black')
            idraw = ImageDraw.Draw(self.ramka)
            idraw.rectangle((20, 20, self.width + 30, self.height + 30), fill='white')
            idraw.rectangle((23, 23, self.width + 27, self.height + 27), fill='black')
            self.ramka.paste((255, 255, 255), ((self.width + 50 - x) // 2, (self.height + 40)),
                             mask=fontimage1)
            self.ramka.paste((255, 255, 255), ((self.width + 50 - x1) // 2, (self.height + 40 + y + 10)),
                             mask=fontimage)
            self.ramka.paste(self.img, (25, 25))
            self.ramka.thumbnail(self.size, Image.Resampling.LANCZOS)
            self.flag_ok.show()
            self.sohranit.hide()
            self.flag_deistv = False
            self.flag_2 = False
            self.img = self.ramka.copy()
            self.a = ImageQt(self.img)
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

    def show_zst(self):
        self.w = Kek()
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
