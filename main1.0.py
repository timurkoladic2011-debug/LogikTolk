from customtkinter import *          # сучасний Tkinter
from PIL import Image                # робота з зображеннями
import socket                        # мережа (чат)
import threading                     # потоки для прийому повідомлень

# ================== ЗОБРАЖЕННЯ ==================

# фон головного екрану
FON = CTkImage(Image.open("fon.png"), size=(350,400))

# іконка налаштувань
CONF = CTkImage(Image.open("conf.png"), size=(20,20))

# іконка користувача
USER = CTkImage(Image.open("user.png"), size=(20,20))

# список аватарів користувача
ICONS = []
for i in range(7):
    ICONS.append(
        CTkImage(light_image=Image.open(f"{i}.png"), size=(85,85))
    )

# ================== КОЛЬОРИ ==================

BLUE = "#5D89EA"
CYAN = "#2EB3E4"
PURPULE = "#B43EF5"
MEDIUMBLUE = "#8D60F0"
PHLOX = "#EB0EFC"

# ================== КАСТОМНІ ВІДЖЕТИ ==================

# власний Label
class MyLbl(CTkLabel):
    def __init__(self, master, text="CTkLabel", size=16, image=None):
        super().__init__(
            master,
            text_color=PHLOX,
            text=text,
            font=("Arial", size, "bold"),
            image=image
        )

# власна кнопка
class MyBtn(CTkButton):
    def __init__(self, master, width=140, height=40,
                 text="CTkbutton", image=None, command=None):

        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=20,
            fg_color=PURPULE,
            hover_color=MEDIUMBLUE,
            text=text,
            font=("Arial",16,"bold"),
            text_color="white",
            image=image,
            command=command
        )

# повідомлення в чаті
class Mess(CTkLabel):
    def __init__(self, master, urer, icon, text, anchor):

        # завантаження маленької іконки користувача
        icon = CTkImage(
            light_image=Image.open(f"{icon}.png"),
            size=(25,25)
        )

        super().__init__(
            master=master,
            fg_color="#4C474B",
            text_color="white",
            font=("Arial",16,"bold"),
            image=icon,
            compound="left",
            corner_radius=20,
            padx=10,
            pady=10,
            text=f"{urer}: {text}"
        )

        # розміщення повідомлення
        self.pack(padx=50, pady=2, anchor=anchor)

# ================== ГОЛОВНИЙ ДОДАТОК ==================

