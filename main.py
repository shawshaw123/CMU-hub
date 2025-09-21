"""
CISC Virtual Hub – Main entry point
login → reset → profile (with navbar/header)
"""

import sys
import warnings
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QMessageBox, QHBoxLayout, QWidget
)
from PyQt6.QtCore import QSize

import resetpassword
import user_profile
import navbar

warnings.filterwarnings("ignore", category=DeprecationWarning)

START_WIDTH  = 1980
START_HEIGHT = 1080
MIN_WIDTH    = 1280
MIN_HEIGHT   = 720


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CISC Virtual Hub")
        self.setMinimumSize(QSize(MIN_WIDTH, MIN_HEIGHT))
        self.resize(START_WIDTH, START_HEIGHT)

        # Create central widget with horizontal layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add sidebar
        self.sidebar = navbar.Sidebar()
        main_layout.addWidget(self.sidebar)

        # Content area with stacked widget
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 1)  # Take remaining space

        # Pages
        self.profile_page = user_profile.ProfileWidget()
        self.stack.addWidget(self.profile_page)
        
        # Connect navbar navigation
        self.connect_navbar_buttons()
        
        # Set initial page
        self.stack.setCurrentWidget(self.profile_page)

    def connect_navbar_buttons(self):
        """Connect navbar buttons to page navigation"""
        # Connect main section buttons
        for section in self.sidebar.sections:
            section.main_btn.clicked.connect(lambda checked, section=section: self.navigate_to_section(section))
            
            # Connect sub-item buttons
            for i in range(section.sub_layout.count()):
                sub_btn = section.sub_layout.itemAt(i).widget()
                if sub_btn:
                    sub_btn.clicked.connect(lambda checked, section=section, sub_btn=sub_btn: self.navigate_to_subsection(section, sub_btn))

    def navigate_to_section(self, section):
        """Navigate to a main section"""
        section_name = section.main_btn.text().replace("  ", "").strip()
        print(f"Navigating to section: {section_name}")
        
        # For now, just show the profile page for all sections
        # You can add specific pages for each section later
        self.stack.setCurrentWidget(self.profile_page)

    def navigate_to_subsection(self, section, sub_btn):
        """Navigate to a subsection"""
        section_name = section.main_btn.text().replace("  ", "").strip()
        subsection_name = sub_btn.text()
        print(f"Navigating to subsection: {section_name} > {subsection_name}")
        
        # For now, just show the profile page for all subsections
        # You can add specific pages for each subsection later
        self.stack.setCurrentWidget(self.profile_page)

    def closeEvent(self, event):
        if QMessageBox.question(self, "Exit", "Are you sure you want to exit?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()