"""
This class is the main class of the "Adventure World" application.
'Adventure World' is a very simple, text based adventure game. Users can walk
around some scenery. That's all. It should really be extended to make it more
interesting!

To play this game, create an instance of this class and call the "play" method.

This main class creates and initialises all the others: it creates all rooms,
creates the parser and starts the game. It also evaluates and executes the
commands that the parser returns.

This game is adapted from the 'World of Zuul' by Michael Kolling and 
David J. Barnes. The original was written in Java and has been simplified and
converted to Python by Kingsley Sage.
"""


from room import Room
from text_ui import TextUI
from backpack import Backpack
import random
from player import Player
from soldier import Soldier
import os




class Game:
    """Main class for the game."""

    def __init__(self):
        """
        Initialises the game.
        """
        self.create_rooms()
        self.player = Player(self.outside)
        self.ui = TextUI()
        self.backpack = Backpack(5)
        self.dragon_health = 200

        #log file
        self.log_file="game_log.txt"
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def log(self, message):
        """
        This writes a log message to the log file.
        :param message: The message to log
        """
        with open(self.log_file, "a") as log:
            log.write(f"{message}\n")

    def create_rooms(self):
        """
            Sets up all room assets.
        :return: None
        """
        self.garden = Room("you are in the castle's garden, enter the castle to save the queen")
        self.outside = Room("You are outside the castle")
        self.entrance_hall = Room("You are in the lobby of the castle, a hall with lights in the ceilings")
        self.dining_room = Room("table room with dishes on it")
        self.library = Room("An old room with book shelves",clue="The bookshelf might hide a secret passage, and the key is in the dungeon.")
        self.armory = Room("A big room of weapons")
        self.dungeon = Room("A dark, damp room with the faint sound of chains rattling")
        self.tower_room = Room("A circular room with a window overlooking the castle grounds")
        self.queens_quarters = Room("A luxurious room with elegant furnishings" , locked=True, key_item="key")
        self.dragons_lair = Room("A fiery chamber where the dragon waits")
        self.hidden_chamber = Room("A secret room concealed behind a bookshelf, full of mysterious artifacts")

        self.dragons_lair.has_dragon = True
        self.queens_quarters.has_queen = True

        #Setting exits
        #Garden
        self.garden.set_exit("north", self.outside)
        #outside the castle
        self.outside.set_exit("north", self.entrance_hall)
        self.outside.set_exit("south", self.garden)
        #entrance hall
        self.entrance_hall.set_exit("south", self.outside)
        self.entrance_hall.set_exit("north", self.dining_room)
        self.entrance_hall.set_exit("east", self.library)
        #dining room
        self.dining_room.set_exit("south", self.entrance_hall)
        self.dining_room.set_exit("east", self.armory)
        #library
        self.library.set_exit("west", self.entrance_hall)
        self.library.set_exit("upstairs", self.tower_room)
        self.library.set_exit("secret", self.hidden_chamber)
        #armory
        self.armory.set_exit("west", self.dining_room)
        self.armory.set_exit("downstairs", self.dungeon)
        #dungeon
        self.dungeon.set_exit("upstairs", self.armory)
        #tower room
        self.tower_room.set_exit("downstairs", self.library)
        self.tower_room.set_exit("north", self.queens_quarters)
        #queens quarters
        self.queens_quarters.set_exit("south", self.tower_room)
        self.queens_quarters.set_exit("east", self.dragons_lair)
        #dragons lair
        self.dragons_lair.set_exit("west", self.queens_quarters)
        self.dungeon.set_exit("west", self.hidden_chamber)
        #hidden chamber
        self.hidden_chamber.set_exit("out", self.library)
        self.hidden_chamber.set_exit("east", self.dungeon)

        #Adding items to specific rooms
        self.armory.add_room_item("sword")
        self.armory.add_room_item("shield")
        self.tower_room.add_room_item("health drink")
        self.hidden_chamber.add_room_item("health bag")
        self.dining_room.add_room_item("health bag")
        self.dining_room.add_room_item("health drink")
        self.library.add_room_item("magic scroll")
        self.dungeon.add_room_item("key")
        self.hidden_chamber.add_room_item("ancient artifact")

        #Adding soldiers in rooms
        self.garden.add_soldier(Soldier("Soldier in the Garden", health=50, damage=10))
        self.library.add_soldier(Soldier("Soldier in the Library", health=50, damage=10))

    def play(self):
        """
            The main play loop.
        :return: None
        """
        self.print_welcome()
        finished = False
        while not finished:
            command = self.ui.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
        print("Thank you for playing!")

    def print_welcome(self):
        """
            Displays a welcome message.
        :return: None
        """
        self.log("Game started.")
        self.ui.print("Welcome, brave knight! The Queen has been captured.")
        self.ui.print("Your quest is to navigate the castle, unlock doors, and rescue her from the dragon!")
        self.ui.print(f"Your command words are: {self.show_command_words()}")

    def show_command_words(self):
        """
            Show a list of available commands.
        :return: None
        """
        return ["help", "go", "quit", "pick" , "inventory","read", "solve", "fight", "use" , "fight soldiers", "look"]

    def do_look_command(self):
        """
        This method allows the player to look around and see the contents of the room.
        """
        room_contents = self.player.current_room.describe_contents()
        self.ui.print(f"Room contents: {room_contents}")

    def show_inventory(self):
        """
        This function displays the player's inventory.
        :return: None
        """
        if self.player.backpack.contents:
            self.ui.print("You are carrying:")
            for item in self.player.backpack.contents:
                self.ui.print(f"- {item}")
        else:
            self.ui.print("Your backpack is empty.")

    def do_pick_up_command(self, item):
        """
        This method handles the 'pick up' command to take an item from the current room.
        :param item: The item to pick up
        :return: None
        """
        if item is None:
            self.ui.print("Pick up what?")
            return

        if item in self.player.current_room.get_room_items():
            if item == "shield":
                self.player.equip_shield()
                self.player.current_room.remove_room_item(item)
                self.ui.print("You picked up and equipped the shield! Your protection is increased.")
                self.log("Player equipped the shield for increased protection.")
            elif self.player.backpack.add_item(item):
                self.player.current_room.remove_room_item(item)
                self.ui.print(f"You picked up the {item}.")
                self.log(f"Player picked up {item}.")
            else:
                self.ui.print("Your backpack is full!")
                self.log(f"Failed to pick up {item} (backpack full).")
        else:
            self.ui.print(f"There is no {item} here.")
            self.log(f"Tried to pick up {item}, but it was not found.")

    def do_drop_command(self, item):
        """
        This Method handles the 'drop' command to place an item from the backpack into the current room.
        :param item: The item to drop
        :return: None
        """
        if item is None:
            self.ui.print("Drop what?")
            return

        if self.player.backpack.check_item(item):
            self.player.backpack.remove_item(item)
            self.player.current_room.add_room_item(item)
            self.ui.print(f"You dropped the {item}.")
            self.log(f"Player dropped {item} in {self.player.current_room.description}.")
        else:
            self.ui.print(f"You are not carrying {item}.")
            self.log(f"Failed to drop {item}: not in inventory.")

    def do_read_command(self):
        """
        This Method displays the clue in the current room, if there is any.
        :return: None
        """
        if self.player.current_room.clue:
            self.ui.print(f"Clue: {self.player.current_room.clue}")
        else:
            self.ui.print("There is nothing to read here.")

    def do_solve_command(self):
        """This Method is to solve a puzzle to open the secret chamber"""
        if self.player.current_room == self.library:
            self.library.set_exit("secret", self.hidden_chamber)
            self.ui.print("You solved the puzzle! A secret passage opens.")
            self.log("Player solved the library puzzle. Secret passage unlocked.")
        else:
            self.ui.print("There's nothing to solve here.")
            self.log("Player attempted to solve a puzzle, but none was present.")

    def do_fight_command(self):
        if self.player.current_room != self.dragons_lair:
            self.ui.print("There is nothing to fight here.")
            self.log("Player attempted to fight, but no dragon was present.")
            return False

        self.log("Player engaged the dragon in combat.")

        if "sword" not in self.player.backpack.contents:
            self.ui.print("You need a sword to fight the dragon!")
            return False

        sword_damage = 40
        if "magic scroll" not in self.player.backpack.contents:
            self.ui.print("Your sword is sharp but ordinary.")
        else:
            self.ui.print("Your sword glows with magical energy!")
            sword_damage = 60
        self.dragon_health -= sword_damage

        self.ui.print("The battle begins!")

        while self.player.health > 0 and self.dragon_health > 0:
            # Display health bars
            self.ui.print(Game.health_bar("Knight", self.player.health, 100))
            self.ui.print(Game.health_bar("Dragon", self.dragon_health, 200))
            #Let the player decide what to do heal or attack
            self.ui.print("What will you do? (attack / heal)")
            action = input("> ").strip().lower()
            if action == "attack":
              # When the player attacks the dragon
                self.ui.print("You strike the dragon!")
                self.dragon_health -= 40
                if self.dragon_health <= 0:
                    self.ui.print("You have defeated the dragon!")
                    self.ui.print("The Queen is safe! Congratulations, you win!")
                    return True
            elif action == "heal":
                # When the player heals himself
                if "health drink" in self.player.backpack.contents:
                    self.player.backpack.remove_item("health drink")
                    self.player.heal(30)
                    self.ui.print("You used a health drink and restored 30 health.")
                elif "health bag" in self.player.backpack.contents:
                    self.player.backpack.remove_item("health bag")
                    self.player.heal(50)
                    self.ui.print("You used a health bag and restored 50 health.")
                else:
                    self.ui.print("You have no healing items left!")
            else:
                self.ui.print("Invalid action. You lose your turn!")

            # when dragon does a counter-attack
            damage = random.randint(15, 30)  # This random damages between 15 and 30 randomly
            self.ui.print(f"The dragon breathes fire and deals {damage} damage!")
            self.player.health -= damage
            self.log(f"Dragon attacked! Player took {damage} damage. Current health: {self.player.health}.")
            if self.player.health <= 0:
                self.ui.print("Game Over !! You have been defeated by the dragon...")
                self.log("Player was defeated by the dragon.")
                return True

        return True

    def do_use_command(self, item):
        """
        This method handles the 'use' command to recover health, where drink gives 30 HP
        and health bag gives 50 HP
        :param item: The item to use
        """
        if item is None:
            self.ui.print("Use what?")
            return

        if item == "health drink":
            if "health drink" in self.player.backpack.contents:
                self.player.backpack.remove_item("health drink")
                self.player.heal(30)
                self.ui.print("You used a health drink and restored 30 health.")
                self.log("Player used a health drink and restored 30 health.")
            else:
                self.ui.print("You don't have a health drink.")
                self.log("Player tried to use health drink but none were available.")
        elif item == "health bag":
            if "health bag" in self.player.backpack.contents:
                self.player.backpack.remove_item("health bag")
                self.player.heal(50)
                self.ui.print("You used a health bag. Restored 50 health.")
            else:
                self.ui.print("You don't have a health bag.")
        else:
            self.ui.print(f"You can't use {item}.")

    def offer_bag_upgrade(self):
        """
        This Method offers the player a chance to upgrade their backpack capacity.
        """
        new_capacity = self.player.backpack.capacity + 5
        self.ui.print(f"A new backpack with capacity {new_capacity} is available!")
        self.ui.print("Do you want to upgrade? (yes/no)")

        choice = input("> ").strip().lower()
        if choice == "yes":
            # Upgrade the backpack
            new_backpack = Backpack(new_capacity)
            # This is to transfer items from the old backpack to the new one
            for item in self.player.backpack.contents:
                new_backpack.add_item(item)
            self.player.backpack = new_backpack
            self.ui.print(f"You upgraded your backpack to a capacity of {new_capacity}!")
        else:
            self.ui.print("You decided to keep your current backpack.")

    def do_fight_soldier_command(self):
        """
        This method allows the player to fight a soldier and earn a reward.
        """
        soldiers = self.player.current_room.get_soldiers()

       #check if there are any soldiers in the room
        if not soldiers:
            self.ui.print("There is no one to fight here.")
            self.log("Attempted to fight, but no soldiers were present.")
            return

        soldier = soldiers[0]
        self.ui.print(f"You are fighting {soldier.name}!")
        self.log(f"Engaged in a fight with {soldier.name}.")

        while soldier.health > 0 and self.player.health > 0:
            self.ui.print(self.health_bar("Knight", self.player.health, self.player.max_health))
            self.ui.print(self.health_bar(soldier.name, soldier.health, 60))

            #choice between to heal or to attack?
            self.ui.print("What will you do? (attack / heal)")
            action = input("> ").strip().lower()
            if action == "attack":
                # when the player attacks the soldier
                self.ui.print("You attack the soldier!")
                soldier.health -= 30
                if soldier.health <= 0:
                    self.ui.print(f"You defeated {soldier.name}!")
                    self.player.current_room.remove_soldier(soldier)
                    self.log(f"Defeated {soldier.name} in combat.")
                    # This code is for the reward
                    reward = random.choice(["bag_upgrade", "heal", "sword"])
                    if reward == "bag_upgrade":
                        self.ui.print("You are rewarded with a bag upgrade!")
                        self.offer_bag_upgrade()
                    elif reward == "heal":
                        self.ui.print("You are rewarded with a full heal!")
                        self.player.heal(self.player.max_health)
                    elif reward == "sword":
                        self.ui.print("You are rewarded with a stronger sword!")
                        self.player.backpack.add_item("enhanced sword")
                    return
            elif action == "heal":
                # when the player heals himself
                if "health drink" in self.player.backpack.contents:
                    self.player.backpack.remove_item("health drink")
                    self.player.heal(30)
                    self.ui.print("You used a health drink and restored 30 health.")
                elif "health bag" in self.player.backpack.contents:
                    self.player.backpack.remove_item("health bag")
                    self.player.heal(50)
                    self.ui.print("You used a health bag and restored 50 health.")
                else:
                    self.ui.print("You have no healing items left!")
                    self.log("Player attempted to heal but had no items.")
            else:
                self.ui.print("Invalid action. You lose your turn!")
                self.log(f"Invalid action '{action}' during fight.")

            # when the soldier attacks the player
            self.ui.print(f"{soldier.name} counter-attacks!")
            damage = soldier.damage
            self.player.take_damage(damage)
            if self.player.health <= 0:
                self.ui.print("You have been defeated!")
                self.log(f"Player was defeated by {soldier.name}.")
                return

    def process_command(self, command):
        """
            Process a command from the TextUI.
        :param command: a 2-tuple of the form (command_word, second_word)
        :return: True if the game has been quit, False otherwise
        """
        command_word, second_word = command
        if command_word is not None:
            command_word = command_word.lower()

        want_to_quit = False
        if command_word == "help":
            self.print_help()
        elif command_word == "go":
            self.do_go_command(second_word)
        elif command_word == "quit":
            want_to_quit = True
            self.log("Player quit the game.")
        elif command_word == "pick":
            self.do_pick_up_command(second_word)
        elif command_word == "inventory":
            self.show_inventory()
        elif command_word == "drop":
            self.do_drop_command(second_word)
        elif command_word == "read":
            self.do_read_command()
        elif command_word == "solve":
            self.do_solve_command()
        elif command_word =="fight" and second_word == "soldiers":
            self.do_fight_soldier_command()
        elif command_word == "fight":
            self.do_fight_command()
        elif command_word == "use":
            self.do_use_command(second_word)
        elif command_word == "look":
            self.do_look_command()
        else:
            # Unknown command...
            self.ui.print("Don't know what you mean.")

        return want_to_quit

    def print_help(self):
        """
            Display some useful help text.
        :return: None
        """
        self.ui.print("You are lost. You are alone. You wander around the deserted complex.")
        self.ui.print("")
        self.ui.print(f"Your command words are: {self.show_command_words()}.")

    def do_go_command(self, second_word):
        """
            Performs the GO command.
        :param second_word: the direction the player wishes to travel in
        :return: None
        """
        if second_word is None:
            # Missing second word...
            self.ui.print("Go where?")
            return

        next_room = self.player.current_room.get_exit(second_word, self.player.backpack.contents)
        if next_room == "locked":
            self.ui.print("The door is locked. You need a key to enter.")
            self.log(f"Attempted to go {second_word}, but the door is locked.")
        elif next_room is None:
            self.ui.print("There is no door!")
            self.log(f"Attempted to go {second_word}, but no door exists.")
        else:
            self.log(f"Player moved from {self.player.current_room.description} to {next_room.description}.")
            self.player.current_room = next_room
            self.ui.print(self.player.current_room.get_long_description())

            # Show the contents of the room
            room_contents = self.player.current_room.describe_contents()
            self.ui.print(f"Room contents: {room_contents}")

        if self.player.current_room == self.dragons_lair:
            self.ui.print("You have entered the Dragon's Lair. The dragon roars fiercely!")
            return
    @staticmethod
    def health_bar(name, health, max_health):
        """
        This method displays a visual health bar for a character.
        :param name: Name of the character
        :param health: Current health points
        :param max_health: Maximum health points
        """
        bar_length = 20
        filled_length = int(bar_length * health / max_health)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        return f"{name} Health: [{bar}] {health}/{max_health}"

def main():
    """Main entry point for the game."""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
