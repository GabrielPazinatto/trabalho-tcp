from midiutil import MIDIFile
from Constants import MIDI_VALUE_DICT, MIDI_VALUE

def save_music(text: str, filename: str, instrument: int, octave_modifier: int, bpm: int, volume: int):
    """
    Salva a música como um arquivo MIDI.

    :param text: Texto contendo as notas da música.
    :param filename: Nome do arquivo MIDI a ser salvo.
    :param instrument: Instrumento MIDI a ser usado.
    :param octave_modifier: Modificador de oitava.
    :param bpm: Velocidade em BPM.
    :param volume: Volume da música.
    """
    midi_file = MIDIFile(1)  # Uma única faixa
    track = 0
    time = 0
    channel = 0

    # Configurações da faixa
    midi_file.addTrackName(track, time, "Generated Track")
    midi_file.addTempo(track, time, bpm)
    midi_file.addProgramChange(track, channel, time, instrument)

    # Processa o texto e adiciona as notas no arquivo MIDI
    for char in text:
        note = MIDI_VALUE_DICT.get(char, MIDI_VALUE.NO_SOUND)
        if note != MIDI_VALUE.NO_SOUND:
            midi_file.addNote(
                track=track,
                channel=channel,
                pitch=int(note) + octave_modifier * 12,
                time=time,
                duration=1,  # Duração padrão
                volume=volume
            )
            time += 1

    # Salva o arquivo
    with open(filename, "wb") as midi_out:
        midi_file.writeFile(midi_out)

    print(f"Arquivo MIDI '{filename}' salvo com sucesso.")
