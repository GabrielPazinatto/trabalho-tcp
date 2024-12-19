from MainWindow import MainWindow
import asyncio
from qasync import QEventLoop
from PyQt6.QtWidgets import QApplication
from MusicPlayer import MusicPlayer
from Constants import INSTRUMENTS_VALUE_DICT
from music_saver import save_music


class Application:
    def __init__(self):
        self.app = QApplication([])
        self.loop = QEventLoop()
        asyncio.set_event_loop(self.loop)

        self.window = MainWindow()
        self.player = MusicPlayer()

        self._configure_buttons()
        self.player._init_midi()

    def _configure_buttons(self):
        self.window.submit_button.clicked.connect(self.submit_song)
        self.window.play_button.clicked.connect(self.play_typed_song)
        self.window.play_button.clicked.connect(self.change_button_icon)
        self.window.instrument_combo.currentIndexChanged.connect(self.change_instrument)
        self.window.next_button.clicked.connect(self.stop_playing)
        self.window.prev_button.clicked.connect(self.restart_song)
        self.window.save_button.clicked.connect(self.save_song)
        self.window.loop_button.clicked.connect(self.set_repeat_song)
        self.window.bpm_input.returnPressed.connect(self.adjust_bpm)

    def run(self):
        self.window.show()
        with self.loop:
            self.loop.run_forever()

    def play_typed_song(self):
        if not self.player.get_is_playing():
            self.player.play_song()
        else:
            self.player.switch_paused()

    def submit_song(self):
        song = self.window.music_text_box.toPlainText()
        self.player.process_input(song)

    def change_instrument(self):
        instrument = self.window.instrument_combo.currentText()
        self.player.set_instrument(INSTRUMENTS_VALUE_DICT[instrument])

    def adjust_bpm(self):
        try:
            bpm = 60000 / int(self.window.bpm_input.text())
        except ValueError:
            bpm = 500
        self.player.set_wait_time(bpm)

    def stop_playing(self):
        self.player.set_stop_playing(True)

    def restart_song(self):
        self.player.reset()
        self.player.reset_song()

    def set_repeat_song(self):
        self.player.switch_repeat_song()
        if self.player.get_repeat_song():
            self.window.loop_button.set_background_color("Lime")
        else:
            self.window.loop_button.set_background_color("#1A1A1A")

    def change_button_icon(self):
        if self.player.get_paused():
            self.window.play_button.set_icon_pause()
        else:
            self.window.play_button.set_icon_play()

    def save_song(self):
        text = self.window.music_text_box.toPlainText()
        save_music(
            text=text,
            filename="output.mid",
            instrument=self.player._instrument,
            octave_modifier=self.player._octave_modifier,
            bpm=(60000 / self.player.get_wait_time()),
            volume=self.player._volume,
        )