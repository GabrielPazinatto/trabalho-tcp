from MainWindow import MainWindow
import sys
import time
import asyncio
from qasync import QEventLoop, asyncSlot
from PyQt6.QtWidgets import QApplication
from MusicPlayer import MusicPlayer
from Constants import INSTRUMENTS_VALUE_DICT, INSTRUMENTS_VALUE

app = QApplication(sys.argv)
loop = QEventLoop()
window = MainWindow()
player = MusicPlayer()
asyncio.set_event_loop(loop)

def play_typed_song():
    if not player._is_playing:
        player.play_song()
    else:
        player.switch_paused()

def submit_song():
    song = window.music_text_box.toPlainText()
    print(song)
    player.process_input(song)
    
def reset_song():
    player.reset()

def change_instrument():
    instrument = window.instrument_combo.currentText()
    player.set_instrument(INSTRUMENTS_VALUE_DICT[instrument])

def restart():
    player._stop_playing = True
    play_typed_song()

def stop_playing():
    player._is_playing = False

if __name__ == '__main__':

    player._init_midi()

    window.submit_button.clicked.connect(submit_song)
    window.play_button.clicked.connect(play_typed_song)
    window.instrument_combo.currentIndexChanged.connect(change_instrument)
    window.prev_button.clicked.connect(restart)
    window.next_button.clicked.connect(stop_playing)

    window.show()
    with loop:
        loop.run_forever()