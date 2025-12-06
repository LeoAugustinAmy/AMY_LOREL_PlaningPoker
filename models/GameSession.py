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
        @details Appelle reset() pour mettre l'état à zéro dès la création.
        """
        self.reset()

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

    def to_dict(self, status="IN_PROGRESS"):
        """!
        @brief Convertit l'état complet de la session en dictionnaire pour l'export JSON.
        @param status Le statut de la partie ("IN_PROGRESS", "FINISHED", "PAUSED").
        @return Un dictionnaire contenant toutes les données nécessaires à la restauration.
        """
        return {
            "status": status,
            "rules": self.rules.selected_mode,
            "players": [p.name for p in self.players],
            "backlog": self.backlog.features,
            "current_feature_index": self.current_feature_index,
            "current_round_number": self.current_round_number,
            "validated_features": {str(k): v for k, v in self.validated_features.items()}
        }

    def from_dict(self, data):
        """!
        @brief Restaure l'état de la session depuis un dictionnaire.
        @param data Le dictionnaire chargé depuis le fichier JSON.
        """
        self.reset()
        
        if "rules" in data:
            self.rules.set_mode(data["rules"])
        
        for p_name in data.get("players", []):
            self.add_player(p_name)
            
        for feat in data.get("backlog", []):
            self.backlog.add_feature(feat)
            
        self.current_feature_index = data.get("current_feature_index", 0)
        self.current_round_number = data.get("current_round_number", 1)
        
        self.validated_features = data.get("validated_features", {})

    def add_player(self, name):
        """!
        @brief Ajoute un joueur à la session.
        @param name Le nom du joueur.
        @return True si l'ajout est un succès, False sinon.
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
        @return Une liste de chaînes de caractères.
        """
        return [p.name for p in self.players]

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
        @brief Passe au tour de vote suivant pour la même fonctionnalité.
        @details Incrémente le compteur de tours et vide les votes pour revoter.
        """
        self.current_round_number += 1
        self.votes = {}