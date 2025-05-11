import unittest
from room import Room
from player import Player
from soldier import Soldier
from game import Game


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = Room("A dark, quiet room")

    def test_room_description(self):
        self.assertEqual(self.room.description, "A dark, quiet room")

    def test_room_items(self):
        self.room.add_room_item("sword")
        self.assertIn("sword", self.room.get_room_items())
        self.room.remove_room_item("sword")
        self.assertNotIn("sword", self.room.get_room_items())

    def test_room_clue(self):
        self.room.clue = "This is a clue."
        self.assertEqual(self.room.clue, "This is a clue.")

    def test_room_soldiers(self):
        soldier = Soldier("Guard", 50, 10)
        self.room.add_soldier(soldier)
        self.assertIn(soldier, self.room.get_soldiers())
        self.room.remove_soldier(soldier)
        self.assertNotIn(soldier, self.room.get_soldiers())


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.room = Room("Starting Room")
        self.player = Player(self.room)

    def test_player_health(self):
        self.assertEqual(self.player.health, 100)
        self.player.take_damage(20)
        self.assertEqual(self.player.health, 80)
        self.player.heal(50)
        self.assertEqual(self.player.health, 100)

    def test_equip_shield(self):
        self.assertFalse(self.player.has_shield)
        self.player.equip_shield()
        self.assertTrue(self.player.has_shield)
        self.assertEqual(self.player.max_health, 120)
        self.assertEqual(self.player.health, 120)


class TestSoldier(unittest.TestCase):
    def setUp(self):
        self.soldier = Soldier("Enemy", 50, 10)

    def test_soldier_health(self):
        self.assertEqual(self.soldier.health, 50)
        self.soldier.take_damage(20)
        self.assertEqual(self.soldier.health, 30)
        self.soldier.take_damage(50)
        self.assertEqual(self.soldier.health, 0)

    def test_soldier_is_alive(self):
        self.assertTrue(self.soldier.is_alive())
        self.soldier.take_damage(50)
        self.assertFalse(self.soldier.is_alive())


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_game_initialization(self):
        self.assertIsNotNone(self.game.player)
        self.assertEqual(self.game.player.health, 100)
        self.assertEqual(len(self.game.backpack.contents), 0)

    def test_room_transitions(self):
        self.assertEqual(self.game.player.current_room.description, "You are outside the castle")
        self.game.do_go_command("north")
        self.assertEqual(self.game.player.current_room.description, "You are in the lobby of the castle, a hall with lights in the ceilings")

    def test_fight_soldier(self):
        self.game.player.current_room = self.game.garden
        self.assertIn("Soldier in the Garden", [soldier.name for soldier in self.game.garden.get_soldiers()])
        self.game.do_fight_soldier_command()
        self.assertEqual(len(self.game.garden.get_soldiers()), 0)

    def test_pick_item(self):
        self.game.player.current_room = self.game.armory
        self.assertIn("sword", self.game.armory.get_room_items())
        self.game.do_pick_up_command("sword")
        self.assertIn("sword", self.game.player.backpack.contents)
        self.assertNotIn("sword", self.game.armory.get_room_items())

    def test_solve_puzzle(self):
        self.game.player.current_room = self.game.library
        self.game.do_solve_command()
        self.assertIsNotNone(self.game.library.get_exit("secret", self.game.player.backpack.contents))


if __name__ == "__main__":
    unittest.main()
