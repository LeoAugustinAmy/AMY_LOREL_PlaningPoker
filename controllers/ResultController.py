import json
from tkinter import filedialog
from views.CustomPopup import CustomPopup

class ResultController:
    """!
    @brief Contrôleur dédié à la vue des résultats (ResultView).
    @details Gère l'affichage du récapitulatif et la sauvegarde finale.
    """

    def __init__(self, game_session, main_controller):
        """!
        @brief Initialise le ResultController.
        @param game_session Instance du modèle GameSession.
        @param main_controller Instance du MainController.
        """
        self.model = game_session
        self.main_controller = main_controller

    def get_results(self):
        """!
        @brief Récupère la liste des fonctionnalités validées et leurs scores.
        @return Dictionnaire {feature_name: score}.
        """
        return self.model.validated_features

    def save_results(self):
        """!
        @brief Exporte les résultats finaux en JSON.
        """
        data = {
            "status": "FINISHED",
            "results": {str(k): v for k, v in self.model.validated_features.items()},
            "players": self.model.get_player_names()
        }
        
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                CustomPopup("Succès", "Résultats sauvegardés avec succès !", type="info")
            except Exception as e:
                CustomPopup("Erreur", f"Erreur lors de la sauvegarde :\n{e}", type="error")

    def go_home(self):
        """!
        @brief Retourne au menu principal.
        """
        self.main_controller.show_home()