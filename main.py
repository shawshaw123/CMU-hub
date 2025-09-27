import sys
import warnings
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QMessageBox,
    QHBoxLayout, QVBoxLayout, QWidget
)
from PyQt6.QtCore import QSize

import resetpassword
import user_profile
import navbar
import header

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
        central_widget.setStyleSheet("background-color: #F8F9FA;")
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout (sidebar + content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add sidebar
        self.sidebar = navbar.Sidebar()
        main_layout.addWidget(self.sidebar)

        # Content area (Header + StackedWidget)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 20, 20)  
        content_layout.setSpacing(20)

        # Add Header with proper container
        header_container = QWidget()
        header_container.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 0, 0, 0) 

        self.header = header.Header()
        header_layout.addWidget(self.header)
        content_layout.addWidget(header_container)

        # Content area with stacked widget
        stack_container = QWidget()
        stack_layout = QVBoxLayout(stack_container)
        stack_layout.setContentsMargins(20, 0, 0, 0)  
        stack_layout.setSpacing(0)
        
        self.stack = QStackedWidget()
        stack_layout.addWidget(self.stack)
        content_layout.addWidget(stack_container, 1)  

        main_layout.addWidget(content_widget, 1)

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
        self.stack.setCurrentWidget(self.profile_page)

    def navigate_to_subsection(self, section, sub_btn):
        """Navigate to a subsection"""
        section_name = section.main_btn.text().replace("  ", "").strip()
        subsection_name = sub_btn.text()
        print(f"Navigating to subsection: {section_name} > {subsection_name}")
        self.stack.setCurrentWidget(self.profile_page)

    def mousePressEvent(self, event):
        """Close popups when clicking elsewhere."""
        # Check if the mail or notification menus in the header are visible and hide them
        if self.header.mail_menu.isVisible():
            self.header.mail_menu.hide()

        if self.header.notif_menu.isVisible():
            self.header.notif_menu.hide()

        super().mousePressEvent(event)

    def closeEvent(self, event):
        if QMessageBox.question(self, "Exit", "Are you sure you want to exit?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
