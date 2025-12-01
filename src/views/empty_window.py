from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QLinearGradient

from views.styles.styles import HyprlandStyles

class EmptyWindow(QWidget):
    def __init__(self):
        
        super().__init__()
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup the empty window UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Empty View")
        title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="xl"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel("This is an empty view. You can add your content here.")
        description.setStyleSheet(HyprlandStyles.get_label_style(size="medium"))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add stretch to center content
        layout.addStretch()
    
    def apply_styles(self):
        """Apply styles to the empty window"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
            }}
        """)
