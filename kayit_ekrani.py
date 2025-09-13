import mysql.connector
from PyQt6.QtWidgets import *
from datetime import datetime

try:
    vtb_harcama = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="ots"
    )
    secilen_harcama = vtb_harcama.cursor()
    secilen_harcama.execute("""
        create table if not exists harcama_talepleri(
            id int auto_increment primary key,
            aciklama varchar(255),
            tutar decimal(10,2),
            tarih date
        )
    """)
    print("Bağlantı tamam.")
except Exception as e:
    print("Veritabanına bağlanırken bir hata oluştu:", e)


class HarcamaTalepPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Harcama Talep Kayıt")

        icerik = QVBoxLayout()

        icerik.addWidget(QLabel("Harcama Açıklaması: "))
        self.aciklama_kutusu = QLineEdit()
        icerik.addWidget(self.aciklama_kutusu)

        icerik.addWidget(QLabel("Tutar (₺): "))
        self.tutar_kutusu = QLineEdit()
        icerik.addWidget(self.tutar_kutusu)

        self.tarih = datetime.now().strftime("%Y-%m-%d")
        self.tarih_label = QLabel(f"Tarih: {self.tarih}")
        icerik.addWidget(self.tarih_label)

        buton1 = QPushButton("Kaydet")
        icerik.addWidget(buton1)
        buton1.clicked.connect(self.kaydetme)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

    def kaydetme(self):
        self.aciklama = self.aciklama_kutusu.text()
        self.tutar = self.tutar_kutusu.text()

        print(f"Kaydedilecek bilgiler: {self.aciklama}, {self.tutar}, {self.tarih}")

        try:
            secilen_harcama.execute(
                "insert into harcama_talepleri(aciklama, tutar, tarih) values(%s, %s, %s)",
                (self.aciklama, self.tutar, self.tarih)
            )
            vtb_harcama.commit()

            QMessageBox.information(self, "Başarılı", "Harcama talebi kaydedildi.")
            self.aciklama_kutusu.clear()
            self.tutar_kutusu.clear()

        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Kayıt sırasında hata oluştu: {e}")


if __name__ == "__main__":
    aa = QApplication([])
    pencere = HarcamaTalepPenceresi()
    pencere.show()
    aa.exec()
