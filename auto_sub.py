from PyQt5.QtWidgets import *
import sys
import whisper 
import datetime 
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import threading

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto_Sub")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Enter the file path")
        self.file_path.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")


        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setStyleSheet("padding: 8px 16px; background-color: #3498db; color: white; border: none; border-radius: 4px;")


        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setStyleSheet("padding: 8px 16px; background-color: #e74c3c; color: white; border: none; border-radius: 4px;")


        self.label = QLabel("File Path:")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px;")

        layout1 = QHBoxLayout()
        layout1.addWidget(self.label)
        layout1.addWidget(self.file_path)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.upload_button)
        layout2.addWidget(self.browse_button)
        layout1.addLayout(layout2)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(layout1)
        self.progress_dialog = QProgressBar(self)
        self.progress_dialog.setGeometry(10,80,280,25)
        self.progress_dialog.setValue(0)
        main_layout.addWidget(self.progress_dialog)
        self.progress_dialog.hide()
        self.progress_complete = QLabel('Generate Subtitles..Complete!!',self)
        self.progress_complete.setStyleSheet("font-style: italic; font-size: 14px; color: #555;")
        main_layout.addWidget(self.progress_complete)
        self.progress_complete.hide()

    def upload_file(self):
        file_path = self.file_path.text()
        if file_path:
            print(f"Uploading file from {file_path}")
            self.progress_dialog.show()
            self.sub_thread = threading.Thread(target=self.generate_subtitles, args=(file_path,))
            self.sub_thread.start()

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File")
        if filename:
            self.file_path.setText(filename)

    def update_progress(self, percentage):
        self.progress_dialog.setValue(percentage)

    def subtitle_generation_finished(self):
        self.progress_dialog.setValue(100)
        print("Subtitle generation completed.")

    def generate_subtitles(self, file_path):
        model = whisper.load_model('base')
        result = model.transcribe(file_path,language='en')

        extension = file_path.split(".")[-1]
        save_target = file_path.replace(extension, 'srt')
        
        with open(save_target, 'w') as file:
            total_segments = len(result['segments'])
            for indx, segment in enumerate(result['segments']):
                file.write(str(indx + 1) + '\n')
                file.write(str(datetime.timedelta(seconds=segment['start'])) + '--->' + str(datetime.timedelta(seconds=segment['end'])) + '\n')
                file.write(segment['text'].strip() + '\n')
                file.write('\n')
                progress_percentage = (indx + 1) * 100 // total_segments
                print(progress_percentage)
                self.progress_dialog.setValue(progress_percentage)
                if(progress_percentage == 100):
                    self.progress_dialog.hide()
                    self.progress_complete.show()
            

app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
window = Window()
window.setGeometry(0, 40, size.width(), size.height())
window.show()
sys.exit(app.exec_())
