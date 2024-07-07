from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QFormLayout, QLineEdit, QDateEdit,
                             QLabel, QVBoxLayout)
from PyQt5.QtCore import QDate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import sys

class Arayuz(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle("Katılımcı Sertifikası Oluştur")
        self.setGeometry(100, 100, 500, 500)

        katilimci = QFormLayout()

        self.ad_input = QLineEdit()
        self.soyad_input = QLineEdit()
        self.etkinlik_input = QLineEdit()
        self.saat_input = QLineEdit()
        self.tarih_input = QDateEdit()
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDate(QDate.currentDate())

        self.gonder = QPushButton("Sertifika Oluştur")
        self.gonder.clicked.connect(self.bilgi_gonder)

        katilimci.addRow(QLabel("Katılımcı Adı: "), self.ad_input)
        katilimci.addRow(QLabel("Katılımcı Soyadı: "), self.soyad_input)
        katilimci.addRow(QLabel("Etkinlik Adı: "), self.etkinlik_input)
        katilimci.addRow(QLabel("Etkinlik Saati: "), self.saat_input)
        katilimci.addRow(QLabel("Etkinlik Tarihi: "), self.tarih_input)
        katilimci.addRow(self.gonder)

        layout = QVBoxLayout()
        layout.addLayout(katilimci)
        self.setLayout(layout)

    def bilgi_gonder(self):
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        etkinlik = self.etkinlik_input.text()
        saat = self.saat_input.text()
        tarih = self.tarih_input.date().toString("dd/MM/yyyy")

        yazi = f"Tebrikler {ad} {soyad}, {etkinlik} etkinliğine katıldınız. Saat : {saat}"

        cert_olustur = PDFOlustur(f"{ad.lower()}{soyad.lower()}", f"{ad} {soyad} Katılımcı Sertifikası", "MITC")
        cert_olustur.pdf_olustur(yazi)

        self.temizle()

    def temizle(self):
        self.ad_input.clear()
        self.soyad_input.clear()
        self.etkinlik_input.clear()
        self.saat_input.clear()

class PDFMetadata:

    def __init__(self, baslik, yazar):
        self.baslik = baslik
        self.yazar = yazar

    def metadata_olustur(self, belge):
        belge.setTitle(self.baslik)
        belge.setAuthor(self.yazar)

class PDFIcerik:

    def __init__(self):
        self.font_secimi()

    def font_secimi(self):
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    def yazdir(self, belge, yazi, font='Arial', size=12):
        belge.setFont(font, size)
        belge.drawString(100, 750, yazi)

class PDFOlustur(PDFMetadata, PDFIcerik):

    def __init__(self, dosyaadi, baslik, yazar):
        PDFMetadata.__init__(self, baslik, yazar)
        PDFIcerik.__init__(self)
        self.dosyaadi = dosyaadi + '.pdf'
        self.canvas = canvas.Canvas(self.dosyaadi, pagesize=letter)

    def pdf_olustur(self, yazi):
        self.metadata_olustur(self.canvas)
        self.yazdir(self.canvas, yazi)
        self.canvas.save()
        print("PDF Oluşturuldu.")

app = QApplication(sys.argv)
katil = Arayuz()
katil.show()
sys.exit(app.exec_())

# ad = input("Dosya adını gir: ")
# baslik = input("Başlık gir:")
# yazar = input("Yazarı girin.")
# text = 'Tebrikler yazdı!'

# olustur = PDFOlustur(ad, baslik, yazar)
# olustur.pdf_olustur(text)