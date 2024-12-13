from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QGridLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import re

from Constants import INSTRUMENTS_VALUE_DICT, INSTRUMENTS_VALUE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        instruments = list(INSTRUMENTS_VALUE_DICT.keys())

        self.play_button = PlayBitches("media-playback-start")
        self.import_button = QPushButton()
        self.prev_button = PlayBitches("media-skip-backward")
        self.next_button = PlayBitches("media-skip-forward")
        self.loop_button = PlayBitches("media-playlist-repeat")

        self.bpm_input = QLineEdit()
        
        self.instrument_combo = QComboBox()
        
        self.music_text_box = QTextEdit()

        # Window title and increased size
        self.setWindowTitle("Audio Player")
        self.setFixedSize(1000, 600)  # Increased window size
        self.setStyleSheet("background-color: #1a1a1a; color: white;")

        # Main layout
        main_layout = QVBoxLayout()

        # Texto Label, Text Box, and Submit Button
        texto_label = QLabel("Texto")
        texto_label.setStyleSheet("color: white;")
        
        self.music_text_box = QTextEdit()
        self.music_text_box.setStyleSheet("background-color: #333333; color: white;")
        self.music_text_box.setFixedHeight(450)  # Adjust height for a larger text box

        # Grid layout to tightly align label and text box
        texto_layout = QGridLayout()
        texto_layout.setVerticalSpacing(0)  # No vertical spacing between label and text box
        texto_layout.addWidget(texto_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        texto_layout.addWidget(self.music_text_box, 1, 0)

        # Submit Button for Texto
        self.submit_button = QPushButton("Gerar Música")
        self.submit_button.setStyleSheet("background-color: white; color: black;")
        texto_layout.addWidget(self.submit_button, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)

        # Right panel for Arquivo, BPM, and Instrumento with adjustments
        right_panel = QFormLayout()
        right_panel.setSpacing(25)  # Increased spacing between rows for larger window
        right_panel.setContentsMargins(0,20,0,0)

        # BPM field
        bpm_label = QLabel("Bpm")
        bpm_label.setStyleSheet("color: white;")
        self.bpm_input.setStyleSheet("background-color: #333333; color: white;")
        right_panel.addRow(bpm_label, self.bpm_input)

        # Spacer between BPM and Instrumento fields
        right_panel.addItem(QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Instrumento field
        instrumento_label = QLabel("Instrumento")
        instrumento_label.setStyleSheet("color: white;")
        self.instrument_combo = QComboBox()
        self.instrument_combo.addItems(instruments)  # Example items
        self.instrument_combo.setStyleSheet("background-color: #333333; color: white;")
        right_panel.addRow(instrumento_label, self.instrument_combo)

        # Layout for Text and Right Panel
        top_layout = QHBoxLayout()
        top_layout.addLayout(texto_layout, 3)
        top_layout.addLayout(right_panel, 1)

        # Import Button (changed from Download)
        self.import_button = QPushButton("Importar Arquivo de Texto")
        self.import_button.setStyleSheet("background-color: white; color: black;")
        self.import_button.setFixedHeight(50)  # Increase button height for better visibility in the larger UI

        # Playback Controls
        playback_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Salvar Música")
        self.save_button.setStyleSheet("background-color: white; color: black;")
        self.save_button.setFixedHeight(50)

        playback_layout.addWidget(self.play_button)
        playback_layout.addWidget(self.prev_button)
        playback_layout.addWidget(self.loop_button)
        playback_layout.addWidget(self.next_button)

        # Adding widgets to main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(playback_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        main_layout.addWidget(self.save_button)


class PlayBitches(QPushButton):
    def __init__(self, fut_icon:str):
        super().__init__()
        self.setIcon(QIcon.fromTheme(fut_icon))
        self.setFixedSize(50, 50)

    def get_icon(self):
        return self.icon()
    
    def get_background_color(self):
        color = re.search(r"background-color:\s*(.*);", self.styleSheet())
        return color.group(1)
    
    def set_background_color(self, color) -> None:
        self.setStyleSheet(f"background-color: {color};")
        
    def set_icon_play(self) -> None:
        self.setIcon(QIcon.fromTheme("media-playback-start"))

    def set_icon_pause(self) -> None:
        self.setIcon(QIcon.fromTheme("media-playback-pause"))

    

    