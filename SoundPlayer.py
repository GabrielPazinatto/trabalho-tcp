import pygame
import pygame.midi

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
As_NOTE = 70    # A Sharp | Lá Sustenido
B_NOTE = 71     # B       | Si

MIDI_VALUE: dict[str:int] = {
    'C': C_NOTE,
    'D': D_NOTE,
    'E': E_NOTE,
    'F': F_NOTE,
    'G': G_NOTE,
    'A': A_NOTE,
    'B': B_NOTE
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
        
    def _play_note(self, note:int) -> None:
        pygame.midi.init()
        self._midi_output = pygame.midi.Output(0)
        
        self._midi_output.note_on(MIDI_VALUE[note] + self._octave_modifier*OCTAVE_SIZE, self._volume)
        pygame.time.wait(self._wait_time)
        self._midi_output.note_off(MIDI_VALUE[note], self._volume)
    
        pygame.midi.quit()