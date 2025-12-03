import customtkinter as ctk
from views.HeaderView import HeaderView
from views.HomeView import HomeView
from views.SetupView import SetupView
from views.GameView import GameView
from views.ResultView import ResultView

class MainWindow(ctk.CTk):
    """!
    @brief Fenêtre principale de l'application.
    @details Hérite de CTk. Gère le conteneur principal et la navigation entre les différentes frames.
    """

    def __init__(self):
        """!
        @brief Constructeur de la fenêtre principale.
        @details Configure la géométrie, le titre, le header commun et instancie toutes les vues.
        """
        super().__init__()
        self.title("AMY LOREL Planning Poker")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.controller = None
        self.frames = {}

        self.header = HeaderView(parent=self, controller=None)
        self.header.grid(row=0, column=0, sticky="ew")

        # Instanciation de toutes les vues
        for F in (HomeView, SetupView, GameView, ResultView):
            page_name = F.__name__
            frame = F(parent=self, controller=None)
            self.frames[page_name] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame("HomeView")

    def set_controller(self, main_controller):
        """!
        @brief Injecte les dépendances de contrôleurs dans les vues.
        """
        self.controller = main_controller
        self.header.controller = main_controller

        if "HomeView" in self.frames:
            self.frames["HomeView"].controller = main_controller
        if "SetupView" in self.frames:
            self.frames["SetupView"].controller = main_controller.setup_controller
        if "GameView" in self.frames:
            self.frames["GameView"].controller = main_controller.game_controller
        if "ResultView" in self.frames:
            self.frames["ResultView"].controller = main_controller.result_controller

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def quit_app(self):
        self.destroy()