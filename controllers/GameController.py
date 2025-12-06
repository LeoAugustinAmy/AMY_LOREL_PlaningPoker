from statistics import mean, median, multimode
import json
from tkinter import filedialog
from views.CustomPopup import CustomPopup

class GameController:
    """!
    @brief Gère la logique de la phase de jeu (Votes, Révélation, Calculs, Règles Spéciales).
    """

    def __init__(self, game_session, main_controller):
        """!
        @brief Initialise le GameController.
        @param game_session Instance du modèle GameSession.
        @param main_controller Instance du MainController.
        """
        self.model = game_session
        self.main_controller = main_controller
        
        self.deck = ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "interro", "cafe"]
        
        self.reset()

    def reset(self):
        """!
        @brief Réinitialise l'état interne du contrôleur (index joueur, état révélation).
        """
        self.current_player_index = 0
        self.revealed = False

    def get_current_feature_name(self):
        """!
        @brief Récupère le nom de la fonctionnalité courante.
        """
        return self.model.get_current_feature()

    def get_current_player_name(self):
        """!
        @brief Retourne le nom du joueur qui doit voter.
        """
        players = self.model.get_player_names()
        if self.current_player_index < len(players):
            return players[self.current_player_index]
        return None

    def cast_vote(self, card_value):
        """!
        @brief Enregistre le vote du joueur courant et passe au suivant.
        """
        player_name = self.get_current_player_name()
        if player_name:
            self.model.votes[player_name] = card_value
            self.current_player_index += 1
            return True
        return False

    def is_round_finished(self):
        """!
        @brief Vérifie si tous les joueurs ont voté.
        """
        return self.current_player_index >= len(self.model.players)

    def get_votes(self):
        """!
        @brief Récupère les votes actuels.
        """
        return self.model.votes

    def check_coffee_break(self):
        """!
        @brief Vérifie la règle spéciale 'Pause Café'.
        """
        votes = list(self.model.votes.values())
        if not votes: return False
        return all(v == "cafe" for v in votes)

    def calculate_result(self):
        """!
        @brief Calcule le résultat du vote selon les règles (Unanimité au T1, puis règle choisie).
        """
        votes_values = [v for v in self.model.votes.values() if v not in ["interro", "cafe"]]
        
        numeric_votes = []
        for v in votes_values:
            if v.isdigit(): numeric_votes.append(int(v))
        
        if self.model.current_round_number == 1:
            if not numeric_votes: return None 
            if len(set(numeric_votes)) == 1:
                return numeric_votes[0] 
            else:
                return None 

        if not numeric_votes: return "?"

        mode = self.model.rules.selected_mode
        
        if mode == "Unanimité":
            return numeric_votes[0] if len(set(numeric_votes)) == 1 else None
        elif mode == "Moyenne":
            return round(mean(numeric_votes))
        elif mode == "Médiane":
            return round(median(numeric_votes))
        elif mode == "Majorité Absolue":
            counts = {x: numeric_votes.count(x) for x in set(numeric_votes)}
            winner = max(counts, key=counts.get)
            if counts[winner] > len(numeric_votes) / 2:
                return winner
            return None 
        elif mode == "Majorité Relative":
            res = multimode(numeric_votes)
            return max(res)

        return None

    def handle_end_of_round(self):
        """!
        @brief Orchestre la fin du tour (Café, Calcul ou Revote).
        """
        if self.check_coffee_break():
            self.save_game_state_and_quit()
            return "COFFEE"

        result = self.calculate_result()

        if result is not None:
            return result
        else:
            return "REVOTE"

    def validate_feature(self, final_score):
        """!
        @brief Valide la fonctionnalité avec le score final et passe à la suivante.
        """
        self.model.save_feature_score(final_score)
        self.model.next_feature()
        self._reset_round_state()

        if self.model.get_current_feature() is None:
            self.finish_game()
        else:
            self.main_controller.show_game()

    def restart_round(self):
        """!
        @brief Relance un vote pour la même fonctionnalité (Tour suivant).
        """
        self.model.next_round()
        self._reset_round_state()
        self.main_controller.show_game()

    def _reset_round_state(self):
        self.current_player_index = 0
        self.revealed = False
        self.model.votes = {}

    def save_game_state_and_quit(self):
        """!
        @brief Sauvegarde l'état complet (PAUSED) et revient à l'accueil.
        """
        data = self.model.to_dict(status="PAUSED")
        self._export_json(data, "Partie mise en pause (Café) !")
        self.main_controller.show_home()

    def finish_game(self):
        """!
        @brief Fin de partie : Redirige vers la page de résultats.
        """
        self.main_controller.show_result()

    def _export_json(self, data, success_msg):
        """!
        @brief Utilitaire d'export JSON avec popup.
        """
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                CustomPopup("Succès", success_msg, type="info")
            except Exception as e:
                CustomPopup("Erreur", f"Erreur sauvegarde: {e}", type="error")