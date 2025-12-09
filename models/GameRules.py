class GameRules:
    """!
    @brief Gère les règles de validation pour le Planning Poker.
    @attributes
        available_modes Modes de validation disponibles.
        selected_mode Mode actuellement sélectionné.
    """

    def __init__(self):
        """!
        @brief Initialise les règles par défaut.
        @details Définit la liste des modes disponibles et sélectionne 'Unanimité' par défaut.
        @example
            rules = GameRules()
        """
        self.available_modes = ["Unanimité", "Majorité Absolue", "Majorité Relative", "Médiane", "Moyenne"]
        self.selected_mode = "Unanimité"

    def set_mode(self, mode):
        """!
        @brief Définit le mode de validation choisi.
        @param mode Le nom du mode à appliquer.
        @raises ValueError Si le mode n'est pas reconnu.
        """
        if mode in self.available_modes:
            self.selected_mode = mode
        else:
            raise ValueError(f"Mode inconnu: {mode}")