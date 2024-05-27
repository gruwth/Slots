import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import os
import pyglet

pyglet.font.add_file(os.path.join(os.path.dirname(__file__), 'font', 'static', 'UbuntuSansMono-Bold.ttf'))

BLACK = '#000000'
WHITE = '#FFFFFF'
L_PINK = '#9f7aea'
D_PINK = '#7c3aed'

class Login(tk.Frame):
    def __init__(self, login_func, register_func, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=D_PINK)
        self.load_custom_font()
        self.create_widgets()
        self.center_window()
        self.show_grid = False
        ### MUSS ZUERST GESETZT WERDEN ###
        self.login_func: function = login_func
        self.register_func: function = register_func


    def load_custom_font(self):
        self.custom_font = tkfont.Font(family='Ubuntu Sans Mono', size=12)
    
    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username", bg=D_PINK, fg=BLACK, font=self.custom_font)
        self.username_label.pack(padx=10, pady=(10, 2))

        self.username_entry_canvas, self.username_entry_widget = self.create_rounded_entry(font=self.custom_font, bg=L_PINK)
        self.username_entry_canvas.pack(padx=10, pady=(2, 10))

        self.password_label = tk.Label(self, text="Password", bg=D_PINK, fg=BLACK, font=self.custom_font)
        self.password_label.pack(padx=10, pady=(10, 2))

        self.password_entry_canvas, self.password_entry_widget = self.create_rounded_entry(show="*", font=self.custom_font, bg=L_PINK)
        self.password_entry_canvas.pack(padx=10, pady=(2, 10))

        self.register_label = tk.Label(self, text="Don't have an account? Register here", bg=D_PINK, fg=BLACK, font=self.custom_font, cursor="hand2")
        self.register_label.pack(side=tk.BOTTOM)

        self.login_button = self.create_rounded_button("Login", self.login, bg=L_PINK, fg=BLACK, font=self.custom_font, width=150, height=40)
        self.login_button.pack(side=tk.BOTTOM, pady=(0, 10))

        self.register_button = self.create_rounded_button("Register", self.register_, bg=L_PINK, fg=BLACK, font=self.custom_font, width=150, height=40)
        self.register_button.pack(side=tk.BOTTOM, pady=(0, 10))
        self.register_button.pack_forget()

        self.register_label.bind("<Button-1>", self.register_clicked)

    def register_clicked(self, event):
        self.login_button.pack_forget()
        self.register_button.pack(side=tk.BOTTOM, pady=(0, 10))
            
        self.confirm_password_label = tk.Label(self, text="Confirm Password", bg=D_PINK, fg=BLACK, font=self.custom_font)
        self.confirm_password_label.pack(padx=10, pady=(10, 2))
        
        self.confirm_password_entry_canvas, self.confirm_password_entry_widget = self.create_rounded_entry(show="*", font=self.custom_font, bg=L_PINK)
        self.confirm_password_entry_canvas.pack(padx=10, pady=(2, 10))
        
        self.register_label.config(text="Back to login", cursor="hand2")
        self.register_label.bind("<Button-1>", self.back_to_login)

    def back_to_login(self, event):
        self.confirm_password_label.pack_forget()
        self.confirm_password_entry_canvas.pack_forget()

        self.register_button.pack_forget()
        self.login_button.pack(side=tk.BOTTOM, pady=(0, 10))

        self.register_label.config(text="Don't have an account? Register here", cursor="hand2")
        self.register_label.bind("<Button-1>", self.register_clicked)

    
    def create_rounded_entry(self, show=None, font=None, bg=None):
        entry_frame = tk.Frame(self, bg=D_PINK)
        entry_frame.grid_propagate(False)
        canvas = tk.Canvas(entry_frame, height=30, width=200, bg=D_PINK, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.create_rounded_rectangle(canvas, 0, 0, 200, 30, radius=15, outline=BLACK, width=2, fill=bg)
        entry = tk.Entry(canvas, bd=0, highlightthickness=0, bg=bg, font=font, relief='flat')
        if show:
            entry.config(show=show)
        canvas.create_window(100, 15, window=entry, width=180, height=20)
        return entry_frame, entry
    
    def create_rounded_button(self, text, command, bg=None, fg=None, font=None, width=200, height=25):
        button_frame = tk.Frame(self, bg=D_PINK)
        button_frame.grid_propagate(False)
        canvas = tk.Canvas(button_frame, height=height, width=width, bg=D_PINK, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.create_rounded_rectangle(canvas, 0, 0, width, height, radius=15, outline=BLACK, width=2, fill=bg)
        label = tk.Label(canvas, text=text, bg=bg, fg=fg, font=font)
        label.bind("<Button-1>", lambda event: command())
        canvas.create_window(width/2, height/2, window=label, width=width-20, height=height-10)
        return button_frame
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    
    def login(self):
        username = self.get_username()
        password = self.get_password()
        self.login_func(username, password)
    
    def register_(self):
        username = self.get_username()
        password = self.get_password()
        confirm_password = self.get_confirm_password()
        self.register_func(username, password, confirm_password)

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def get_username(self):
        return self.username_entry_widget.get()

    def get_password(self):
        return self.password_entry_widget.get()
    
    def get_confirm_password(self):
        return self.confirm_password_entry_widget.get()

class GUI(tk.Tk):
    def __init__(self, login_func, register_func):
        super().__init__()
        self.title("Login Page")
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(bg=D_PINK)
        self.login_page = Login(login_func=login_func, register_func=register_func, master=self)
        self.login_page.pack(expand=True)


    def run(self):
        self.mainloop()

