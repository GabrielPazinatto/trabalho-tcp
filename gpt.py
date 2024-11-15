from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QSlider, QFormLayout, QSpacerItem, QSizePolicy, QGridLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window title and increased size
        self.setWindowTitle("Audio Player")
        self.setFixedSize(1000, 600)  # Increased window size
        self.setStyleSheet("background-color: #1a1a1a; color: white;")

        # Main layout
        main_layout = QVBoxLayout()

        # Texto Label, Text Box, and Submit Button
        texto_label = QLabel("Texto")
        texto_label.setStyleSheet("color: white;")
        
        texto_textedit = QTextEdit()
        texto_textedit.setStyleSheet("background-color: #333333; color: white;")
        texto_textedit.setFixedHeight(450)  # Adjust height for a larger text box

        # Grid layout to tightly align label and text box
        texto_layout = QGridLayout()
        texto_layout.setVerticalSpacing(0)  # No vertical spacing between label and text box
        texto_layout.addWidget(texto_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        texto_layout.addWidget(texto_textedit, 1, 0)

        # Submit Button for Texto
        submit_button = QPushButton("Gerar Música")
        submit_button.setStyleSheet("background-color: white; color: black;")
        texto_layout.addWidget(submit_button, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)

        # Right panel for Arquivo, BPM, and Instrumento with adjustments
        right_panel = QFormLayout()
        right_panel.setSpacing(25)  # Increased spacing between rows for larger window
        right_panel.setContentsMargins(0,20,0,0)

        # BPM field
        bpm_label = QLabel("Bpm")
        bpm_label.setStyleSheet("color: white;")
        bpm_input = QLineEdit()
        bpm_input.setStyleSheet("background-color: #333333; color: white;")
        right_panel.addRow(bpm_label, bpm_input)

        # Spacer between BPM and Instrumento fields
        right_panel.addItem(QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Instrumento field
        instrumento_label = QLabel("Instrumento")
        instrumento_label.setStyleSheet("color: white;")
        instrumento_combo = QComboBox()
        instrumento_combo.addItems(["Piano", "Guitar", "Drums"])  # Example items
        instrumento_combo.setStyleSheet("background-color: #333333; color: white;")
        right_panel.addRow(instrumento_label, instrumento_combo)

        # Layout for Text and Right Panel
        top_layout = QHBoxLayout()
        top_layout.addLayout(texto_layout, 3)
        top_layout.addLayout(right_panel, 1)

        # Import Button (changed from Download)
        import_button = QPushButton("Importar Arquivo de Texto")
        import_button.setStyleSheet("background-color: white; color: black;")
        import_button.setFixedHeight(50)  # Increase button height for better visibility in the larger UI

        # Playback Controls
        playback_layout = QHBoxLayout()
        
        play_button = QPushButton()
        play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        play_button.setFixedSize(50, 50)  # Larger buttons for the bigger window
        
        prev_button = QPushButton()
        prev_button.setIcon(QIcon.fromTheme("media-skip-backward"))
        prev_button.setFixedSize(50, 50)
        
        next_button = QPushButton()
        next_button.setIcon(QIcon.fromTheme("media-skip-forward"))
        next_button.setFixedSize(50, 50)
        
        loop_button = QPushButton()
        loop_button.setIcon(QIcon.fromTheme("media-playlist-repeat"))
        loop_button.setFixedSize(50, 50)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setFixedHeight(30)  # Increase slider height for better visibility

        playback_layout.addWidget(play_button)
        playback_layout.addWidget(slider)
        playback_layout.addWidget(prev_button)
        playback_layout.addWidget(loop_button)
        playback_layout.addWidget(next_button)

        # Adding widgets to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(import_button)  # Updated button name and added to layout
        main_layout.addLayout(playback_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
