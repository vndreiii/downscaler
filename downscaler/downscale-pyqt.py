from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import ffmpeg

class DownscaleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file = None

        self.init_ui()


    def get_file_path(self):
        self.file = QFileDialog.getOpenFileName(self, "Choose your file...")
        if self.file is not None:
            print(self.file)
        else:
            print("No file selected.")

    def get_folder_path(self):
        self.folder = QFileDialog.getExistingDirectory(self, "Choose your folder...")
        if self.folder is not None:
            print(self.folder)
        else:
            print("No folder selected.")

    def init_ui(self):
        self.setWindowTitle('Downscaler')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.input_label = QLabel('Choose your video:')
        self.input_dialog = QPushButton("Open File...")
        self.input_dialog.clicked.connect(self.get_file_path)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_dialog)

        self.output_label = QLabel('Specify the name of the video output:')
        self.output_dialog = QPushButton("Choose output folder...")
        self.output_dialog.clicked.connect(self.get_folder_path)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_dialog)

        self.output_text = QLineEdit()
        layout.addWidget(self.output_text)

        self.convert_button = QPushButton('Downscale')
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)

        self.central_widget.setLayout(layout)

    def convert(self):
        try:
            input_filename = self.file[0]
            output_filename = f"{self.folder}/{self.output_text.text()}_downscaled.mp4"
            print(input_filename, output_filename)
        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("No file selected. You must select one.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        try:
            ffmpeg.input(input_filename).output(output_filename, vcodec='libx264', crf=28, b='800k', preset='faster',
                                                tune='film').run()
            print("Conversion successful")
        except ffmpeg.Error as e:
            print("An error occurred:", e)


def main():
    app = QApplication([])
    window = DownscaleApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()