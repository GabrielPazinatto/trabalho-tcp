import pygame
import pygame.midi
import asyncio
from Constants import MIDI_VALUE_DICT, MIDI_VALUE
import random

OCTAVE_SIZE = 12
MAX_VOLUME = 200

class SoundPlayer:
    
    # instruments:
    #http://www.ccarh.org/courses/253/handout/gminstruments/
    
    def __init__(self, octave_modifier:int = 0, wait_time:int = 500, instrument:int = 0, volume:int = 127):
        self._octave_modifier:int = octave_modifier
        self._wait_time:int = wait_time
        self._instrument:int = instrument
        self._volume:int = volume
        self._midi_output = None
        self._song:str = ""
        self._action_index = 0
        
    async def _play_note(self, note:int) -> None:
        if note == MIDI_VALUE.NO_SOUND:
            await asyncio.sleep(self._wait_time/1000)
            return
        
        self._midi_output.note_on(int(MIDI_VALUE_DICT[note]) + self._octave_modifier*OCTAVE_SIZE, self._volume)
        await asyncio.sleep(self._wait_time/1000)
        self._midi_output.note_off(int(MIDI_VALUE_DICT[note]) + self._octave_modifier*OCTAVE_SIZE, self._volume)
            
    def _init_midi(self) -> None:
        pygame.midi.init()
        self._midi_output = pygame.midi.Output(0)        
            
    def set_instrument(self, instrument:int) -> None:
        self._instrument = instrument
        
    def set_volume(self, volume:int) -> None:
        self._volume = volume
    
    def set_octave_modifier(self, octave_modifier:int) -> None:
        self._octave_modifier = octave_modifier
        
    def increment_octave(self) -> None:
        self._octave_modifier += 1
        
    def decrement_octave(self) -> None:
        self._octave_modifier -= 1
        
    def set_wait_time(self, wait_time:int) -> None:
        self._wait_time = wait_time
        
    def double_volume(self) -> None:
        if self._volume*2 >= MAX_VOLUME:
            return
        else:
            self._volume *=2 
    
    def increment_bpm_by_80(self) -> None:
        self._wait_time -= 80
        

    