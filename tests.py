"""!
@file tests.py
@brief Suite de tests unitaires pour les modèles et la logique de jeu.
"""

import unittest
from unittest.mock import MagicMock

from models.GameSession import GameSession
from controllers.GameController import GameController


class TestModels(unittest.TestCase):
    """!
    @brief Tests unitaires pour les modèles de données (Player, Backlog, GameSession).
    """

    def setUp(self):
        """!
        @brief Prépare une session de jeu fraîche avant chaque test.
        """
        self.session = GameSession()

    def test_player_management(self):
        """!
        @brief Vérifie l'ajout et la suppression de joueurs.
        """
        self.assertTrue(self.session.add_player("Alice"))
        self.assertTrue(self.session.add_player("Bob"))
        self.assertFalse(self.session.add_player("Alice"))  # Doublon interdit
        self.assertFalse(self.session.add_player(""))       # Nom vide interdit

        self.assertEqual(len(self.session.players), 2)
        self.assertEqual(self.session.get_player_names(), ["Alice", "Bob"])

        self.session.remove_player("Alice")
        self.assertEqual(len(self.session.players), 1)
        self.assertEqual(self.session.get_player_names(), ["Bob"])

    def test_backlog_management(self):
        """!
        @brief Vérifie la gestion des User Stories.
        """
        backlog = self.session.backlog
        self.assertTrue(backlog.add_feature("Login Page"))
        self.assertTrue(backlog.add_feature("Logout"))
        self.assertFalse(backlog.add_feature("Login Page"))  # Doublon

        self.assertEqual(len(backlog.features), 2)
        self.assertEqual(self.session.get_current_feature(), "Login Page")

    def test_save_load_serialization(self):
        """!
        @brief Vérifie que to_dict/from_dict sauvegardent et restaurent tout l'état.
        """
        self.session.add_player("Alice")
        self.session.add_player("Bob")
        self.session.backlog.add_feature("Feature A")
        self.session.backlog.add_feature("Feature B")
        self.session.rules.set_mode("Moyenne")
        self.session.current_feature_index = 1
        self.session.validated_features = {"Feature A": 5}

        data = self.session.to_dict(status="PAUSED")

        new_session = GameSession()
        new_session.from_dict(data)

        self.assertEqual(new_session.get_player_names(), ["Alice", "Bob"])
        self.assertEqual(new_session.rules.selected_mode, "Moyenne")
        self.assertEqual(new_session.validated_features["Feature A"], 5)
        self.assertEqual(new_session.get_current_feature(), "Feature B")  # Index restauré


class TestGameLogic(unittest.TestCase):
    """!
    @brief Tests unitaires pour la logique du contrôleur de jeu.
    """

    def setUp(self):
        """!
        @brief Prépare une session et un contrôleur mockés avant chaque test.
        """
        self.session = GameSession()
        self.mock_main_controller = MagicMock()
        self.controller = GameController(self.session, self.mock_main_controller)

        self.session.add_player("Alice")
        self.session.add_player("Bob")
        self.session.add_player("Charlie")
        self.session.backlog.add_feature("User Story 1")

    def test_voting_process(self):
        """!
        @brief Vérifie l'enregistrement des votes et l'avancement du tour.
        """
        self.assertEqual(self.controller.get_current_player_name(), "Alice")

        self.controller.cast_vote("5")
        self.assertEqual(self.controller.get_current_player_name(), "Bob")
        self.assertFalse(self.controller.is_round_finished())

        self.controller.cast_vote("8")
        self.controller.cast_vote("5")
        self.assertTrue(self.controller.is_round_finished())

    def test_rule_unanimous_round_one(self):
        """!
        @brief Tour 1 : unanimité absolue requise.
        """
        self.session.current_round_number = 1

        self.session.votes = {"Alice": "5", "Bob": "5", "Charlie": "8"}
        self.assertIsNone(self.controller.calculate_result())

        self.session.votes = {"Alice": "5", "Bob": "5", "Charlie": "5"}
        self.assertEqual(self.controller.calculate_result(), 5)

    def test_rule_average_round_two(self):
        """!
        @brief Tour 2+ : mode Moyenne, moyenne arrondie.
        """
        self.session.current_round_number = 2
        self.session.rules.set_mode("Moyenne")

        self.session.votes = {"Alice": "3", "Bob": "5", "Charlie": "8"}
        self.assertEqual(self.controller.calculate_result(), 5)

    def test_rule_absolute_majority(self):
        """!
        @brief Tour 2+ : mode Majorité Absolue (>50%).
        """
        self.session.current_round_number = 2
        self.session.rules.set_mode("Majorité Absolue")

        self.session.votes = {"Alice": "5", "Bob": "5", "Charlie": "8"}
        self.assertEqual(self.controller.calculate_result(), 5)

        self.session.votes = {"Alice": "3", "Bob": "5", "Charlie": "8"}
        self.assertIsNone(self.controller.calculate_result())

    def test_coffee_break_rule(self):
        """!
        @brief Règle spéciale : tout le monde vote café => sauvegarde.
        """
        self.session.votes = {"Alice": "cafe", "Bob": "cafe", "Charlie": "cafe"}
        self.controller.save_game_state_and_quit = MagicMock()

        result = self.controller.handle_end_of_round()

        self.assertEqual(result, "COFFEE")
        self.controller.save_game_state_and_quit.assert_called_once()

    def test_ignore_special_cards_in_calc(self):
        """!
        @brief Les cartes '?' et 'cafe' sont ignorées dans les calculs numériques.
        """
        self.session.current_round_number = 2
        self.session.rules.set_mode("Moyenne")

        self.session.votes = {"Alice": "5", "Bob": "13", "Charlie": "interro"}
        self.assertEqual(self.controller.calculate_result(), 9)


if __name__ == '__main__':
    unittest.main()