class App(CTk):
    def __init__(self):
        super().__init__()

        # ім’я користувача та іконка
        self.USER = "anonim"
        self.ICON = 0
        self.HOST = "0"
        self.PORT = 8080

        # налаштування вікна
        self.geometry("600x400")
        self.configure(fg_color="#4C474B")
        self.title("LogikTalk")
        self.iconbitmap("icon.ico")
        self.resizable(False, False)

        # ================== ГОЛОВНИЙ ЕКРАН ==================

        self.lbl = MyLbl(self, text="WELCOM", size=40, image=FON)
        self.lbl.place(x=0, y=0)

        lbl = MyLbl(self, text="LogikTalk", size=30)
        lbl.place(x=405, y=50)

        # кнопка введення імені
        self.btn_name = MyBtn(
            self, text="Enter name", image=USER,
            command=self.open_name
        )
        self.btn_name.place(x=400, y=120)

        # кнопка вибору іконки
        self.btn_icon = MyBtn(
            self, text="Enter icon", image=CONF,
            command=self.open_icon
        )
        self.btn_icon.place(x=400, y=185)

        # кнопка входу в чат
        self.btn_chat = MyBtn(self, width=100, text="Enter chat")
        self.btn_chat.configure(
            fg_color=PHLOX,
            text_color="grey",
            command=self.open_chat
        )
        self.btn_chat.place(x=415, y=260)

        # ================== ФРЕЙМ ІМЕНІ ==================

        self.frame_name = CTkFrame(
            self, width=350, height=400, fg_color="#342f2f"
        )
        self.frame_name.place(x=-350, y=0)

        label3 = MyLbl(self.frame_name, text="enter your name", size=20)
        label3.place(x=50, y=100)

        self.box_name = CTkEntry(
            self.frame_name,
            width=250,
            height=50,
            fg_color=BLUE,
            corner_radius=25
        )
        self.box_name.place(x=50, y=150)

        self.btn_save_name = MyBtn(
            self.frame_name,
            text="save name",
            command=self.save_name
        )
        self.btn_save_name.place(x=100, y=220)

        # ================== ФРЕЙМ ІКОНОК ==================

        self.frame_icon = CTkFrame(
            self, width=350, height=400, fg_color="#342f2f"
        )
        self.frame_icon.place(x=-350, y=0)

        r, c = 0, 0
        for i in range(1, 7):
            c = 1 if i % 2 == 0 else 0

            btn = MyBtn(
                self.frame_icon,
                text="",
                image=ICONS[i],
                width=80,
                height=80,
                command=lambda i=i: self.save_icon(i)
)
            btn.grid(row=int(r), column=c, padx=23, pady=23)
            r += 0.5

        # ================== ЧАТ ==================

        self.frame_chat = CTkFrame(
            self, width=600, height=400, fg_color="#342f2f"
        )
        self.frame_chat.place(x=0, y=-400)

        # зона повідомлень
        self.all_mess = CTkScrollableFrame(
            self.frame_chat, width=580, height=300,
            fg_color="#342f2f"
        )
        self.all_mess.place(x=0, y=0)

        # поле введення
        self.inp_mess = CTkTextbox(
            self.frame_chat,
            width=350,
            height=50,
            fg_color=BLUE,
            corner_radius=25
        )
        self.inp_mess.place(x=20, y=320)

        # кнопка відправки
        self.btn_send_mess = MyBtn(
            self.frame_chat,
            width=100,
            text="send",
            command=self.send_mess
        )
        self.btn_send_mess.place(x=400, y=320)

        self.frame_start = CTkFrame(self, width=600, height=400, fg_color="#342f2f")
        self.box_port = CTkEntry(
            self.frame_start,
            width=250,
            height=50,
            fg_color=BLUE,
            corner_radius=25
        )
        self.box_port.place(x=50, y=150)
        self.box_host = CTkEntry(
            self.frame_start,
            width=250,
            height=50,
            fg_color=BLUE,
            corner_radius=25
        )
        self.box_host.place(x=50, y=200)

        self.btn_begin = MyBtn(
            self.frame_start,
            text="begin",
            command=self.save_name
        )
        self.btn_begin.place(x=100, y=220)

    def begin(self):
        self.PORT = int(self.box_port.get())
        self.HOST = int(self.box_host.get())
        self.frame_start.destroy()

    def start(self):
        self.HOST = self.box_host.get()
        self.PORT = int(self.box_port.get())
        self.frame_start.destroy()

    
    


    # ================== АНІМАЦІЇ ==================

    def open_name(self):
        self.new_x = -350
        def anime():
            self.new_x += 10
            self.frame_name.place(x=self.new_x, y=0)
            if self.new_x < 0:
                self.after(10, anime)
        anime()

    def close_name(self):
        self.new_x = 0
        def anime():
            self.new_x -= 10
            self.frame_name.place(x=self.new_x, y=0)
            if self.new_x > -350:
                self.after(10, anime)
        anime()

    def save_name(self):
        self.USER = self.box_name.get()
        self.close_name()

    def open_icon(self):
        self.new_x = -350
        def anime():
            self.new_x += 10
            self.frame_icon.place(x=self.new_x, y=0)
            if self.new_x < 0:
                self.after(10, anime)
        anime()

    def close_icon(self):
        self.new_x = 0
        def anime():
            self.new_x -= 10
            self.frame_icon.place(x=self.new_x, y=0)
            if self.new_x > -350:
                self.after(10, anime)
        anime()

    def save_icon(self, i):
        self.ICON = i
        self.close_icon()

    # ================== ЧАТ / МЕРЕЖА ==================

    def open_chat(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((f"{self.HOST}.tcp.eu.ngrok.io", self.PORT))

            # відправка імені та іконки серверу
            self.sock.send(f"{self.USER}|{self.ICON}".encode())

            # локальне повідомлення
            Mess(self.all_mess, self.USER, self.ICON, "welcome to chat", "w")

            # потік прийому повідомлень
            input = threading.Thread(target=self.input_mess)
            input.start()

            # анімація появи чату
            self.new_y = -400
            def anime():
                self.new_y += 10
                self.frame_chat.place(x=0, y=self.new_y)
                if self.new_y < 0:
                    self.after(10, anime)
            anime()

        except:
            self.lbl.configure(text="error connection")

    def input_mess(self):
        file = self.sock.makefile("r", encoding="utf-8", newline="\n")
        while True:
            try:
                mess = file.readline()
                user, icob, mess = mess.rstrip("\n").split("|")
                Mess(self.all_mess, user, icob, mess, "e")
            except:
                Mess(self.all_mess, "server", "0", "error connection", "w")
                self.after(100, self.close)

    def send_mess(self):
        mess = self.inp_mess.get("1.0", "end").strip()
        self.inp_mess.delete("1.0", "end")
        try:
            self.sock.send(mess.encode())
            Mess(self.all_mess, self.USER, self.ICON, mess, "w")
        except:
            Mess(self.all_mess, "server", "0", "error connection", "w")
            self.after(100, self.close)

    def close(self):
        self.sock.close()
        self.destroy()

    
    

# запуск програми
app = App()
app.mainloop()
