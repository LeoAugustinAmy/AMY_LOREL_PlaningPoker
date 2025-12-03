import json
from tkinter import filedialog
from models.GameSession import GameSession
from controllers.SetupController import SetupController
from controllers.GameController import GameController
from controllers.ResultController import ResultController
from views.CustomPopup import CustomPopup

class MainController:
    """!
    @brief Contrôleur Principal de l'application.
    @details Gère le cycle de vie, la navigation et le chargement de partie.
    """

    def __init__(self, view):
        """!
        @brief Initialise le MainController et tous les sous-contrôleurs.
        """
        self.view = view
        self.game_session = GameSession() 
        
        self.setup_controller = SetupController(self.game_session, self)
        self.game_controller = GameController(self.game_session, self)
        self.result_controller = ResultController(self.game_session, self) # Instanciation indispensable

    def show_home(self):
        """!
        @brief Affiche la vue d'accueil.
        """
        self.view.show_frame("HomeView")

    def show_setup(self):
        """!
        @brief Affiche la vue de configuration (Nouvelle Partie).
        @details RESET impératif pour ne pas garder l'état de l'ancienne partie.
        """
        self.game_session.reset()      
        self.game_controller.reset()   
        
        setup_frame = self.view.frames["SetupView"]
        setup_frame.controller = self.setup_controller
        setup_frame.refresh_ui()
        self.view.show_frame("SetupView")

    def load_game(self):
        """!
        @brief Charge une partie depuis un fichier JSON et redirige vers la bonne vue.
        @details Si la partie est FINISHED -> ResultView. Sinon -> GameView.
        """
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filename:
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. On restaure le modèle
            self.game_session.from_dict(data)
            self.game_controller.reset() # On reset les index de voteurs temporaires

            # 2. Analyse du statut pour savoir où aller
            status = data.get("status", "IN_PROGRESS")

            if status == "FINISHED":
                CustomPopup("Chargement", "Partie terminée chargée. Affichage des résultats.", type="info")
                self.show_result()
            
            else:
                # Vérification s'il reste des choses à faire
                if self.game_session.get_current_feature():
                    CustomPopup("Chargement", "Partie reprise avec succès !", type="info")
                    self.show_game()
                else:
                    self.show_result()

        except Exception as e:
            CustomPopup("Erreur", f"Impossible de charger la partie :\n{e}", type="error")

    def show_game(self):
        """!
        @brief Affiche la vue du jeu.
        """
        game_frame = self.view.frames["GameView"]
        game_frame.controller = self.game_controller 
        game_frame.refresh_ui()
        self.view.show_frame("GameView")

    def show_result(self): 
        """!
        @brief Affiche la vue des résultats de fin de partie.
        @details C'est la méthode qui manquait et causait le crash.
        """
        result_frame = self.view.frames["ResultView"]
        result_frame.controller = self.result_controller
        result_frame.refresh_ui()
        self.view.show_frame("ResultView")

    def quit_app(self):
        """!
        @brief Quitte l'application.
        """
        self.view.quit_app()