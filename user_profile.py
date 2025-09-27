from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QIcon
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QStackedWidget, QGraphicsDropShadowEffect,
    QDialog, QListWidget, QListWidgetItem, QGraphicsBlurEffect,
    QLineEdit, QGridLayout
)
from resume_builder import ResumeBuilderDialog


class ProfileWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:#f4f5f7;")
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # ---------------- Profile Title ----------------
        profile_title = QLabel("Profile")
        profile_title.setStyleSheet("font:22px bold;color:#14532d;margin-top:12px;margin-bottom:8px;background:transparent;")
        root.addWidget(profile_title)

        # ---------------- Main Content ----------------
        main = QHBoxLayout()
        main.setSpacing(24)

        # ---- Profile Card (left) ----
        profile_card = QFrame()
        profile_card.setStyleSheet("background:white;border-radius:12px;")
        profile_card.setFixedSize(360, 520)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        profile_card.setGraphicsEffect(shadow)

        p = QVBoxLayout(profile_card)
        p.setContentsMargins(30, 30, 30, 30)
        p.setSpacing(16)

        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(140, 140)
        self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_lbl.setStyleSheet("border:3px solid #dee2e6;border-radius:70px;background:#e9ecef;")
        p.addWidget(self.avatar_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

        p.addWidget(QLabel("2022301108", styleSheet="font:18px bold;color:#1e4d2b;background:transparent;"),
                    alignment=Qt.AlignmentFlag.AlignCenter)
        p.addWidget(QLabel("s.castro.carlosfidel@coc.edu.ph", styleSheet="color:#6c757d;background:transparent;"),
                    alignment=Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("Change Profile Picture")
        btn.setFixedSize(200, 36)
        btn.setStyleSheet("background:#084924;color:white;border:none;border-radius:8px;font-weight:bold")
        btn.clicked.connect(self.show_change_page)
        p.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Info
        for k, v in [
            ("Name", "Carlos Fidel Castro"),
            ("Course", "BS Information Technology"),
            ("Role", "Student"),
            ("Year", "3rd"),
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{k}:", styleSheet="font-weight:bold;background:transparent;"))
            row.addWidget(QLabel(v, styleSheet="background:transparent;"))
            p.addLayout(row)

        p.addStretch()

        # ---- Resume Card (right) ----
        resume_card = QFrame()
        resume_card.setStyleSheet("background:white; border-radius:12px;")
        resume_card.setFixedSize(640, 520)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(12)
        shadow2.setOffset(0, 2)
        resume_card.setGraphicsEffect(shadow2)

        r = QVBoxLayout(resume_card)
        r.setContentsMargins(20, 20, 20, 20)
        r.setSpacing(8)

        # Resume title
        resume_title = QLabel("Resume")
        resume_title.setStyleSheet("font:18px bold; color:#084924;background:transparent;")
        r.addWidget(resume_title)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background:#d3d3d3; margin:4px 0;")
        r.addWidget(line)

        # Section header with title and add button
        section_header = QHBoxLayout()
        
        # Section title that will update based on current page
        self.section_title = QLabel("Education")
        self.section_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #084924;background:transparent;")
        
        section_header.addWidget(self.section_title)
        section_header.addStretch()
        
        # Add button
        add_btn = QPushButton("+")
        add_btn.setFixedSize(24, 24)
        add_btn.setStyleSheet("""
            QPushButton {
                background: #15803d;
                color: white;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #166534;
            }
        """)
        add_btn.clicked.connect(lambda: self.handle_add_click())
        section_header.addWidget(add_btn)
        r.addLayout(section_header)

        # Create stacked widget for different sections
        self.resume_stack = QStackedWidget()
        
        # 1. Education Section
        edu_widget = QWidget()
        edu_layout = QVBoxLayout(edu_widget)
        
        # Education Table (2 columns)
        self.table1 = QTableWidget(2, 2)
        self.table1.setHorizontalHeaderLabels(["School", "School Year"])
        self.table1.setItem(0, 0, QTableWidgetItem("Valencia National High School"))
        self.table1.setItem(0, 1, QTableWidgetItem("2005–2006"))
        self.table1.setItem(1, 0, QTableWidgetItem("Central Mindanao University"))
        self.table1.setItem(1, 1, QTableWidgetItem("2006–2012"))
        edu_layout.addWidget(self.table1)
        self.resume_stack.addWidget(edu_widget)
        
        # 2. Work Experience Section
        work_widget = QWidget()
        work_layout = QVBoxLayout(work_widget)
        
        self.table2 = QTableWidget(1, 2)
        self.table2.setHorizontalHeaderLabels(["Company", "Duration"])
        self.table2.setItem(0, 0, QTableWidgetItem("ABC Company"))
        self.table2.setItem(0, 1, QTableWidgetItem("2020-2022"))
        work_layout.addWidget(self.table2)
        self.resume_stack.addWidget(work_widget)
        
        # 3. Skills & Awards Section
        skills_widget = QWidget()
        skills_layout = QVBoxLayout(skills_widget)
        
        self.table3 = QTableWidget(2, 5)
        self.table3.setHorizontalHeaderLabels(["Skill", "Proficiency", "Award", "Date", "Presenter"])
        self.table3.setItem(0, 0, QTableWidgetItem("Python Programming"))
        self.table3.setItem(0, 1, QTableWidgetItem("Advanced"))
        self.table3.setItem(0, 2, QTableWidgetItem(""))
        self.table3.setItem(0, 3, QTableWidgetItem(""))
        self.table3.setItem(0, 4, QTableWidgetItem(""))
        self.table3.setItem(1, 0, QTableWidgetItem(""))
        self.table3.setItem(1, 1, QTableWidgetItem(""))
        self.table3.setItem(1, 2, QTableWidgetItem("Best Employee Award"))
        self.table3.setItem(1, 3, QTableWidgetItem("2022"))
        self.table3.setItem(1, 4, QTableWidgetItem("Company ABC"))
        
        # Set row height to accommodate wrapped text
        self.table3.verticalHeader().setDefaultSectionSize(60)
        
        skills_layout.addWidget(self.table3)
        self.resume_stack.addWidget(skills_widget)
        
        # Apply table styling after all tables are created
        self.make_table(self.table1, "#14532d")
        self.make_table(self.table2, "#084924")
        self.make_table(self.table3, "#084924")
        
        r.addWidget(self.resume_stack)

        # Pagination buttons with click handlers
        self.page_buttons = []
        pagination = QHBoxLayout()
        pagination.addStretch()
        
        for i in range(1, 4):
            btn = QPushButton(str(i))
            btn.setFixedSize(32, 32)
            if i == 1:
                btn.setStyleSheet("background:#084924; color:white; border-radius:6px;")
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: white;
                        color: #084924;
                        border: 1px solid #ccc;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background: #f0f0f0;
                    }
                """)
            btn.clicked.connect(lambda checked, x=i-1: self.switch_resume_section(x))
            self.page_buttons.append(btn)
            pagination.addWidget(btn)
            
        pagination.addStretch()
        r.addLayout(pagination)

        # ---- Create Resume Button ----
        create_resume_layout = QHBoxLayout()
        create_resume_layout.addStretch()
        create_resume_btn = QPushButton("Create Resume")
        create_resume_btn.setFixedSize(150, 36)
        create_resume_btn.setStyleSheet("""
            QPushButton {
                background: #084924;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #06381c;
            }
        """)
        create_resume_btn.clicked.connect(self.show_resume_builder)
        create_resume_layout.addWidget(create_resume_btn)
        r.addLayout(create_resume_layout)

        # ---- Stack (Profile + Resume / Change Page) ----
        self.stack = QStackedWidget()
        main_page = QWidget()
        ml = QHBoxLayout(main_page)
        ml.setSpacing(24)
        ml.addWidget(profile_card)
        ml.addWidget(resume_card)
        self.stack.addWidget(main_page)

        # Change picture page
        change_page = QWidget()
        ch = QVBoxLayout(change_page)
        ch.setContentsMargins(80, 80, 80, 80)
        ch.setSpacing(20)
        ch.addWidget(QLabel("Change Profile Picture", styleSheet="font:22px bold;color:#084924;background:transparent;"),
                     alignment=Qt.AlignmentFlag.AlignCenter)

        self.preview_lbl = QLabel()
        self.preview_lbl.setFixedSize(120, 120)
        self.preview_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_lbl.setStyleSheet("border:2px solid #dee2e6;border-radius:60px;background:#e9ecef;")
        ch.addWidget(self.preview_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

        choose_btn = QPushButton("Choose File")
        choose_btn.setFixedSize(120, 36)
        choose_btn.setStyleSheet("color:#084924; font-weight:bold; background:transparent; border:none;")
        choose_btn.clicked.connect(self.choose_avatar)

        save_btn = QPushButton("Save")
        save_btn.setFixedSize(120, 36)
        save_btn.setStyleSheet("background:#084924;color:white;border:none;border-radius:8px")
        save_btn.clicked.connect(self.save_avatar)

        back_btn = QPushButton("Back")
        back_btn.setFixedSize(120, 36)
        back_btn.setStyleSheet("background:#6c757d;color:white;border:none;border-radius:8px")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        hb = QHBoxLayout()
        hb.addStretch()
        hb.addWidget(choose_btn)
        hb.addWidget(save_btn)
        hb.addWidget(back_btn)
        hb.addStretch()
        ch.addLayout(hb)

        ch.addStretch()
        self.stack.addWidget(change_page)

        root.addWidget(self.stack)

        # Default avatar
        self.set_avatar(":default")

    # ---------------- Helpers ----------------
    def make_table(self, table, header_color="#15803d"):
        table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setWordWrap(True)  # Enable text wrapping
        table.setStyleSheet(f"""
            QHeaderView::section {{
                background: {header_color};
                color: white;
                font-weight: bold;
                height: 32px;
            }}
            QTableWidget {{
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 4px;
                background: white;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }}
            QTableWidget::item:selected {{
                background: #e8f5e9;
            }}
            QTableWidget::item:alternate {{
                background: #f9f9f9;
            }}
        """)
        
        # Set different resize modes for different tables
        if table == self.table3:  # Skills & Awards table with 5 columns
            # Set specific column widths for better display
            table.setColumnWidth(0, 120)  # Skill
            table.setColumnWidth(1, 100)  # Proficiency
            table.setColumnWidth(2, 120)  # Award
            table.setColumnWidth(3, 80)   # Date
            table.setColumnWidth(4, 120)  # Presenter
            # Make the table wider to accommodate all columns
            table.setMinimumWidth(540)
        else:
            # For other tables, use stretch mode
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def show_change_page(self):
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(8)
        self.setGraphicsEffect(blur)

        dlg = ChangeProfileDialog(self)
        dlg.exec()

        self.setGraphicsEffect(None)

    def set_avatar(self, path):
        if path == ":default":
            self.avatar_lbl.setPixmap(QPixmap())
            self.avatar_lbl.setText("👨‍💼")
            self.preview_lbl.setPixmap(QPixmap())
            self.preview_lbl.setText("👨‍💼")
            return
        pixmap = QPixmap(path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                      Qt.TransformationMode.SmoothTransformation)
        rounded = QPixmap(120, 120)
        rounded.fill(Qt.GlobalColor.transparent)
        p = QPainter(rounded)
        clip = QPainterPath()
        clip.addEllipse(0, 0, 120, 120)
        p.setClipPath(clip)
        p.drawPixmap(0, 0, pixmap)
        p.end()
        self.avatar_lbl.setPixmap(rounded)
        self.avatar_lbl.setText("")
        self.preview_lbl.setPixmap(rounded)
        self.preview_lbl.setText("")

    def choose_avatar(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Picture", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file:
            self.set_avatar(file)

    def save_avatar(self):
        QMessageBox.information(self, "Success", "Profile picture updated!")
        self.stack.setCurrentIndex(0)

    def handle_add_click(self):
        current_index = self.resume_stack.currentIndex()
        if current_index == 0:
            self.add_education()
        elif current_index == 1:
            self.add_work_experience()
        elif current_index == 2:
            self.add_skill_award()

    def show_success_message(self, message):
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(5)
        self.setGraphicsEffect(self.blur_effect)
        
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle("Success")
        self.msg_box.setText(message)
        self.msg_box.setIcon(QMessageBox.Icon.Information)
        self.msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
            QLabel {
                font-size: 14px;
                color: #14532d;
                background: transparent;
            }
            QPushButton {
                background-color: #15803d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #166534;
            }
        """)
        
        self.msg_box.finished.connect(lambda: self.setGraphicsEffect(None))
        self.msg_box.exec()

    def add_education(self):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)
        self.setGraphicsEffect(blur_effect)
        
        dialog = AddEducationDialog(self)
        dialog.finished.connect(lambda: self.setGraphicsEffect(None))
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            institution = dialog.institution.text()
            duration = dialog.duration.text()
            if institution and duration:
                row = self.table1.rowCount()
                self.table1.insertRow(row)
                self.table1.setItem(row, 0, QTableWidgetItem(institution))
                self.table1.setItem(row, 1, QTableWidgetItem(duration))
                self.show_success_message("Education added successfully!")
        else:
            self.setGraphicsEffect(None)

    def add_work_experience(self):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)
        self.setGraphicsEffect(blur_effect)
        
        dialog = AddWorkExperienceDialog(self)
        dialog.finished.connect(lambda: self.setGraphicsEffect(None))
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            company = dialog.company.text()
            duration = dialog.duration.text()
            if company and duration:
                row = self.table2.rowCount()
                self.table2.insertRow(row)
                self.table2.setItem(row, 0, QTableWidgetItem(company))
                self.table2.setItem(row, 1, QTableWidgetItem(duration))
                self.show_success_message("Work experience added successfully!")
        else:
            self.setGraphicsEffect(None)

    def switch_resume_section(self, index):
        section_titles = ["Education", "Work Experience", "Skills & Awards"]
        self.section_title.setText(section_titles[index])
        
        for i, btn in enumerate(self.page_buttons):
            if i == index:
                btn.setStyleSheet("background:#14532d; color:white; border-radius:6px;")
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: white;
                        color: #14532d;
                        border: 1px solid #ccc;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background: #f0f0f0;
                    }
                """)
        
        self.resume_stack.setCurrentIndex(index)

    def show_resume_builder(self):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)
        self.setGraphicsEffect(blur_effect)

        dialog = ResumeBuilderDialog(self)
        dialog.finished.connect(lambda: self.setGraphicsEffect(None))
        dialog.exec()

    def add_skill_award(self):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)
        self.setGraphicsEffect(blur_effect)
        
        dialog = AddSkillAwardDialog(self)
        dialog.finished.connect(lambda: self.setGraphicsEffect(None))
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            skill = dialog.skill.text()
            proficiency = dialog.proficiency.text()
            award = dialog.award.text()
            date = dialog.date.text()
            presenter = dialog.presenter.text()
            
            if skill or award:
                row = self.table3.rowCount()
                self.table3.insertRow(row)
                self.table3.setItem(row, 0, QTableWidgetItem(skill if skill else ""))
                self.table3.setItem(row, 1, QTableWidgetItem(proficiency if proficiency else ""))
                self.table3.setItem(row, 2, QTableWidgetItem(award if award else ""))
                self.table3.setItem(row, 3, QTableWidgetItem(date if date else ""))
                self.table3.setItem(row, 4, QTableWidgetItem(presenter if presenter else ""))
                
                if skill and award:
                    self.show_success_message("Skill and Award added successfully!")
                elif skill:
                    self.show_success_message("Skill added successfully!")
                else:
                    self.show_success_message("Award added successfully!")
        else:
            self.setGraphicsEffect(None)


class ChangeProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Change Profile Picture")
        self.setModal(True)
        self.setFixedSize(520, 400)
        self.setStyleSheet("""
            QDialog { 
                background: white; 
                border-radius: 18px;
                border: 1px solid #d1d5db;
            }
            QPushButton { 
                border: none; 
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        # Title
        title = QLabel("Change Profile Picture")
        title.setStyleSheet("font: 22px bold; color: #14532d; margin-bottom: 20px; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Left side - Recent Uploaded Images
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        
        recent_label = QLabel("Recent Uploaded Images")
        recent_label.setStyleSheet("font: 15px bold; color: #084924; margin-bottom: 8px; background: transparent;")
        left_layout.addWidget(recent_label)
        
        # Recent images list
        self.recent_list = QListWidget()
        self.recent_list.setFixedSize(180, 180)
        self.recent_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d1d5db;
                border-radius: 10px;
                background: #f9fafb;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e5e7eb;
                background: transparent;
            }
            QListWidget::item:selected {
                background: transparent;
                color: inherit;
            }
            QListWidget::item:hover {
                background: #f0f0f0;
            }
        """)
        
        # Add sample recent images
        for i in range(3):
            item = QListWidgetItem(f"Profile_{i+1}.png")
            self.recent_list.addItem(item)
            
        left_layout.addWidget(self.recent_list)
        content_layout.addLayout(left_layout)

        # Right side - Upload File
        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)
        
        upload_label = QLabel("Upload File")
        upload_label.setStyleSheet("font: 15px bold; color: #14532d; margin-bottom: 8px; background: transparent;")
        right_layout.addWidget(upload_label)
        
        # Upload area
        upload_frame = QFrame()
        upload_frame.setFixedSize(180, 180)
        upload_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #9ca3af;
                border-radius: 10px;
                background: #f9fafb;
            }
        """)
        
        upload_inner = QVBoxLayout(upload_frame)
        upload_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_inner.setSpacing(12)
        
        
        # Upload text
        upload_text = QLabel("Drag & Drop here\nor")
        upload_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_text.setStyleSheet("color: #6b7280; background: transparent;")
        upload_inner.addWidget(upload_text)
        
        # Browse button
        browse_btn = QPushButton("Browse")
        browse_btn.setFixedSize(100, 32)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #084924;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #06381c;
            }
        """)
        browse_btn.clicked.connect(self.browse_image)
        upload_inner.addWidget(browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        right_layout.addWidget(upload_frame)
        content_layout.addLayout(right_layout)

        layout.addLayout(content_layout)

        # Buttons at the bottom
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(100, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #6b7280;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b5563;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(100, 36)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #084924;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #06381c;
            }
        """)
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)

        self.selected_image = None

    def browse_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file:
            self.selected_image = file
            item = QListWidgetItem(file.split("/")[-1])
            self.recent_list.insertItem(0, item)
            QMessageBox.information(self, "Selected", f"Selected file:\n{file}")


class AddEducationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Add Education")
        self.setModal(True)
        self.setFixedSize(440, 260)
        self.setStyleSheet("""
            QDialog { background: white; border-radius: 18px; border: 1px solid #d1d5db; }
            QLabel { font: 14px; color: #333; background: transparent; }
            QLineEdit { border: 1px solid #ccc; border-radius: 10px; padding: 8px; }
            QPushButton { 
                background: #198754; 
                color: white; 
                border: none; 
                border-radius: 10px; 
                padding: 8px 16px; 
                font-weight: bold; 
            }
            QPushButton:hover {
                background: #166534;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Degree
        self.degree = QLineEdit()
        self.degree.setPlaceholderText("Enter your degree")
        layout.addWidget(self.degree)

        # Institution
        self.institution = QLineEdit()
        self.institution.setPlaceholderText("Enter institution name")
        layout.addWidget(self.institution)

        # Duration
        self.duration = QLineEdit()
        self.duration.setPlaceholderText("Enter duration (e.g., 2018-2022)")
        layout.addWidget(self.duration)

        # Buttons
        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)

        save = QPushButton("Save")
        save.clicked.connect(self.accept)
        btns.addWidget(save)

        layout.addLayout(btns)


class AddWorkExperienceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Add Work Experience")
        self.setModal(True)
        self.setFixedSize(440, 260)
        self.setStyleSheet("""
            QDialog { background: white; border-radius: 18px; border: 1px solid #d1d5db; }
            QLabel { font: 14px; color: #333; background: transparent; }
            QLineEdit { border: 1px solid #ccc; border-radius: 10px; padding: 8px; }
            QPushButton { 
                background: #198754; 
                color: white; 
                border: none; 
                border-radius: 10px; 
                padding: 8px 16px; 
                font-weight: bold; 
            }
            QPushButton:hover {
                background: #166534;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Company
        self.company = QLineEdit()
        self.company.setPlaceholderText("Enter company name")
        layout.addWidget(self.company)

        # Position
        self.position = QLineEdit()
        self.position.setPlaceholderText("Enter your position")
        layout.addWidget(self.position)

        # Duration
        self.duration = QLineEdit()
        self.duration.setPlaceholderText("Enter duration (e.g., 2020-2022)")
        layout.addWidget(self.duration)

        # Buttons
        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)

        save = QPushButton("Save")
        save.clicked.connect(self.accept)
        btns.addWidget(save)

        layout.addLayout(btns)


class AddSkillAwardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Add Skill/Award")
        self.setModal(True)
        self.setFixedSize(480, 420)  # ⬅ Bigger height for 5 fields
        self.setStyleSheet("""
            QDialog { 
                background: white; 
                border-radius: 18px; 
                border: 1px solid #d1d5db; 
            }
            QLabel { font: 14px; color: #333; background: transparent; }
            QLineEdit { 
                border: 1px solid #ccc; 
                border-radius: 10px; 
                padding: 10px; 
                font-size: 14px;
            }
            QPushButton { 
                background: #198754; 
                color: white; 
                border: none; 
                border-radius: 10px; 
                padding: 10px 18px; 
                font-weight: bold; 
            }
            QPushButton:hover {
                background: #166534;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Skill
        self.skill = QLineEdit()
        self.skill.setPlaceholderText("Enter skill name")
        layout.addWidget(self.skill)

        # Proficiency
        self.proficiency = QLineEdit()
        self.proficiency.setPlaceholderText("Enter proficiency level")
        layout.addWidget(self.proficiency)

        # Award
        self.award = QLineEdit()
        self.award.setPlaceholderText("Enter award name (if any)")
        layout.addWidget(self.award)

        # Date
        self.date = QLineEdit()
        self.date.setPlaceholderText("Enter date received")
        layout.addWidget(self.date)

        # Presenter
        self.presenter = QLineEdit()
        self.presenter.setPlaceholderText("Enter presenter name (if any)")
        layout.addWidget(self.presenter)

        # Buttons
        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)

        save = QPushButton("Save")
        save.clicked.connect(self.accept)
        btns.addWidget(save)

        layout.addLayout(btns)
