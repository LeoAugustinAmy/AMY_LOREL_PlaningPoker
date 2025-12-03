import customtkinter as ctk
from views.HeaderView import HeaderView
from views.HomeView import HomeView
from views.SetupView import SetupView
from views.GameView import GameView
from views.ResultView import ResultView
from views.SummaryView import SummaryView

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AMY LOREL Planning Poker")
        self.geometry("900x700")
        
        # header (row 0) fixe, contenu (row 1) extensible
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.controller = None
        self.frames = {}

        # Header commun
        self.header = HeaderView(parent=self, controller=None)
        self.header.grid(row=0, column=0, sticky="ew")

        # Pages placées sous le header
        for F in (HomeView, SetupView):
            page_name = F.__name__
            frame = F(parent=self, controller=None)
            self.frames[page_name] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame("HomeView")

    def set_controller(self, controller):
        self.controller = controller
        # transmettre le controller au header et aux pages
        self.header.controller = controller
        for frame in self.frames.values():
            frame.controller = controller

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def quit_app(self):
        self.destroy()