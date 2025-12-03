from models.GameSession import GameSession
from controllers.SetupController import SetupController

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
        self.setup_controller = SetupController(self.game_session, self)

    def show_home(self):
        """!
        @brief Affiche la vue d'accueil.
        """
        self.view.show_frame("HomeView")

    def show_setup(self):
        """!
        @brief Affiche la vue de configuration.
        @details Configure le contrôleur de la vue Setup et force un rafraîchissement de l'interface.
        """
        setup_frame = self.view.frames["SetupView"]
        setup_frame.controller = self.setup_controller
        setup_frame.refresh_ui()
        self.view.show_frame("SetupView")

    def show_game(self):
        """!
        @brief Affiche la vue du jeu.
        """
        self.view.show_frame("GameView")

    def quit_app(self):
        """!
        @brief Ferme l'application.
        """
        self.view.quit_app()