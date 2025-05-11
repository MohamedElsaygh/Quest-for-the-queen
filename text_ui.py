"""
A simple text based User Interface (UI) for the Adventure World game.
"""


class TextUI:
    """A simple text based User Interface (UI) for the Adventure World game."""

    def __init__(self):
        # Nothing to do...
        pass

    def get_command(self):
        """
            Fetches a command from the console.
        :return: a 2-tuple of the form (command_word, second_word)
        """
        word1 = None
        word2 = None
        print('> ', end='')
        input_line = input().strip()
        if input_line:
            all_words = input_line.split()
            command_word = all_words[0]
            second_word = " ".join(all_words[1:]) if len(all_words) > 1 else None
            return command_word, second_word
        return None, None

    def print(self, text):
        """
            Displays text to the console.
        :param text: Text to be displayed
        :return: None
        """
        print(text)
