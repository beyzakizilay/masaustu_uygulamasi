import mysql.connector
from PyQt6.QtWidgets import *
import sys
import ots_ogrenci_kayit_modulu 

try:
    vtb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"
    )
    secilen = vtb.cursor()
    secilen.execute("CREATE DATABASE IF NOT EXISTS ots")
    secilen.execute("USE ots")
    secilen.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar(
            id INT AUTO_INCREMENT PRIMARY KEY,
            kullanici_adi VARCHAR(50),
            sifre VARCHAR(50)
        )
    """)
    secilen.execute("""
        CREATE TABLE IF NOT EXISTS bmi_kayit(
            id INT AUTO_INCREMENT PRIMARY KEY,
            kullanici_adi VARCHAR(50),
            boy FLOAT,
            kilo FLOAT,
            bmi FLOAT,
            ideal_kilo FLOAT
        )
    """)
    vtb.commit()
    print("Veritabanı bağlantısı tamam.")
except Exception as e:
    print("Veritabanına bağlanırken hata:", e)


class AnaPencere(QMainWindow):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle(f"Sağlık Hesaplayıcı - Hoşgeldin {kullanici}")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Boy (cm):"))
        self.boy_input = QLineEdit()
        layout.addWidget(self.boy_input)

        layout.addWidget(QLabel("Kilo (kg):"))
        self.kilo_input = QLineEdit()
        layout.addWidget(self.kilo_input)

        hesap_btn = QPushButton("Hesapla")
        hesap_btn.clicked.connect(self.hesapla)
        layout.addWidget(hesap_btn)

        self.sonuc_label = QLabel("")
        layout.addWidget(self.sonuc_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def hesapla(self):
        try:
            boy = float(self.boy_input.text()) / 100
            kilo = float(self.kilo_input.text())
            bmi = kilo / (boy ** 2)
            ideal_kilo = (boy*100 - 100) * 0.9

            if bmi < 18.5:
                durum = "Zayıf"
            elif 18.5 <= bmi < 25:
                durum = "Normal"
            elif 25 <= bmi < 30:
                durum = "Fazla Kilo"
            else:
                durum = "Obez"

            self.sonuc_label.setText(
                f"BMI: {bmi:.2f} ({durum})\nİdeal Kilo: {ideal_kilo:.2f} kg"
            )

            secilen.execute(
                "INSERT INTO bmi_kayit(kullanici_adi,boy,kilo,bmi,ideal_kilo) "
                "VALUES(%s,%s,%s,%s,%s)",
                (self.kullanici, boy*100, kilo, bmi, ideal_kilo)
            )
            vtb.commit()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli değer girin!")


class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kullanıcı adı:"))
        self.ka = QLineEdit()
        layout.addWidget(self.ka)

        layout.addWidget(QLabel("Şifre:"))
        self.sf = QLineEdit()
        self.sf.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.sf)

        giris_btn = QPushButton("Giriş Yap")
        giris_btn.clicked.connect(self.kontrol)
        layout.addWidget(giris_btn)

        kayit_btn = QPushButton("Kayıt Ol")
        kayit_btn.clicked.connect(self.kayit_ac)
        layout.addWidget(kayit_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def kontrol(self):
        secilen.execute("SELECT * FROM kullanicilar")
        kullanicilistesi = secilen.fetchall()
        for k in kullanicilistesi:
            if self.ka.text() == k[1] and self.sf.text() == k[2]:
                self.ana = AnaPencere(self.ka.text())
                self.ana.show()
                self.close()
                return
        QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

    def kayit_ac(self):
        self.kayit = ots_ogrenci_kayit_modulu.KayitPenceresi(vtb, secilen)
        self.kayit.show()

app = QApplication(sys.argv)
pencere = GirisEkrani()
pencere.show()
sys.exit(app.exec())
