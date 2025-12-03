class Backlog:
    """!
    @brief Gère la liste des fonctionnalités (User Stories) à estimer.
    """

    def __init__(self):
        """!
        @brief Initialise un backlog vide.
        """
        self.features = []

    def add_feature(self, name):
        """!
        @brief Ajoute une fonctionnalité au backlog.
        @param name Le nom ou la description de la fonctionnalité.
        @return True si l'ajout a réussi, False si le nom est vide ou existe déjà.
        """
        if name and name not in self.features:
            self.features.append(name)
            return True
        return False

    def remove_feature(self, name):
        """!
        @brief Supprime une fonctionnalité du backlog.
        @param name Le nom de la fonctionnalité à retirer.
        """
        if name in self.features:
            self.features.remove(name)