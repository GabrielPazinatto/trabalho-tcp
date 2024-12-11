from enum import IntEnum


class MIDI_VALUE(IntEnum):
    NO_SOUND = -1
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

MIDI_VALUE_DICT: dict[str:int] = {
    'C': MIDI_VALUE.C_NOTE,
    'D': MIDI_VALUE.D_NOTE,
    'E': MIDI_VALUE.E_NOTE,
    'F': MIDI_VALUE.F_NOTE,
    'G': MIDI_VALUE.G_NOTE,
    'A': MIDI_VALUE.A_NOTE,
    'B': MIDI_VALUE.B_NOTE,
    'c': MIDI_VALUE.C_NOTE,
    'd': MIDI_VALUE.D_NOTE,
    'e': MIDI_VALUE.E_NOTE,
    'f': MIDI_VALUE.F_NOTE,
    'g': MIDI_VALUE.G_NOTE,
    'a': MIDI_VALUE.A_NOTE,
    'b': MIDI_VALUE.B_NOTE,
    ' ': MIDI_VALUE.NO_SOUND
}


    # instruments:
    #http://www.ccarh.org/courses/253/handout/gminstruments/

class INSTRUMENTS_VALUE(IntEnum):
    PIANO = 0
    VIOLAO = 24
    GUITARRA = 27
    GUITARRA_DISTORCIDA = 30
    BAIXO = 33
    VIOLINO = 40
    TROMPETE = 56

INSTRUMENTS_VALUE_DICT: dict[str:int] = {
    "Piano": INSTRUMENTS_VALUE.PIANO,
    "Violão": INSTRUMENTS_VALUE.VIOLAO,
    "Guitarra": INSTRUMENTS_VALUE.GUITARRA,
    "Guitarra Distorcida": INSTRUMENTS_VALUE.GUITARRA_DISTORCIDA,
    "Baixo": INSTRUMENTS_VALUE.BAIXO,
    "Violino": INSTRUMENTS_VALUE.VIOLINO,
    "Trompete": INSTRUMENTS_VALUE.TROMPETE
}