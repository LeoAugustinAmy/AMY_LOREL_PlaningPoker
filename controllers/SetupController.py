import json
from tkinter import filedialog
from views.CustomPopup import CustomPopup

class SetupController:
    """!
    @brief Contrôleur dédié à la vue de configuration (SetupView).
    @details Gère les interactions utilisateur liées à l'ajout de joueurs, de tâches, et l'import/export.
    @attributes
        model Le modèle de session en cours.
        main_controller Contrôleur principal pour la navigation.
    """

    def __init__(self, game_session, main_controller):
        """!
        @brief Initialise le SetupController.
        @param game_session Instance du modèle GameSession.
        @param main_controller Instance du contrôleur principal pour la navigation.
        @note Ne réinitialise pas le modèle ; utile pour un chargement de partie.
        """
        self.model = game_session
        self.main_controller = main_controller

    def add_player(self, name):
        """!
        @brief Demande au modèle d'ajouter un joueur.
        @param name Nom du joueur.
        @return True si succès, False sinon.
        @raises ValueError Si le nom est vide ou déjà utilisé.
        """
        return self.model.add_player(name)

    def remove_player(self, name):
        """!
        @brief Demande au modèle de supprimer un joueur.
        @param name Nom du joueur.
        @note Ne lève pas d'exception si le joueur n'existe pas.
        """
        self.model.remove_player(name)
        
    def get_players(self):
        """!
        @brief Récupère la liste des joueurs actuels.
        @return Liste des noms des joueurs.
        @example
            players = controller.get_players()
        """
        return self.model.get_player_names()

    def add_feature(self, name):
        """!
        @brief Demande au modèle d'ajouter une fonctionnalité au backlog.
        @param name Description de la fonctionnalité.
        @return True si succès, False sinon.
        @raises ValueError Si la fonctionnalité est vide ou dupliquée.
        """
        return self.model.backlog.add_feature(name)

    def remove_feature(self, name):
        """!
        @brief Demande au modèle de supprimer une fonctionnalité.
        @param name Description de la fonctionnalité.
        @note Ignore silencieusement les noms inexistants.
        """
        self.model.backlog.remove_feature(name)

    def get_features(self):
        """!
        @brief Récupère la liste des fonctionnalités du backlog.
        @return Liste des chaînes de caractères.
        @example
            features = controller.get_features()
        """
        return self.model.backlog.features

    def get_available_rules(self):
        """!
        @brief Récupère les modes de jeu disponibles.
        @return Liste des modes de validation.
        @see GameRules.available_modes
        """
        return self.model.rules.available_modes

    def set_rule(self, rule_name):
        """!
        @brief Définit la règle du jeu choisie.
        @param rule_name Nom de la règle.
        @raises ValueError Si la règle est inconnue.
        """
        self.model.rules.set_mode(rule_name)

    def export_data(self):
        """!
        @brief Exporte les données de la session (joueurs, backlog, règle) dans un fichier JSON.
        @details Ouvre une boîte de dialogue pour choisir l'emplacement de sauvegarde.
        @raises OSError Si l'écriture du fichier échoue.
        """
        data = {
            "players": self.get_players(),
            "features": self.get_features(),
            "rule": self.model.rules.selected_mode
        }
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                CustomPopup("Export Réussi", "La partie a été sauvegardée avec succès !", type="info")
            except Exception as e:
                CustomPopup("Erreur d'export", f"Une erreur est survenue :\n{e}", type="error")
    
    def import_data(self):
        """!
        @brief Importe les données d'une session depuis un fichier JSON.
        @details Ouvre une boîte de dialogue pour choisir le fichier et met à jour le modèle.
        @return True si l'import a réussi, False sinon.
        @raises ValueError Si le fichier ne contient pas les clés attendues.
        """
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    self.model.players.clear()
                    self.model.backlog.features.clear()
                    
                    for p in data.get("players", []):
                        self.model.add_player(p)
                    for feat in data.get("features", []):
                        self.model.backlog.add_feature(feat)
                    
                    rule = data.get("rule")
                    if rule:
                        self.set_rule(rule)

                CustomPopup("Import Réussi", "Données chargées avec succès !", type="info")
                return True
            except Exception as e:
                CustomPopup("Erreur d'import", f"Le fichier est corrompu :\n{e}", type="error")
                return False
        return False

    def start_game(self):
        """!
        @brief Vérifie les conditions et affiche une alerte CustomPopup si nécessaire.
        """
        if len(self.model.players) >= 2 and self.model.backlog.features:
            self.main_controller.show_game()
        else:
            CustomPopup("Impossible de lancer", 
                        "Pour démarrer, il faut :\n• au moins 2 joueurs\n• au moins 1 fonctionnalité", 
                        type="warning")