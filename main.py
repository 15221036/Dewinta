import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate  # Import QDate dengan benar
from PyQt5.QtWidgets import QMessageBox

class HalamanAwal(QtWidgets.QMainWindow): #membuat class HalamanMulai
    def __init__(self):
        super(HalamanAwal, self).__init__()
        uic.loadUi("HalamanAwal.ui", self) #mengimpor file ui

        self.tombol_mulai = self.findChild(QtWidgets.QPushButton, 'pushButton_2') #mrndefiniskan pushButton_2 dengan nama tombol_mulai
        self.tombol_mulai.clicked.connect(self.goToLogin) #menghubungkan tombol mulai dengan fungsi goToLogin

    def goToLogin(self): #membuat fungsi gotologin
        self.halamanLogin = HalamanLogin() #membuat variable halamanlogin dengan fungsi memanggil Halaman Login
        self.halamanLogin.show() #menampilkan halamanLogin
        self.close() #menutup Halaman sebelemumnya

class HalamanLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super(HalamanLogin, self).__init__()
        uic.loadUi("HalamanLogin.ui", self)

        self.input_pengguna = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.input_password = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
        self.input_tglLahir = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')

        self.tombol_login  = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.tombol_daftar = self.findChild(QtWidgets.QPushButton, 'pushButton_4')

        self.tombol_daftar.clicked.connect(self.goToDaftar)
        self.tombol_login.clicked.connect(self.login)

    def goToDaftar(self):
        self.halamanDaftar= HalamanDaftar()
        self.halamanDaftar.show()
        self.close()

    def goToMenu(self):
        self.halamanmenu = HalamanMenu()
        self.halamanmenu.show()
        self.close()

    def login(self):
        username = self.input_pengguna.text()
        password = self.input_password.text()
        tgl_lahir = self.input_tglLahir.text()
        if self.check_credentials(username, password, tgl_lahir):
            self.goToMenu()
        else:
            QMessageBox.warning(self, 'Error', 'data yang anda masukan salah.') #menampilkan messagebox

    def check_credentials(self, username, password, tgl_lahir): #fungsi mengecek data yang dimasukan benar atau salah
        try:
            with open("users.txt", "r") as file: #membuka file txt
                for line in file: #perulangan line di dalamn file
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:  # cek jumlah elemen harus 3 (username, password, tgl_lahir)
                        continue
                    username_tersimpan, password_tersimpan, tgl_lahir_tersimpan = parts #membuat variabel parts
                    if username_tersimpan == username and password_tersimpan == password and tgl_lahir_tersimpan == tgl_lahir:
                        return True
        except FileNotFoundError: #membuat error handling
            print("File tidak ditemukan")
        except IOError:
            print("kesalahan dalam membaca data")
        return False

class HalamanMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(HalamanMenu, self).__init__()
        uic.loadUi("HalamanMenu.ui", self)

        self.pushButton_2.clicked.connect(self.tutupAPK)

    def tutupAPK(self):
        self.close()
class HalamanDaftar(QtWidgets.QMainWindow):
    def __init__(self):
        super(HalamanDaftar, self).__init__()
        uic.loadUi("Halaman Daftar.ui", self)
        self.input_pengguna = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.input_password = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
        self.input_tglLahir = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
        self.tombol_kembali = self.findChild(QtWidgets.QPushButton, 'pushButton_5')

        self.tombol_daftar = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.tombol_daftar.clicked.connect(self.daftar)
        self.tombol_kembali.clicked.connect(self.kembali)

    def kembali(self):
        self.halamanlogin = HalamanLogin()
        self.halamanlogin.show()
        self.close()

    def daftar(self):
        username = self.input_pengguna.text() #membuat variabel dan dihubungkan dengan lineEdit
        password = self.input_password.text()
        tgl_lahir = self.input_tglLahir.text()
        if self.cek_email_yang_sudah_ada(username):
            QMessageBox.warning(self, 'Error', 'email sudah terdaftar.')
        else:
            if self.validasi_tanggal_lahir(tgl_lahir):
                self.save_credentials(username, password, tgl_lahir)
                QMessageBox.information(self, 'Success', 'akun sukses dibuat')
            else:
                QMessageBox.warning(self, 'Error', 'Format tanggal lahir harus dd/mm/yy')

    def cek_email_yang_sudah_ada(self, username):  # Ini harusnya ada
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) >= 3 and username == data[0]:
                        return True
            return False
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'file data tidak dapat ditemukan')
            return False

    def validasi_tanggal_lahir(self, tgl_lahir):
        try:
            QDate.fromString(tgl_lahir, "dd/mm/yy")
            return True
        except ValueError:
            return False
    #membuat fungsi validasi tanggal lahir

    def save_credentials(self, username, password, tgl_lahir):
        try:
            with open("users.txt", "a") as file:
                file.write(f"{username},{password},{tgl_lahir}\n")
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'file data tidak dapat ditemukan.')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = HalamanAwal()
    window.show()
    sys.exit(app.exec_())