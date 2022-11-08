import sys
from os import system

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
        uic.loadUi('vkl.ui', self)


class Shbln(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sbl.ui', self)

        self.x = Image.open('3.jpg')
        self.size = 150, 150
        self.x.thumbnail(self.size)
        self.a = ImageQt(self.x)
        self.pixmap = QPixmap.fromImage(self.a)
        self.pic_1.setPixmap(self.pixmap)


class Osnova(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('osn.ui', self)  # Загружаем дизайн
        self.kartinka.clicked.connect(self.yo)
        self.bibl.clicked.connect(self.show_sbl)
        self.vst_text.clicked.connect(self.spros_text)
        self.vst_pic.clicked.connect(self.spros_pic)
        self.sohranit.clicked.connect(self.sohr)
        self.flag_ok.clicked.connect(self.flgok)
        self.flag_ok.hide()
        self.x1 = 30
        self.y1 = 30
        self.flag = True
        self.flag_1 = True
        self.flag_deistv = True

    def flgok(self):
        self.flag = True
        self.flag_1 = True
        self.flag_deistv = True
        self.flag_ok.hide()
        self.sohranit.show()
        try:
            self.img = self.nazd.copy()
        except:
            None

    def mousePressEvent(self, event):
        self.coords.setText(f'{event.x()}, {event.y()}')
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
            self.sizezz = 1200, 1200
            self.img.thumbnail(self.sizezz)
            if nazv:
                self.img.save(f'{nazv}.jpg')
            else:
                self.img.save('Вы_не_ввели_название.jpg')
            self.img.thumbnail(self.size)
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                           font-weight:600;\">Ой, нет мема! Нечего сохранять</span></p></body></html>"))

    def yo(self):
        try:
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.img = Image.open(self.fname)
            self.size = 400, 400
            self.img.thumbnail(self.size)
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
            self.flag_ok.show()
            self.sohranit.hide()
            self.vstav_text()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def spros_pic(self):
        if self.flag_deistv:
            self.fname_1 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.flag_ok.show()
            self.sohranit.hide()
        else:
            QMessageBox.critical(self, "Ой, ошибка ", "Ты забыл закончить предыдущее действие, бака", QMessageBox.Ok)

    def vstav_text(self):
        if self.ok_pressed:
            self.coords.setText(self.text_mem)
            try:
                self.flag_deistv = False
                self.nazd = self.img.copy()
                name = self.text_mem
                self.font = ImageFont.truetype('Arial.ttf', size=18)
                self.draw_text = ImageDraw.Draw(self.nazd)
                x = self.x1 - 30
                y = self.y1 - 30 - ((400 - self.height) // 2)
                for off in range(3):
                    # move right
                    self.draw_text.text((x - off, y), name, font=self.font, fill='black')
                    # move left
                    self.draw_text.text((x + off, y), name, font=self.font, fill='black')
                    # move up
                    self.draw_text.text((x, y + off), name, font=self.font, fill='black')
                    # move down
                    self.draw_text.text((x, y - off), name, font=self.font, fill='black')
                    # diagnal left up
                    self.draw_text.text((x - off, y + off), name, font=self.font, fill='black')
                    # diagnal right up
                    self.draw_text.text((x + off, y + off), name, font=self.font, fill='black')
                    # diagnal left down
                    self.draw_text.text((x - off, y - off), name, font=self.font, fill='black')
                    # diagnal right down
                    self.draw_text.text((x + off, y - off), name, font=self.font, fill='black')
                self.draw_text.text((x, y), name, font=self.font, fill='white')
                self.a = ImageQt(self.nazd)
                self.pixmap = QPixmap.fromImage(self.a)
                self.label.setPixmap(self.pixmap)
                self.flag = False
            except:
                _translate = QtCore.QCoreApplication.translate
                self.label.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; \
                                               font-weight:600;\">Вы не выбрали картинку!</span></p></body></html>"))

    def vstav_pic(self):
        try:
            self.flag_deistv = False
            self.nazd = self.img.copy()
            self.pic = Image.open(self.fname_1)
            self.size_1 = 50, 50
            self.pic.thumbnail(self.size_1)
            self.vstav_pic()
            x = self.x1 - 30
            y = self.y1 - 30 - ((400 - self.height) // 2)
            coord = (x, y)
            self.nazd.paste(self.pic, coord)
            self.a = ImageQt(self.nazd)
            self.pixmap = QPixmap.fromImage(self.a)
            self.label.setPixmap(self.pixmap)
            self.flag_1 = False
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
        self.osn = Osnova()
        self.osn.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Osnova()
    ex.show_zst()
    sys.exit(app.exec_())
