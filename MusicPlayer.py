from enum import Enum
from collections import defaultdict
import asyncio
from qasync import asyncSlot, QEventLoop

from SoundPlayer import SoundPlayer

class Types(Enum):
    NOTE = 1,
    ACTION = 2

token_type = defaultdict(lambda: Types.ACTION, {
    'A': Types.NOTE,
    'B': Types.NOTE,
    'C': Types.NOTE,
    'D': Types.NOTE,
    'E': Types.NOTE,
    'F': Types.NOTE,
    'G': Types.NOTE,
    'a': Types.NOTE,
    'b': Types.NOTE,
    'c': Types.NOTE,
    'd': Types.NOTE,
    'e': Types.NOTE,
    'f': Types.NOTE,
    'g': Types.NOTE,
})

class MusicPlayer(SoundPlayer): 

    def __init__(self, octave_modifier: int = 0, wait_time: int = 500, instrument: int = 0, volume: int = 127):
        super().__init__(octave_modifier, wait_time, instrument, volume)
        self.actions: list[str] = []
        self.previous_char: str = ''

        self.actions_map = {
            Types.NOTE: self._play_note,
            'O': self._change_instrument,
            'o': self._change_instrument,
            'I': self._change_instrument,
            'i': self._change_instrument,
            'U': self._change_instrument,
            'u': self._change_instrument,
            ' ': self._double_volume,
            '?': self._increment_octave,
            '.':self._increment_octave,
        }
            
    @asyncSlot()
    async def play_song(self):
        for action in self.actions:
            try:
                await action[0](action[1])
            except TypeError:
                await action[0]()

    def process_input(self, input: str):
        input = list(input)
        self.actions = []
        for i in range(len(input)):

            match(token_type[input[i]]):
                
                case Types.NOTE:
                    self.actions.append((self.actions_map[Types.NOTE], input[i]))

                case Types.ACTION:
                    self.actions.append((self.actions_map[input[i]], input[i]))
                    
            self.previous_char = input[i]
    
    def _double_volume(self):
        self._volume = self._volume * 2
    
    def _change_instrument(self, instrument:str):
        self._instrument = instrument
    
    def _increment_octave(self) -> None:
        return super().increment_octave()
    
    