class Player:
    """!
    @brief Représente un joueur dans la session de jeu.
    @attributes
        name Nom du joueur.
    """

    def __init__(self, name):
        """!
        @brief Constructeur de la classe Player.
        @param name Le nom du joueur.
        @example
            player = Player("Alice")
        """
        self.name = name