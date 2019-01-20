from tkinter import *
import info
import sys

class Application(Frame):
    def __init__(self,master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_main()

    def create_main(self):
        print("testing")
        self.title = Label(self, text=" Registro ") 
        self.title.grid(row=0, column=2)

        self.user_entry_label = Label(self, text="Nombre de usuario: ")
        self.user_entry_label.grid(row=1, column=1)

        self.user_entry = Entry(self)                        
        self.user_entry.grid(row=1, column=2)

        self.pass_entry_label = Label(self, text="Contrasena: ")
        self.pass_entry_label.grid(row=2, column=1)

        self.pass_entry = Entry(self)                        
        self.pass_entry.grid(row=2, column=2)

        self.token_entry_label = Label(self, text="Token: ")
        self.token_entry_label.grid(row=3, column=1)


        self.token_entry = Entry(self)                        
        self.token_entry.grid(row=3, column=2)

        self.sign_in_butt = Button(self, text="Enviar",command = self.logging_in)
        self.sign_in_butt.grid(row=5, column=2)

    def logging_in(self):
        user_get = self.user_entry.get()
        pass_get = self.pass_entry.get()
        token_get = self.token_entry.get()
        f = open('login.txt', 'w')
        f.write('usuario: '+ user_get + '\n')
        f.write('password: '+ pass_get + '\n')
        f.write('token: '+ token_get + '\n')

        info.exportAllInfo()

        sys.exit()


if __name__ == '__main__':
    root = Tk()
    root.title("Registro")
    root.geometry("420x120")

    app = Application(root)#The frame is inside the widgit
    root.mainloop()#Keeps the window open/running
