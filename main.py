from ui.MainWindow import MainWindow
import sys
import asyncio
from qasync import QEventLoop, asyncSlot
from PyQt6.QtWidgets import QApplication
from MusicPlayer import MusicPlayer

app = QApplication(sys.argv)
loop = QEventLoop()
window = MainWindow()
player = MusicPlayer()
asyncio.set_event_loop(loop)

def play_typed_song():
    player.play_song()

def submit_song():
    song = window.music_text_box.toPlainText()
    print(song)
    player.process_input(song)

if __name__ == '__main__':

    player._init_midi()

    window.submit_button.clicked.connect(submit_song)
    window.play_button.clicked.connect(play_typed_song)

    window.show()
    with loop:
        loop.run_forever()