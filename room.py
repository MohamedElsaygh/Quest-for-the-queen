"""
Create a room described "description". Initially, it has no exits. The
'description' is something like 'kitchen' or 'an open court yard'.
"""


class Room:
    """A room in the game."""

    def __init__(self, description, locked=False, key_item=None, clue=None):
        """
            Constructor method.
        :param description: Text description for this room
        :param locked: Boolean indicating if the room is locked
        :param key_item: The item required to unlock the room
        """
        self.description = description
        self.exits = {}  # Dictionary
        self.items = []    #list of items in the room
        self.locked = locked
        self.key_item = key_item
        self.clue = clue
        self.soldiers = []
        self.has_dragon = False
        self.has_queen = False

    def set_exit(self, direction, neighbour):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room).
        :param direction: The direction leading out of this room
        :param neighbour: The room that this direction takes you to
        :return: None
        """
        self.exits[direction] = neighbour

    def get_short_description(self):
        """
            Fetch a short text description.
        :return: text description
        """
        return self.description

    def get_long_description(self):
        """
            Fetch a longer description including available exits.
        :return: text description
        """
        return f'Location: {self.description}, Exits: {self.get_exits()}.'

    def describe_contents(self):
        """
        :return: A string listing the room's contents.
        """
        contents = []

        # Add items to the description if there are
        if self.items:
            contents.append(f"Items: {', '.join(self.items)}")
        # Add soldiers to the description if there are
        if self.soldiers:
            soldier_names=', '.join(soldier.name for soldier in self.soldiers)
            contents.append(f"Soldiers: {soldier_names}")

        # if it contains (dragon, queen)
        if self.has_dragon:
            contents.append("A fierce dragon is here!")
        if self.has_queen:
            contents.append("The Queen is here, awaiting rescue!")

            # Combine all together
        return " | ".join(contents) if contents else "The room is empty."

    def get_exits(self):
        """
            Fetch all available exits as a list.
        :return: list of all available exits
        """
        all_exits = list(self.exits.keys())
        return all_exits

    def get_exit(self, direction, player_inventory):
        """
            Fetch an exit in a specified direction.
        :param direction: The direction that the player wishes to travel
        :param player_inventory: List of items the player has
        :return: Room object that this direction leads to, None if one does not exist
        """
        if direction in self.exits:
            next_room = self.exits[direction]
            if next_room.locked and next_room.key_item not in player_inventory:
                return "locked"
            return next_room
        return None

    def add_room_item(self, item):
        """
        Adds an item to the room.
        :param item: The item to add
        :return: None
        """
        self.items.append(item)

    def remove_room_item(self, item):
        """
        Removes an item from the room.
        :param item: The item to remove
        :return: True if the item was removed, False if it wasn’t found
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_room_items(self):
        """
        Returns a list of items in the room.
        :return: List of items
        """
        return self.items

    def add_soldier(self, soldier):
        """This method adds a soldier to the room."""
        self.soldiers.append(soldier)

    def remove_soldier(self , soldier):
        """This method removes a soldier from the room."""
        if soldier in self.soldiers:
            self.soldiers.remove(soldier)

    def get_soldiers(self):
        """This method gets the list of soldiers in the room."""
        return self.soldiers
