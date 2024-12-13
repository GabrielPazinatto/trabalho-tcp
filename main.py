from MainWindow import MainWindow
import sys
import asyncio
from qasync import QEventLoop, asyncSlot
from PyQt6.QtWidgets import QApplication
from MusicPlayer import MusicPlayer
from Constants import INSTRUMENTS_VALUE_DICT, INSTRUMENTS_VALUE
from music_saver import save_music


app = QApplication(sys.argv)
loop = QEventLoop()
window = MainWindow()
player = MusicPlayer()
asyncio.set_event_loop(loop)

def play_typed_song():
    print(player._is_playing)
    if not player._is_playing:
        player.play_song()
    else:
        player.switch_paused()

def submit_song():
    song = window.music_text_box.toPlainText()
    player.process_input(song)
    
def change_instrument():
    instrument = window.instrument_combo.currentText()
    player.set_instrument(INSTRUMENTS_VALUE_DICT[instrument])

def adjust_bpm():
    try:
        bpm = 60000/(int(window.bpm_input.text()))
    except:
        bpm = 500
    player.set_wait_time(bpm)
    
def stop_playing():
    player._stop_playing = True
    
def restart_song():
    player.reset()
    player.reset_song()
    
def set_repeat_song():
    player._repeat_song = not player._repeat_song
    if player._repeat_song == True:
        window.loop_button.set_background_color("Lime")
    else:
        window.loop_button.set_background_color("#1A1A1A")

def change_button_icon():
    if player.paused == True:
        window.play_button.set_icon_pause()
    else:
        window.play_button.set_icon_play()
    
def save_song():
    """
    Obtém o texto da música e salva no arquivo MIDI.
    """
    text = window.music_text_box.toPlainText()
    save_music(
        text=text,
        filename="output.mid",
        instrument=player._instrument,
        octave_modifier=player._octave_modifier,
        bpm=120,  # Pode ajustar dinamicamente
        volume=player._volume
    )

if __name__ == '__main__':

    player._init_midi()

    window.submit_button.clicked.connect(submit_song)
    window.play_button.clicked.connect(play_typed_song)
    window.play_button.clicked.connect(change_button_icon)
    window.instrument_combo.currentIndexChanged.connect(change_instrument)
    window.next_button.clicked.connect(stop_playing)
    window.prev_button.clicked.connect(restart_song)
    window.save_button.clicked.connect(save_song)
    window.loop_button.clicked.connect(set_repeat_song)

    window.show()
    with loop:
        loop.run_forever()