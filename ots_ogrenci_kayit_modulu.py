from PyQt6.QtWidgets import *

class KayitPenceresi(QMainWindow):
    def __init__(self, vtb, secilen):
        super().__init__()
        self.vtb = vtb
        self.secilen = secilen
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
            self.secilen.execute(
                "INSERT INTO kullanicilar(kullanici_adi,sifre) VALUES(%s,%s)",
                (ka, sifre)
            )
            self.vtb.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt tamamlandı!")
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Boş alan bırakmayın!")
