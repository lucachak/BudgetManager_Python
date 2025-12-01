from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QMessageBox, 
                            QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QColor

from views.styles.styles import HyprlandStyles

class LoginWindow(QWidget):
    login_successful = pyqtSignal()
    
    def __init__(self, auth_model):
        super().__init__()
        self.auth_model = auth_model
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        self.setWindowTitle("Budget Manager - Login")
        
        # Use minimum size instead of fixed size for responsiveness
        self.setMinimumSize(580, 680)
        self.setMaximumSize(1920, 1080)
        
        # Main layout with proper margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create a central container that will handle the responsive design
        central_container = QFrame()
        central_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        central_container.setStyleSheet(f"""
            QFrame {{
                background-color: {HyprlandStyles.BACKGROUND_PRIMARY};
                border: none;
            }}
        """)
        
        container_layout = QVBoxLayout(central_container)
        container_layout.setContentsMargins(24, 32, 24, 32)
        container_layout.setSpacing(0)
        
        # Header section - responsive
        header_section = self.create_header_section()
        container_layout.addWidget(header_section)
        
        # Add some flexible space
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Form section - responsive
        form_section = self.create_form_section()
        container_layout.addWidget(form_section)
        
        # Add some flexible space
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Footer section
        footer_section = self.create_footer_section()
        container_layout.addWidget(footer_section)
        
        main_layout.addWidget(central_container)
        
        # Connect Enter key to login
        self.username_input.returnPressed.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)
    
    def create_header_section(self):
        header_frame = QFrame()
        header_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(16)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App icon - responsive size
        icon_frame = QFrame()
        icon_frame.setFixedSize(80, 80)  # Slightly larger for better proportions
        icon_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {HyprlandStyles.ACCENT_PRIMARY}, 
                    stop:1 {HyprlandStyles.ACCENT_SECONDARY});
                border-radius: 20px;
            }}
        """)
        
        icon_layout = QVBoxLayout(icon_frame)
        icon_label = QLabel("💰")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                background: transparent;
                color: white;
            }
        """)
        icon_layout.addWidget(icon_label)
        
        # Title section
        title_label = QLabel("Budget Manager")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="xl"))
        title_label.setWordWrap(True)
        
        subtitle_label = QLabel("Welcome back to your financial dashboard")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(HyprlandStyles.get_label_style(size="medium"))
        subtitle_label.setWordWrap(True)
        
        header_layout.addWidget(icon_frame)
        header_layout.addSpacing(8)
        header_layout.addWidget(title_label)
        header_layout.addSpacing(4)
        header_layout.addWidget(subtitle_label)
        
        return header_frame
    
    def create_form_section(self):
        form_frame = QFrame()
        form_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        
        # Username field container
        username_container = QFrame()
        username_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        username_layout = QVBoxLayout(username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_layout.setSpacing(8)
        
        username_label = QLabel("Username")
        username_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setText("admin")
        self.username_input.setMinimumHeight(48)
        self.username_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password field container
        password_container = QFrame()
        password_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        password_layout = QVBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(8)
        
        password_label = QLabel("Password")
        password_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setText("admin")
        self.password_input.setMinimumHeight(48)
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"""
            QLabel {{
                color: {HyprlandStyles.ACCENT_ERROR};
                font-size: 12px;
                padding: 12px;
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                border-radius: 6px;
                border-left: 4px solid {HyprlandStyles.ACCENT_ERROR};
            }}
        """)
        self.error_label.setVisible(False)
        self.error_label.setWordWrap(True)
        self.error_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setMinimumHeight(52)
        self.login_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.login_button.clicked.connect(self.attempt_login)
        
        form_layout.addWidget(username_container)
        form_layout.addWidget(password_container)
        form_layout.addWidget(self.error_label)
        form_layout.addWidget(self.login_button)
        
        return form_frame
    
    def create_footer_section(self):
        footer_frame = QFrame()
        footer_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(8)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        help_text = QLabel("Use: <b>admin</b> / <b>admin</b>")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_text.setStyleSheet(f"""
            QLabel {{
                color: {HyprlandStyles.TEXT_MUTED};
                font-size: 12px;
                padding: 8px;
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                border-radius: 6px;
            }}
        """)
        help_text.setWordWrap(True)
        
        copyright_text = QLabel("© 2024 Budget Manager")
        copyright_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_text.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        
        footer_layout.addWidget(help_text)
        footer_layout.addWidget(copyright_text)
        
        return footer_frame
    
    def apply_styles(self):
        # Apply input styles
        input_style = f"""
            QLineEdit {{
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                border: 2px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: {HyprlandStyles.TEXT_PRIMARY};
                font-family: {HyprlandStyles.FONT_FAMILY};
                selection-background-color: {HyprlandStyles.ACCENT_PRIMARY};
            }}
            QLineEdit:focus {{
                border-color: {HyprlandStyles.ACCENT_PRIMARY};
                background-color: {HyprlandStyles.BACKGROUND_CARD};
            }}
            QLineEdit[error="true"] {{
                border-color: {HyprlandStyles.ACCENT_ERROR};
            }}
        """
        
        self.username_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        
        # Button style - fixed to remove unsupported properties
        button_style = f"""
            QPushButton {{
                background-color: {HyprlandStyles.ACCENT_PRIMARY};
                color: {HyprlandStyles.BACKGROUND_PRIMARY};
                border: none;
                padding: 16px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                font-family: {HyprlandStyles.FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: #8ab4f8;
            }}
            QPushButton:pressed {{
                background-color: #6699ff;
            }}
            QPushButton:disabled {{
                background-color: {HyprlandStyles.TEXT_MUTED};
                color: {HyprlandStyles.TEXT_SECONDARY};
            }}
        """
        self.login_button.setStyleSheet(button_style)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Clear any previous errors
        self.clear_error()
        
        # Simulate loading
        original_text = self.login_button.text()
        self.login_button.setText("Signing in...")
        self.login_button.setEnabled(False)
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(500, lambda: self.process_login(username, password, original_text))
    
    def process_login(self, username: str, password: str, original_text: str):
        if self.auth_model.authenticate(username, password):
            self.login_successful.emit()
        else:
            self.show_error("Invalid credentials. Please use username: admin and password: admin")
        
        self.login_button.setText(original_text)
        self.login_button.setEnabled(True)
    
    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)
        
        # Add error styling to inputs
        self.username_input.setProperty("error", "true")
        self.password_input.setProperty("error", "true")
        
        # Re-apply styles to update the error state
        self.apply_styles()
    
    def clear_error(self):
        self.error_label.setVisible(False)
        self.username_input.setProperty("error", "false")
        self.password_input.setProperty("error", "false")
        self.apply_styles()
    
    def sizeHint(self):
        return QSize(400, 550)
    
    def resizeEvent(self, event):
        """Handle window resize events for better responsiveness"""
        super().resizeEvent(event)
        # You can add any responsive behavior here if needed
    
    def showEvent(self, event):
        """Center the window when shown"""
        super().showEvent(event)
        # Center on screen
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
