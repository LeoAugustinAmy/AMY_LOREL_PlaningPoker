from models.Player import Player
from models.Backlog import Backlog
from models.GameRules import GameRules

class GameSession:
    """!
    @brief Modèle principal contenant toute la data vive de la partie.
    """

    def __init__(self):
        """!
        @brief Initialise une nouvelle session de jeu.
        """
        self.reset() # On utilise reset pour l'initialisation aussi

    def reset(self):
        """!
        @brief Réinitialise la session à zéro pour une nouvelle partie.
        @details Vide les joueurs, recrée un backlog vide, remet les règles par défaut et vide les scores.
        """
        self.players = []
        self.backlog = Backlog()
        self.rules = GameRules()
        
        # --- État du Jeu ---
        self.current_feature_index = 0
        self.current_round_number = 1
        self.votes = {} 
        self.validated_features = {}

    def add_player(self, name):
        """!
        @brief Ajoute un joueur à la session.
        @param name Le nom du joueur.
        @return True si l'ajout est un succès, False si le nom est invalide ou déjà pris.
        """
        if not name or any(p.name == name for p in self.players):
            return False
        self.players.append(Player(name))
        return True

    def remove_player(self, name):
        """!
        @brief Supprime un joueur de la session.
        @param name Le nom du joueur à supprimer.
        """
        self.players = [p for p in self.players if p.name != name]

    def get_player_names(self):
        """!
        @brief Récupère la liste des noms des joueurs.
        @return Une liste de chaînes de caractères contenant les noms.
        """
        return [p.name for p in self.players]

    # --- Logique Jeu ---

    def get_current_feature(self):
        """!
        @brief Récupère la fonctionnalité (User Story) en cours de vote.
        @return Le nom de la fonctionnalité ou None si le backlog est terminé.
        """
        if 0 <= self.current_feature_index < len(self.backlog.features):
            return self.backlog.features[self.current_feature_index]
        return None

    def save_feature_score(self, score):
        """!
        @brief Enregistre le score validé pour la fonctionnalité courante.
        @param score La valeur finale retenue (int ou str).
        """
        feature = self.get_current_feature()
        if feature:
            self.validated_features[feature] = score
    
    def next_feature(self):
        """!
        @brief Passe à la fonctionnalité suivante.
        @details Réinitialise le compteur de tours à 1 et vide les votes.
        """
        self.current_feature_index += 1
        self.current_round_number = 1 
        self.votes = {}

    def next_round(self):
        """!
        @brief Passe au tour de vote suivant pour la MÊME fonctionnalité.
        @details Incrémente le compteur de tours et vide les votes pour revoter.
        """
        self.current_round_number += 1
        self.votes = {}