from enum import Enum
from collections import defaultdict
import asyncio
from qasync import asyncSlot, QEventLoop
from random import choice, randint
from inspect import iscoroutinefunction

from Constants import MIDI_VALUE_DICT
from SoundPlayer import SoundPlayer

DEFAULT_VOLUME = 50
DEFAULT_BPM = 500
DEFAULT_OCTAVE_MOD = 0
MAX_OCTAVE_MOD = 5
MIN_OCTAVE_MOD = -5
MAX_VOLUME = 255
DEFAULT_INSTRUMENT = 0

class Types(Enum):
    NOTE = 1,
    ACTION = 2,
    ACTION_WITH_PREV_CHAR = 3,
    ACTION_WITH_NEXT_CHAR = 4,
    INVALID = 5

token_type = defaultdict(lambda: Types.INVALID, {
    'A': Types.NOTE, # A note 
    'B': Types.NOTE, # B note
    'C': Types.NOTE, # C note
    'D': Types.NOTE, # D note
    'E': Types.NOTE, # E note
    'F': Types.NOTE, # F note
    'G': Types.NOTE, # G note
    'a': Types.NOTE, # a note
    'b': Types.NOTE, # b note
    'c': Types.NOTE, # c note
    'd': Types.NOTE, # d note
    'e': Types.NOTE, # e note
    'f': Types.NOTE, # f note
    'g': Types.NOTE, # g note
    ' ': Types.NOTE, # silence
    'O': Types.ACTION_WITH_PREV_CHAR, # play previous note | play instrument #125
    'o': Types.ACTION_WITH_PREV_CHAR, # play previous note | play instrument #125
    'I': Types.ACTION_WITH_PREV_CHAR, # play previous note | play instrument #125
    'i': Types.ACTION_WITH_PREV_CHAR, # play previous note | play instrument #125 
    'U': Types.ACTION_WITH_PREV_CHAR, # play previous note | play instrument #125
    'u': Types.ACTION_WITH_PREV_CHAR, # play previous note | play instrument #125
    '?': Types.ACTION, # random note
    'R+': Types.ACTION, # increment octave
    'R-': Types.ACTION, # decrement octave
    '+': Types.ACTION, # double volume
    '-': Types.ACTION, # default volume
    '\n': Types.ACTION_WITH_NEXT_CHAR, # change instrument (any)
    'BPM+': Types.ACTION, # increment bpm by 80
    ';': Types.ACTION, # randomize bpm
})

class MusicPlayer(SoundPlayer): 

    def __init__(self, octave_modifier: int = 0, wait_time: int = 500, instrument: int = 0, volume: int = DEFAULT_VOLUME):
        super().__init__(octave_modifier, wait_time, instrument, volume)
        self.actions: list[function] = []
        self.previous_char: str = ''
        self.paused = False
        self._is_playing = False
        self._stop_playing = False
        self._reset_song = False
        self._repeat_song = False

        self.actions_map = defaultdict(lambda: None, {
            Types.NOTE: self._play_note,
            'BPM+': self._increment_bpm_by_80,
            'O': self._make_telephone_sound,
            'o': self._make_telephone_sound,
            'I': self._make_telephone_sound,
            'i': self._make_telephone_sound,
            'U': self._make_telephone_sound,
            'u': self._make_telephone_sound,
            '?': self._play_random_note,
            'R+': self._increment_octave,
            'R-': self._decrement_octave,
            '+': self._double_volume,
            '-': self._reset_volume,
            '\n': self._change_instrument,
            ';' : self._randomize_bpm,
        })
            
    @asyncSlot()
    async def play_song(self):
        self._is_playing = True
        
        while self._repeat_song or self._is_playing:
            
            self.reset()
            
            i = 0
            while i < len(self.actions):
                action = self.actions[i]        
                
                if self._reset_song:
                    i = 0
                    action = self.actions[i]        
                    self._reset_song = False
                
                if self._stop_playing:
                    self._stop_playing = False
                    break
                
                while self.paused:
                    await asyncio.sleep(1)
                    
                if not self._reset_song:
                    method_has_parameter:bool = type(action) == tuple
                    method_is_async:bool = iscoroutinefunction(action[0]) if method_has_parameter else iscoroutinefunction(action)
                    print(action, method_has_parameter, method_is_async)
                    
                    if method_is_async and method_has_parameter:
                        await action[0](action[1])
        
                    elif method_has_parameter:
                        try:
                            action[0](action[1])
                        except:
                            pass
                    
                    elif method_is_async:
                        await action()
        
                    else:
                        action()
                        
                i += 1
                        
            self._is_playing = False

    def process_input(self, input: str):
        input = list(input)
        self.actions = []
        for i in range(len(input)):
            
            if input[i] == None:
                continue
            
            if i < len(input) - 3 and token_type[''.join(input[i:i+4])] == Types.ACTION:
                self.actions.append((self.actions_map[''.join(input[i:i+4])]))
                input[i:i+4] = [None, None, None, None]
                
            elif i < len(input) - 1 and  token_type[''.join(input[i:i+2])] == Types.ACTION:
                self.actions.append((self.actions_map[''.join(input[i:i+2])]))
                input[i:i+2] = [None, None]
                
            else:
                match(token_type[input[i]]):
                    
                    case Types.NOTE:
                        self.actions.append((self.actions_map[Types.NOTE], input[i]))

                    case Types.ACTION:
                        self.actions.append((self.actions_map[input[i]]))
                        
                    case Types.ACTION_WITH_PREV_CHAR:
                        try:
                            self.actions.append((self.actions_map[input[i]]))
                        except:
                            pass
                    
                    case Types.ACTION_WITH_NEXT_CHAR:
                        try:
                            self.actions.append((self.actions_map[input[i]], input[i+1]))
                            input[i+1] = None
                        except:
                            pass
                    
                    case Types.INVALID:
                        pass
                    
            self.previous_char = input[i]
    
    def _change_instrument(self, instrument:int):
        return super().set_instrument(instrument)
    
    def _increment_octave(self) -> None:
        if self._octave_modifier < MAX_OCTAVE_MOD:
            return super().increment_octave()        
    
    def _decrement_octave(self) -> None:
        if self._octave_modifier > MIN_OCTAVE_MOD:
            return super().decrement_octave()
    
    def _double_volume(self) -> None:
        if self._volume*2 < MAX_VOLUME:
            return super().double_volume()
        else:
            self._volume = MAX_VOLUME
    
    def _reset_volume(self):
        self._volume = DEFAULT_VOLUME

    def _reset_octave(self):
        self._octave_modifier = DEFAULT_OCTAVE_MOD

    def reset_song(self):
        self._reset_song = True

    def _reset_BPM(self):
        self._wait_time = DEFAULT_BPM
    
    def _randomize_bpm(self):
        self._wait_time = randint(1, 3000)
    
    def _reset_instrument(self):
        self._change_instrument(DEFAULT_INSTRUMENT)
    
    def reset(self):
        self._reset_volume()
        self._reset_octave()
        self._reset_BPM()
         
    async def _play_random_note(self) -> None:
        notes = [val for val in MIDI_VALUE_DICT.keys()]
        await self._play_note(choice(notes))
        
    async def _make_telephone_sound(self) -> None:
        if self.previous_char in MIDI_VALUE_DICT.keys():
            return
        await self._play_note('A', 124)
    
    def _increment_bpm_by_80(self) -> None:
        period = self._wait_time/60000
        current_freq = 1/period
        new_freq = current_freq + 80
        new_period = 1/new_freq
        self._wait_time = new_period * 60000

    def switch_paused(self) -> None:
        self.paused = not self.paused
        