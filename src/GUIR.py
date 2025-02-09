from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTextEdit, QFileDialog, QSlider, QMessageBox, QScrollArea, QFrame)

from PyQt6.QtCore import Qt
import sys
import os


global_value = 1

class PDFAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFinance Analysis Tool")
        self.setGeometry(100, 100, 1000, 1000)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Welcome to PDFinance Analysis Tool\nUpload PDFs and enter your question about them!")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        # Create a QLabel for the logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("../images/logo.png")  # Change the path if the logo is located elsewhere
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)  # Align to top-right
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignRight)

        # File Upload Section
        file_layout = QVBoxLayout()
        file_label = QLabel("Click the button below and upload your PDFs.")
        file_label.setStyleSheet("font-size: 16px; color: #444;")
        file_layout.addWidget(file_label)

        self.upload_button = QPushButton("Upload PDF")
        self.upload_button.setStyleSheet("""
            background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;
            border-radius: 12px; border: none;
        """)
        self.upload_button.clicked.connect(self.image_clicked)
        file_layout.addWidget(self.upload_button)

        layout.addLayout(file_layout)

        # Query Input Section (Reduced height to 2 lines)
        query_label = QLabel("Enter your query here!")
        query_label.setStyleSheet("font-size: 16px; color: #444;")
        layout.addWidget(query_label)

        self.text_entry = QTextEdit()
        self.text_entry.setStyleSheet("""
            font-size: 14px; padding: 5px; border-radius: 12px; border: 1px solid #ccc;
        """)
        self.text_entry.setFixedHeight(35)  # Limit height to around 1 lines
        layout.addWidget(self.text_entry)

        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("""
            background-color: #008CBA; color: white; font-size: 14px; padding: 10px;
            border-radius: 12px; border: none;
        """)
        submit_button.clicked.connect(self.submit_text)
        layout.addWidget(submit_button)

        # Output Display Section
        output_frame = QFrame()
        output_layout = QVBoxLayout()
        output_frame.setLayout(output_layout)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("""
            background-color: #fff; font-size: 14px; padding: 20px;
            border-radius: 12px;
        """)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.output_box)
        output_layout.addWidget(scroll_area)

        layout.addWidget(output_frame)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet("background-color: gray; padding: 5px; border-radius: 10px;")
        sidebar_frame.setLayout(sidebar_layout)

        broadness_label = QLabel("Broadness (number of PDFs inputted and outputted, default 1)")
        broadness_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        sidebar_layout.addWidget(broadness_label)

        self.broadness_slider = QSlider(Qt.Orientation.Horizontal)
        self.broadness_slider.setMinimum(1)
        self.broadness_slider.setMaximum(10)  # Set max to 10
        self.broadness_slider.setValue(1)  # Default value of 1
        self.broadness_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.broadness_slider.setTickInterval(1)  # Step size of 1
        self.broadness_slider.setStyleSheet("""
            padding: 5px; border-radius: 12px;
        """)

        # Initially hidden slider
        self.broadness_slider.setVisible(False)

        broadness_button = QPushButton("Change Broadness")
        broadness_button.setStyleSheet("""
             background-color: #555; color: white; font-size: 12px; padding: 5px;
             border-radius: 12px; border: none;
         """)
        broadness_button.clicked.connect(self.toggle_slider)
        sidebar_layout.addWidget(broadness_button)

        # Add a new button to send the broadness value to the output box
        self.send_broadness_button = QPushButton("Submit")
        self.send_broadness_button.setStyleSheet("""
            background-color: #f39c12; color: white; font-size: 12px; padding: 5px;
            border-radius: 12px;
        """)
        self.send_broadness_button.clicked.connect(self.send_broadness)
        self.send_broadness_button.setVisible(False)
        sidebar_layout.addWidget(self.send_broadness_button)

        # Make sidebar narrower by adjusting layout spacing
        sidebar_layout.setSpacing(5)

        sidebar_layout.addWidget(self.broadness_slider)

        layout.addWidget(sidebar_frame)

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
            background-color: red; color: white; font-size: 14px; padding: 10px;
            border-radius: 12px; border: none;
        """)
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def update_output(self, text):
        self.output_box.append(text)

    def submit_text(self):
        userInput = self.text_entry.toPlainText().strip()
        if userInput:
            self.update_output(f"User's Query: {userInput}")
            self.text_entry.clear()
            self.update_output(api.update_gui(userInput,global_value))

    def image_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if file_path:
            QMessageBox.information(self, "Success", "File uploaded successfully")
            file_name = os.path.basename(file_path)
            self.update_output(f"{file_name} uploaded successfully")
        else:
            QMessageBox.warning(self, "Error", "File was not uploaded.")

    def send_broadness(self):
        global global_value
        # Send the current broadness slider value to the output box
        value = self.broadness_slider.value()
        global_value = value
        self.update_output(f"Broadness value: {value}")

    def toggle_slider(self):
        # Toggle visibility of the slider
        self.broadness_slider.setVisible(not self.broadness_slider.isVisible())
        self.send_broadness_button.setVisible(self.broadness_slider.isVisible())

def run_gui():
    try:
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        window = PDFAnalyzerApp()
        window.show()
        app.exec()
    except Exception as e:
        print("Fatal Error. Something is going on with the GUI loop")
