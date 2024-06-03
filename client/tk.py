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

username_ = ""

class Login(tk.Frame):
    def __init__(self, login_func, register_func, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login")
        self.configure(bg=D_PINK)
        self.custom_font = self.master.custom_font
        self.create_widgets()
        self.center_window()
        ### MUSS ZUERST GESETZT WERDEN ###
        self.login_func: function = login_func
        self.register_func: function = register_func

    
    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username", bg=D_PINK, fg=BLACK, font=self.custom_font)
        self.username_label.pack(padx=10, pady=(10, 2))

        self.username_entry_canvas, self.username_entry_widget = self.master.create_rounded_entry(self, font=self.custom_font, bg=L_PINK)
        self.username_entry_canvas.pack(padx=10, pady=(2, 10))

        self.password_label = tk.Label(self, text="Password", bg=D_PINK, fg=BLACK, font=self.custom_font)
        self.password_label.pack(padx=10, pady=(10, 2))

        self.password_entry_canvas, self.password_entry_widget = self.master.create_rounded_entry(self, show="*", font=self.custom_font, bg=L_PINK)
        self.password_entry_canvas.pack(padx=10, pady=(2, 10))

        self.register_label = tk.Label(self, text="Don't have an account? Register here", bg=D_PINK, fg=BLACK, font=self.custom_font, cursor="hand2")
        self.register_label.pack(side=tk.BOTTOM)

        self.login_button = self.master.create_rounded_button(self, "Login", self.login, bg=L_PINK, fg=BLACK, font=self.custom_font, width=150, height=40)
        self.login_button.pack(side=tk.BOTTOM, pady=(0, 10))

        self.register_button = self.master.create_rounded_button(self, "Register", self.register_, bg=L_PINK, fg=BLACK, font=self.custom_font, width=150, height=40)
        self.register_button.pack(side=tk.BOTTOM, pady=(0, 10))
        self.register_button.pack_forget()

        self.register_label.bind("<Button-1>", self.register_clicked)

    def register_clicked(self, event):
        self.login_button.pack_forget()
        self.register_button.pack(side=tk.BOTTOM, pady=(0, 10))
            
        self.confirm_password_label = tk.Label(self, text="Confirm Password", bg=D_PINK, fg=BLACK, font=self.custom_font)
        self.confirm_password_label.pack(padx=10, pady=(10, 2))
        
        self.confirm_password_entry_canvas, self.confirm_password_entry_widget = self.master.create_rounded_entry(self, show="*", font=self.custom_font, bg=L_PINK)
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


    
    def login(self):
        global username_
        username = self.get_username()
        password = self.get_password()
        res = self.login_func(username, password)
        if res.status_code != 200:
            msg = res.json().get("message")
            self.master.create_popup(f"Login failed: {msg}" , timeout=10)
            return
        elif res.status_code == 200:
            self.master.switch_to_game(popup_message=f"Logged in successfully: {username}")
            username_ = username
        else:
            self.master.create_popup(f"Login failed: An unknown error occurred", timeout=10)
    
    def register_(self):
        username = self.get_username()
        password = self.get_password()
        confirm_password = self.get_confirm_password()
        if password != confirm_password:
            self.master.create_popup("Passwords do not match", timeout=3)
            return
        res = self.register_func(username, password, confirm_password)
        if res.status_code != 200:
            msg = res.json().get("message")
            self.master.create_popup(f"Register failed: {msg}" , timeout=10)
            return
        elif res.status_code == 200:
            self.master.switch_to_game(popup_message=f"Registered successfully: {username}")
        else:
            self.master.create_popup(f"Register failed: An unknown error occurred", timeout=10)

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

class Game(tk.Frame):
    def __init__(self, init_lb_func, play_func, master=None):
        super().__init__(master)
        self.master = master
        self.master.current_screen = "game"
        self.master.title("Game")
        self.configure(bg=D_PINK)
        self.custom_font = self.master.custom_font
        self.add_labels(init_lb_func())
        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.play_func = play_func


    def create_widgets(self):
        stake_label = tk.Label(self, text="Stake", bg=D_PINK, fg=BLACK, font=self.custom_font)
        stake_label.pack(side=tk.TOP, anchor=tk.CENTER)

        stake_entry_canvas, stake_entry_widget = self.master.create_rounded_entry(self, font=self.custom_font, bg=L_PINK)
        stake_entry_canvas.pack(side=tk.TOP, anchor=tk.CENTER)
        stake_entry_widget.insert(0, "20")

        play_button = self.master.create_rounded_button(self, "Play", self.play, bg=L_PINK, fg=BLACK, font=self.custom_font, width=150, height=40)
        play_button.pack(side=tk.TOP, pady=(10, 0))

    def add_labels(self, data):
        leaderboard_label = tk.Label(self, text="Leaderboard", bg=D_PINK, fg=BLACK, font=self.custom_font)
        leaderboard_label.pack(side=tk.TOP, anchor=tk.NW)
        for item in data:
            label = tk.Label(self, text=f"{item.get('id')}: {item.get('money')}", bg=D_PINK, fg=BLACK, font=self.custom_font)
            label.pack(side=tk.TOP, anchor=tk.W)

    def get_stake(self):
        return self.stake_entry_widget.get()
    
    def play(self):
        stake = self.get_stake()
        try:
            stake = int(stake)
        except ValueError:
            self.master.create_popup("Invalid stake", timeout=3)
            return
        res = self.play_func(username_, stake)
        print(res.json())

class GUI(tk.Tk):
    def __init__(self, login_func, register_func, init_lb_func, play_func):
        super().__init__()
        self.title("")
        self.geometry("800x600")
        self.resizable(False, False)
        self.load_custom_font()
        self.configure(bg=D_PINK)
        self.login_page = Login(login_func=login_func, register_func=register_func, master=self)
        self.login_page.pack(expand=True)
        self.current_popup = None
        self.current_screen = "login"
        self.init_lb_func = init_lb_func
        self.play_func = play_func


    
    def create_rounded_entry(self, parent, show=None, font=None, bg=None):
        entry_frame = tk.Frame(parent, bg=D_PINK)
        entry_frame.grid_propagate(False)
        canvas = tk.Canvas(entry_frame, height=30, width=200, bg=D_PINK, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.create_rounded_rectangle(canvas, 0, 0, 200, 30, radius=15, outline=BLACK, width=2, fill=bg)
        entry = tk.Entry(canvas, bd=0, highlightthickness=0, bg=bg, font=font, relief='flat')
        if show:
            entry.config(show=show)
        canvas.create_window(100, 15, window=entry, width=180, height=20)
        return entry_frame, entry
    
    def create_rounded_button(self, parent, text, command, bg=None, fg=None, font=None, width=200, height=25):
        button_frame = tk.Frame(parent, bg=D_PINK)
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
    
    def load_custom_font(self):
        self.custom_font = tkfont.Font(family='Ubuntu Sans Mono', size=12)

    def switch_to_game(self, popup_message=None):
        self.login_page.destroy()
        self.game_page = Game(self.init_lb_func, self.play_func, master=self)
        self.game_page.pack(expand=True)
        if popup_message:
            self.create_popup(popup_message, timeout=3)


    def create_popup(self, message, timeout=3):
        if self.current_popup:
            self.current_popup.destroy()
        
        popup_frame = tk.Frame(self, bg=D_PINK, bd=2) 
        popup_frame.place(relx=0.5, rely=0, anchor=tk.N)

        self.current_popup = popup_frame
        
        popup_label = tk.Label(popup_frame, text=message, bg=D_PINK, fg=BLACK, font=self.login_page.custom_font, bd=2, relief=tk.SOLID, padx=2, pady=2)
        popup_label.pack(padx=10, pady=10)
        
        def close_popup():
            popup_frame.destroy()
            self.current_popup = None
        
        self.after(timeout*1000, close_popup)


    def run(self):
        self.mainloop()


