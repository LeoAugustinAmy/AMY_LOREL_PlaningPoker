from models.Player import Player
from models.Backlog import Backlog
from models.GameRules import GameRules

class GameSession:
    """!
    @brief Classe principale du Modèle regroupant toutes les données d'une session de jeu.
    """

    def __init__(self):
        """!
        @brief Initialise une nouvelle session de jeu.
        @details Crée les instances pour les joueurs, le backlog et les règles.
        """
        self.players = []
        self.backlog = Backlog()
        self.rules = GameRules()

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