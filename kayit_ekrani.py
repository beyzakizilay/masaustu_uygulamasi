import mysql.connector
from PyQt6.QtWidgets import *
import sys

try:
    vtb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="ots"
    )
    secilen = vtb.cursor()
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
    print("Veritabanı bağlantısı başarılı.")
except Exception as e:
    print("Veritabanına bağlanırken hata oluştu:", e)

class KayitPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Kayıt")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kullanıcı Adı:"))
        self.ka_input = QLineEdit()
        layout.addWidget(self.ka_input)

        layout.addWidget(QLabel("Şifre:"))
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.sifre_input)

        kayit_btn = QPushButton("Kayıt Ol")
        kayit_btn.clicked.connect(self.kaydet)
        layout.addWidget(kayit_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def kaydet(self):
        ka = self.ka_input.text()
        sifre = self.sifre_input.text()
        if ka and sifre:
            secilen.execute(f"INSERT INTO kullanicilar(kullanici_adi, sifre) VALUES('{ka}','{sifre}')")
            vtb.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt tamamlandı!")
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Boş alan bırakmayın!")

class AnaPencere(QMainWindow):
    def __init__(self, kullanici):
        super().__init__()
        self.setWindowTitle(f"Sağlık Hesaplayıcı - Hoşgeldin {kullanici}")
        self.kullanici = kullanici
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

            self.sonuc_label.setText(f"BMI: {bmi:.2f} ({durum})\nİdeal Kilo: {ideal_kilo:.2f} kg")

            # Veriyi kaydet
            secilen.execute(f"INSERT INTO bmi_kayit(kullanici_adi,boy,kilo,bmi,ideal_kilo) VALUES('{self.kullanici}',{boy*100},{kilo},{bmi},{ideal_kilo})")
            vtb.commit()

        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doğru doldurun!")

class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setFixedSize(300,200)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kullanıcı Adı:"))
        self.ka_input = QLineEdit()
        layout.addWidget(self.ka_input)

        layout.addWidget(QLabel("Şifre:"))
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.sifre_input)

        giris_btn = QPushButton("Giriş Yap")
        giris_btn.clicked.connect(self.giris)
        layout.addWidget(giris_btn)

        kayit_btn = QPushButton("Kayıt Ol")
        kayit_btn.clicked.connect(self.kayit)
        layout.addWidget(kayit_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def giris(self):
        ka = self.ka_input.text()
        sifre = self.sifre_input.text()
        secilen.execute("SELECT * FROM kullanicilar")
        kullanicilar = secilen.fetchall()
        for k in kullanicilar:
            if ka == k[1] and sifre == k[2]:
                self.ana_ekran = AnaPencere(ka)
                self.ana_ekran.show()
                self.close()
                return
        QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

    def kayit(self):
        self.kayit_pencere = KayitPenceresi()
        self.kayit_pencere.show()

app = QApplication(sys.argv)
pencere = GirisEkrani()
pencere.show()
sys.exit(app.exec())
