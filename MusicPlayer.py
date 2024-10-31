from enum import Enum

from SoundPlayer import SoundPlayer


class Types(Enum):
    NOTE = 1,
    LOWERCASE_NOTE = 2,
    ACTION = 3

token_type = {
    'A': Types.NOTE,
    'B': Types.NOTE,
    'C': Types.NOTE,
    'D': Types.NOTE,
    'E': Types.NOTE,
    'F': Types.NOTE,
    'G': Types.NOTE,
    'a': Types.LOWERCASE_NOTE,
    'b': Types.LOWERCASE_NOTE,
    'c': Types.LOWERCASE_NOTE,
    'd': Types.LOWERCASE_NOTE,
    'e': Types.LOWERCASE_NOTE,
    'f': Types.LOWERCASE_NOTE,
    'g': Types.LOWERCASE_NOTE,
    ' ': Types.ACTION,
    '!': Types.ACTION
}


class MusicPlayer(SoundPlayer):

    def __init__(self, octave_modifier: int = 0, wait_time: int = 500, instrument: int = 0, volume: int = 127):
        super().__init__(octave_modifier, wait_time, instrument, volume)
        self.actions: list[str] = []
        self.previous_char: str = ''

        self.actions_map = {
            Types.NOTE: self._play_note
        }

    def process_input(self, input: str):
        input = list(input)

        for i in range(len(input)):

            match(token_type[input[i]]):
                case Types.NOTE:
                    self.actions.append((self.actions_map[Types.NOTE], input[i]))

                case Types.LOWERCASE_NOTE:
                    if token_type[self.previous_char] != Types.NOTE:
                        self.actions.append((self.actions_map[Types.NOTE], 0))
                    else:
                        self.actions.append(self.actions_map[Types.NOTE], input[i])

            self.previous_char = input[i]

    def play_song(self):
        for action in self.actions:
            action[0](action[1])