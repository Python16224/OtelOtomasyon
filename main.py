import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from template import Ui_Form
from PyQt5.QtCore import QDate, pyqtSlot
from datetime import datetime
from thread import Thread
from PIL import Image
from pytesseract import pytesseract
import database
from database import MusteriListesi, GirisCikis
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


class MainPage(QMainWindow):
    engine = create_engine('sqlite:///database.db')
    session = sessionmaker()
    session.configure(bind=engine)
    database.Base.metadata.create_all(engine)
    s = session()

    def __init__(self):
        super(MainPage, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.drm = True

        self.ui.cmb_room.addItem("Seçiniz")
        self.ui.cmb_room.addItems([str(i) for i in range(1, 21)])

        self.ui.table_customer.setHorizontalHeaderLabels(('TC', 'Adı', 'Soyadı', 'Oda No'))
        self.ui.table_customer.setColumnCount(4)
        self.set_controller()
        self.ui.table_customer.insertRow(0)

        self.ui.btn_check_in.clicked.connect(self.check_in)
        self.ui.btn_check_out.clicked.connect(self.check_out)
        self.ui.btn_add_person.clicked.connect(self.add_person)
        self.ui.check_out_date.dateChanged.connect(self.calculate_fee)

        self.th = Thread()
        self.th.changePixmap.connect(self.set_image)
        self.th.start()

    def calculate_fee(self):
        start_date = self.ui.check_in_date.date()
        end_date = self.ui.check_out_date.date()
        days = start_date.daysTo(end_date)
        self.ui.txt_fee.setText(str(days * 100) + "TL")

    @pyqtSlot(QImage)
    def set_image(self, image):
        self.ui.lbl_camera.setPixmap(QPixmap.fromImage(image))

    def add_person(self):
        try:
            resized_image = cv2.resize(self.th.take_photo(), (640, 480))
            cv2.imwrite('id.jpg', resized_image)

            img = Image.open('id.jpg')
            text = pytesseract.image_to_string(img)
            big_data = text.split("<")
            name = ""
            surname = ""
            tc_no = ""
            for i in big_data:
                if i.isalnum() and len(i) == 11:
                    tc_no = i
                elif i.isalpha() and len(i) > 1:
                    if name == "":
                        name = i
                        surname = big_data[big_data.index(name) - 2]
                    else:
                        name += " " + i
            surname = surname[surname.index("\n") + 1:]
            msg = QMessageBox()
            msg.setWindowTitle('Kimlik Verileri')
            msg.setText('Kimlik Bilgileri\nTC :' + tc_no + '\nAdı Soyadı :' + name + " " + surname)
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            x = msg.exec_()
            if x == 1024:
                self.ui.table_customer.setItem(0, 0, QTableWidgetItem(tc_no))
                self.ui.table_customer.setItem(0, 1, QTableWidgetItem(name))
                self.ui.table_customer.setItem(0, 2, QTableWidgetItem(surname))
                self.ui.btn_add_person.setEnabled(False)

                data = self.s.query(MusteriListesi).filter(MusteriListesi.tc_no == tc_no).first()
                if data:
                    self.ui.table_customer.setItem(0, 3, QTableWidgetItem(data.oda_no.oda_no))
                    self.ui.btn_check_out.setEnabled(True)
                else:
                    self.ui.check_in_date.setEnabled(True)
                    self.ui.check_out_date.setEnabled(True)
                    self.ui.cmb_room.setEnabled(True)
                    self.ui.txt_fee.setEnabled(True)
                    self.ui.btn_check_in.setEnabled(True)

        except Exception:
            msg = QMessageBox()
            msg.setWindowTitle('Okuma Hatası')
            msg.setText('Kimlik bilgileri okunamadı!\nLütfen yeniden deneyin.')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def check_in(self):
        check_detail = GirisCikis(giris_tarihi=self.ui.check_in_date.text(),
                                  cikis_tarihi=self.ui.check_out_date.text(),
                                  oda_no=self.ui.cmb_room.currentText(),
                                  fiyat=self.ui.txt_fee.text())

        customer = MusteriListesi(tc_no=self.ui.table_customer.item(0, 0).text(),
                                  adi=self.ui.table_customer.item(0, 1).text(),
                                  soyadi=self.ui.table_customer.item(0, 2).text(),
                                  oda_no=check_detail)

        self.s.add(check_detail)
        self.s.add(customer)
        self.s.commit()

        msg = QMessageBox()
        msg.setWindowTitle('Kaydetme İşlemi')
        msg.setText('Kayıt başarı ile tamamlandı.')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.set_controller()

    def check_out(self):
        tc_no = self.ui.table_customer.item(0, 0).text()
        data = self.s.query(MusteriListesi).filter(MusteriListesi.tc_no == tc_no).first()
        self.s.query(MusteriListesi).filter(MusteriListesi.tc_no == self.ui.table_customer.item(0, 0).text()).delete()
        self.s.query(GirisCikis).filter(GirisCikis.id == data.musteri_id).delete()
        self.s.commit()

        msg = QMessageBox()
        msg.setWindowTitle('Silme İşlemi')
        msg.setText('Kayıt başarı ile silindi.')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.set_controller()

    def set_controller(self):
        date = datetime.now()
        self.ui.check_in_date.setDate(QDate(date.year, date.month, date.day))
        self.ui.check_out_date.setDate(QDate(date.year, date.month, date.day))
        self.ui.cmb_room.setCurrentIndex(0)
        self.ui.txt_fee.setText("0TL")
        self.ui.table_customer.clear()
        self.ui.table_customer.setHorizontalHeaderLabels(('TC', 'Adı', 'Soyadı', 'Oda No'))

        self.ui.check_in_date.setEnabled(False)
        self.ui.check_out_date.setEnabled(False)
        self.ui.cmb_room.setEnabled(False)
        self.ui.txt_fee.setEnabled(False)
        self.ui.btn_check_in.setEnabled(False)
        self.ui.btn_check_out.setEnabled(False)
        self.ui.btn_add_person.setEnabled(True)


def application():
    app = QApplication(sys.argv)
    win = MainPage()
    win.show()
    sys.exit(app.exec_())


application()
