from models.GameSession import GameSession
from controllers.SetupController import SetupController
from controllers.GameController import GameController
from controllers.ResultController import ResultController # <--- Import du ResultController

class MainController:
    """!
    @brief Contrôleur Principal de l'application.
    @details Gère le cycle de vie de l'application, l'instanciation des modèles et la navigation globale.
    """

    def __init__(self, view):
        """!
        @brief Initialise le MainController.
        @param view L'instance de la fenêtre principale (MainWindow).
        """
        self.view = view
        self.game_session = GameSession() 
        
        # Instanciation de TOUS les sous-contrôleurs
        self.setup_controller = SetupController(self.game_session, self)
        self.game_controller = GameController(self.game_session, self)
        self.result_controller = ResultController(self.game_session, self) # <--- Instanciation

    def show_home(self):
        """Affiche la vue d'accueil."""
        self.view.show_frame("HomeView")

    def show_setup(self):
        """Affiche la vue de configuration avec RESET."""
        self.game_session.reset()      
        self.game_controller.reset()   
        
        setup_frame = self.view.frames["SetupView"]
        setup_frame.controller = self.setup_controller
        setup_frame.refresh_ui()
        self.view.show_frame("SetupView")

    def show_game(self):
        """Affiche la vue du jeu."""
        game_frame = self.view.frames["GameView"]
        game_frame.controller = self.game_controller 
        game_frame.refresh_ui()
        self.view.show_frame("GameView")

    def show_result(self): # <--- LA MÉTHODE MANQUANTE
        """!
        @brief Affiche la vue des résultats de fin de partie.
        """
        result_frame = self.view.frames["ResultView"]
        result_frame.controller = self.result_controller
        result_frame.refresh_ui()
        self.view.show_frame("ResultView")

    def quit_app(self):
        self.view.quit_app()