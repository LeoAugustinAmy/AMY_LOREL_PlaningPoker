from models.GameSession import GameSession
from controllers.SetupController import SetupController
from controllers.GameController import GameController

class MainController:
    """!
    @brief Contrôleur Principal de l'application.
    @details Gère le cycle de vie, les données partagées (GameSession) et l'instanciation des sous-contrôleurs.
    """

    def __init__(self, view):
        """!
        @brief Initialise le MainController et tous les sous-contrôleurs.
        """
        self.view = view
        
        self.game_session = GameSession() 
        
        self.setup_controller = SetupController(self.game_session, self)
        self.game_controller = GameController(self.game_session, self) 

    def show_home(self):
        """!
        @brief Affiche la vue d'accueil.
        """
        self.view.show_frame("HomeView")

    def show_setup(self):
        """!
        @brief Affiche la vue de configuration (Nouvelle Partie).
        @details ATTENTION : Réinitialise (RESET) toute la session de jeu avant d'afficher l'écran.
        Cela corrige le bug où l'ancienne partie persistait.
        """
        # --- C'EST ICI QUE LE FIX SE FAIT ---
        self.game_session.reset()      # Vide le modèle (joueurs, backlog...)
        self.game_controller.reset()   # Vide le contrôleur (index joueur...)
        # ------------------------------------

        setup_frame = self.view.frames["SetupView"]
        setup_frame.controller = self.setup_controller
        setup_frame.refresh_ui()
        self.view.show_frame("SetupView")

    def show_game(self):
        """!
        @brief Affiche la vue du jeu.
        """
        game_frame = self.view.frames["GameView"]
        game_frame.controller = self.game_controller 
        game_frame.refresh_ui()
        self.view.show_frame("GameView")

    def quit_app(self):
        """!
        @brief Ferme l'application.
        """
        self.view.quit_app()