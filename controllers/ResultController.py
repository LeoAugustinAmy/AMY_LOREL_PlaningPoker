import json
from tkinter import filedialog
from views.CustomPopup import CustomPopup

class ResultController:
    """!
    @brief Contrôleur dédié à la vue des résultats (ResultView).
    @details Gère l'affichage du récapitulatif et la sauvegarde finale.
    @attributes
        model Modèle de session de jeu.
        main_controller Contrôleur principal pour la navigation.
    """

    def __init__(self, game_session, main_controller):
        """!
        @brief Initialise le ResultController.
        @param game_session Instance du modèle GameSession.
        @param main_controller Instance du MainController.
        @note Ne déclenche aucune I/O, ne fait que stocker les références.
        """
        self.model = game_session
        self.main_controller = main_controller

    def get_results(self):
        """!
        @brief Récupère le dictionnaire des résultats validés.
        @return Dictionnaire {feature: score}.
        @example
            results = controller.get_results()
        """
        return self.model.validated_features

    def save_results(self):
        """!
        @brief Exporte les résultats finaux en JSON avec le statut FINISHED.
        @return None
        @note Ouvre une boîte de dialogue de sauvegarde ; l'utilisateur peut annuler.
        @raises OSError Si l'écriture du fichier échoue.
        """
        data = self.model.to_dict(status="FINISHED")
        
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
        @return None
        @see MainController.show_home
        """
        self.main_controller.show_home()