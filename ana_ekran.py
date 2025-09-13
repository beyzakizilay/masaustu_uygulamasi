import mysql.connector
from PyQt6.QtWidgets import *
import kayit_ekrani 

try:
    vtb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"
    )
    secilen = vtb.cursor()
    secilen.execute("create database if not exists ots")
    secilen.execute("show databases")
    vtlistesi = secilen.fetchall()
    print("Veritabanları listesi:", vtlistesi)
    print("Bağlantı tamam:")
except:
    print("Veritabanına bağlanırken bir hata oluştu.")


class AnaPencere(QMainWindow):
    def tiklama(self):
        alert = QMessageBox()
        alert.setText('Tıkladın!')
        alert.exec()

    def __init__(self):
        super().__init__()

        def ceviriac():
            self.ceviripenceresi = ots_ceviri_modul.ceviriPenceresi()
            self.ceviripenceresi.show()

        def harcamaEkle():
            print("harcamaEkle çalıştı.")
            self.pencere1 = ots_harcama_talep_modulu.HarcamaTalepPenceresi()
            self.pencere1.show()
            print("harcamaEkle çalıştı.1")

        icerik = QVBoxLayout()

        ceviri = QPushButton('Çeviri')
        icerik.addWidget(ceviri)
        ceviri.clicked.connect(ceviriac)

        icerik.addWidget(QPushButton('Dene'))
        buton1 = QPushButton('Tıkla')
        buton1.clicked.connect(self.tiklama)

        harcamaKayit = QPushButton('Harcama Talebi Ekle')
        icerik.addWidget(harcamaKayit)
        harcamaKayit.clicked.connect(harcamaEkle)

        icerik.addWidget(buton1)
        icerik.addWidget(QLabel('Bilgi'))

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)


class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Harcama Talep Uygulaması")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kullanıcı adı:"))
        ka = QLineEdit()
        layout.addWidget(ka)
        layout.addWidget(QLabel("Şifre:"))
        sf = QLineEdit()
        sf.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(sf)
        layout.addWidget(QCheckBox("Beni hatırla"))

        def kontrol():
            secilen.execute("create table if not exists ots.kullanicilar (id int auto_increment primary key, kullanici_adi varchar(50), sifre varchar(50))")
            secilen.execute("select * from ots.kullanicilar")
            kullanicilistesi = secilen.fetchall()
            print(kullanicilistesi)
            print("Girilen KA:", ka.text())
            print("Girilen SF:", sf.text())

            for aa in kullanicilistesi:
                if ka.text() == aa[1] and sf.text() == aa[2]:
                    print("Giriş yapabilir")
                    self.anaekran = AnaPencere()
                    self.anaekran.show()
                    self.close()
                    return
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")

        buton = QPushButton("Giriş yap")
        layout.addWidget(buton)
        buton.clicked.connect(kontrol)
        layout.addWidget(QLabel("..."))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


aa = QApplication([])
pencere = GirisEkrani()
pencere.show()
aa.exec()
