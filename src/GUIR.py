import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction, QPalette, QColor

class PDFinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("PDFinance")
        self.setGeometry(100, 100, 1000, 800)

        # Set color scheme
        self.colors = {
            "primary": "#ECA400",
            "secondary": "#EAF8BF",
            "accent": "#006992",
            "dark": "#27476E",
            "darker": "#001D4A"
        }

        # Create menu bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet(f"background-color: {self.colors['darker']}; color: white;")

        # Add menus
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")

        # Add actions to menus
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Add a label
        label = QLabel("Welcome to PDFinance", self)
        label.setStyleSheet(f"color: {self.colors['accent']}; font-size: 18px;")
        layout.addWidget(label)

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.colors['secondary']))
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFinanceApp()
    window.show()
    sys.exit(app.exec())