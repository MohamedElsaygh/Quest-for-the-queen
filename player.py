from backpack import Backpack

class Player:
    """
    This Class represents the player, their inventory, and current location.
    """
    def __init__(self, starting_room):
        """
        The constructor initializes the player with a starting room and backpack.
        :param starting_room: The room where the player starts
        """
        self.current_room = starting_room
        self.backpack = Backpack(5)
        self.health = 100
        self.max_health = 100
        self.has_shield = False

    def take_damage(self, damage):
        """
        This Method reduces the player's health. If a shield is equipped, reduces damage taken.
        """
        if self.has_shield:
            damage = max(damage - 10, 0)
        self.health -= damage
        self.health = max(self.health, 0)

    def move_to_room(self, next_room):
        """
        Here the player can move to a new room.
        :param next_room: The room to move to
        """
        self.current_room = next_room

    def heal(self, amount):
        """
        The player can heal himself by a certain amount up to the max_health.
        :param amount: amount to heal
        """
        self.health += amount
        self.health = min(self.health, self.max_health)

    def equip_shield(self):
        """
        When the player equips a shield, this increases protection and maximum health.
        """
        if not self.has_shield:
            self.has_shield = True
            self.max_health += 20
            self.health = self.max_health