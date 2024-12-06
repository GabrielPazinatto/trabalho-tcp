import pygame
import pygame.midi
import asyncio

OCTAVE_SIZE = 12

C_NOTE = 60     # C       | Dó
Cs_NOTE = 61    # C Sharp | Dó Sustenido
D_NOTE = 62     # D       | Ré
Ds_NOTE = 63    # D Sharp | Ré Sustenido
E_NOTE = 64     # E       | Mi
F_NOTE = 65     # F       | Fá
Fs_NOTE = 66    # F Sharp | Fá Sustenido
G_NOTE = 67     # G       | Sol
Gs_NOTE = 68    # G Sharp | Sol Sustenido
A_NOTE = 69     # A       | Lá
As_NOTE = 70    # A Sharp | Lá Susteniset_instrumentdo
B_NOTE = 71     # B       | Si

MIDI_VALUE: dict[str:int] = {
    'C': C_NOTE,
    'D': D_NOTE,
    'E': E_NOTE,
    'F': F_NOTE,
    'G': G_NOTE,
    'A': A_NOTE,
    'B': B_NOTE,
    'c': C_NOTE,
    'd': D_NOTE,
    'e': E_NOTE,
    'f': F_NOTE,
    'g': G_NOTE,
    'a': A_NOTE,
    'b': B_NOTE,
}

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
        self._midi_output.note_on(MIDI_VALUE[note] + self._octave_modifier*OCTAVE_SIZE, self._volume)
        await asyncio.sleep(self._wait_time/1000)
        self._midi_output.note_off(MIDI_VALUE[note], self._volume)
            
    def _init_midi(self) -> None:
        pygame.midi.init()
        self._midi_output = pygame.midi.Output(0)
        self._midi_output.set_instrument(self._instrument)
            
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
        
    