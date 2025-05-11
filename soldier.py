class Soldier:
    """
    This class represents the soldiers the player can fight.
    """
    def __init__(self, name, health , damage ):
        """
         a soldier has a name, health, and damage value. """
        self.name = name
        self.health = health
        self.damage = damage

    def take_damage(self, damage):
        """
        This reduces the soldier's health when he takes damage.
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0  # ensure that the health doesn't go below 0

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name} (Health: {self.health}, Damage: {self.damage})"