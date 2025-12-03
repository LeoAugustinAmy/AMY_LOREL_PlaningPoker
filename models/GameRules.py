class GameRules:
    """!
    @brief Gère les règles de validation pour le Planning Poker.
    """

    def __init__(self):
        """!
        @brief Initialise les règles par défaut.
        @details Définit la liste des modes disponibles et sélectionne 'Unanimité' par défaut.
        """
        self.available_modes = ["Unanimité", "Majorité Absolue", "Majorité Relative", "Médiane", "Moyenne"]
        self.selected_mode = "Unanimité"

    def set_mode(self, mode):
        """!
        @brief Définit le mode de validation choisi.
        @param mode Le nom du mode à appliquer.
        """
        if mode in self.available_modes:
            self.selected_mode = mode