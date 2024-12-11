from enum import Enum
from collections import defaultdict
import asyncio
from qasync import asyncSlot, QEventLoop
from random import choice

from Constants import MIDI_VALUE_DICT
from SoundPlayer import SoundPlayer

DEFAULT_VOLUME = 50
DEFAULT_BPM = 500
DEFAULT_OCTAVE_MOD = 0
MAX_OCTAVE_MOD = 5
MIN_OCTAVE_MOD = -5
MAX_VOLUME = 255

class Types(Enum):
    NOTE = 1,
    ACTION = 2,
    INVALID = 3

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
    'O': Types.ACTION, # play previous note | play instrument #125
    'o': Types.ACTION, # play previous note | play instrument #125
    'I': Types.ACTION, # play previous note | play instrument #125
    'i': Types.ACTION, # play previous note | play instrument #125 
    'U': Types.ACTION, # play previous note | play instrument #125
    'u': Types.ACTION, # play previous note | play instrument #125
    '?': Types.ACTION, # random note
    'R+': Types.ACTION, # increment octave
    'R-': Types.ACTION, # decrement octave
    '+': Types.ACTION, # double volume
    '-': Types.ACTION, # default volume
    '\n': Types.ACTION, # change instrument (any)
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

        self.actions_map = defaultdict(lambda: None, {
            Types.NOTE: self._play_note,
            'BPM+': self._increment_bpm_by_80,
            'O': self._change_instrument,
            'o': self._change_instrument,
            'I': self._change_instrument,
            'i': self._change_instrument,
            'U': self._change_instrument,
            'u': self._change_instrument,
            '?': self._play_random_note,
            'R+': self._increment_octave,
            'R-': self._decrement_octave,
            '+': self._double_volume,
            '-': self._reset_volume,
            '\n': self._change_instrument,
        })
            
    @asyncSlot()
    async def play_song(self):
        self.reset()
        self._is_playing = True
        
        i = 0
        while i < len(self.actions):
            action = self.actions[i]        
            self._midi_output.set_instrument(self._instrument)
            
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
                try:
                    await action[0](action[1])
                except TypeError:
                    print('\n')
                    print(action)
                    action()
                except:
                    break
                
            i += 1
                    
        self._is_playing = False

    def process_input(self, input: str):
        input = list(input)
        self.actions = []
        print(input)
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
                        
                    case Types.INVALID:
                        pass
            self.previous_char = input[i]
        print(input)                    
            
    def _double_volume(self):
        self._volume = self._volume * 2
    
    def _change_instrument(self, instrument:int):
        self._instrument = instrument
    
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
    
    def wipe_song(self):
        self.actions = []
    
    def reset(self):
        self._reset_volume()
        self._reset_octave()
        self._reset_BPM()
         
    async def _play_random_note(self) -> None:
        await self._play_note(choice(list(MIDI_VALUE_DICT.keys())))
    
    def _increment_bpm_by_80(self) -> None:
        period = self._wait_time/60000
        current_freq = 1/period
        new_freq = current_freq + 80
        new_period = 1/new_freq
        self._wait_time = new_period * 60000

    def switch_paused(self) -> None:
        self.paused = not self.paused
        
        
        

