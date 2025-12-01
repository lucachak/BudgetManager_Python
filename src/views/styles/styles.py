from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class HyprlandStyles:
    # Hyprland-inspired color palette (dark theme)
    BACKGROUND_PRIMARY = "#1a1b26"      # Deep blue-black
    BACKGROUND_SECONDARY = "#16161e"    # Slightly darker
    BACKGROUND_CARD = "#24283b"         # Card background
    ACCENT_PRIMARY = "#7aa2f7"          # Bright blue
    ACCENT_SECONDARY = "#bb9af7"        # Purple
    ACCENT_SUCCESS = "#9ece6a"          # Green
    ACCENT_ERROR = "#f7768e"            # Red
    ACCENT_WARNING = "#e0af68"          # Orange
    TEXT_PRIMARY = "#c0caf5"            # Light blue-gray
    TEXT_SECONDARY = "#a9b1d6"          # Gray-blue
    TEXT_MUTED = "#565f89"              # Muted text
    BORDER_COLOR = "#292e42"            # Border color
    
    # Fonts optimized for Linux
    FONT_FAMILY = "JetBrains Mono, Fira Code, Monospace, sans-serif"
    
    @staticmethod
    def setup_app_style(app):
        """Apply Hyprland-inspired styling to the entire application"""
        app.setStyle("Fusion")
        
        # Create dark palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(HyprlandStyles.BACKGROUND_PRIMARY))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(HyprlandStyles.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(HyprlandStyles.BACKGROUND_CARD))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(HyprlandStyles.BACKGROUND_SECONDARY))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(HyprlandStyles.BACKGROUND_CARD))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(HyprlandStyles.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Text, QColor(HyprlandStyles.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(HyprlandStyles.ACCENT_PRIMARY))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(HyprlandStyles.BACKGROUND_PRIMARY))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(HyprlandStyles.ACCENT_ERROR))
        palette.setColor(QPalette.ColorRole.Link, QColor(HyprlandStyles.ACCENT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(HyprlandStyles.ACCENT_PRIMARY))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(HyprlandStyles.BACKGROUND_PRIMARY))
        
        app.setPalette(palette)
    
    @staticmethod
    def get_button_style(primary=True, size="medium"):
        sizes = {
            "small": "8px 16px",
            "medium": "12px 24px",
            "large": "16px 32px"
        }
        padding = sizes.get(size, "12px 24px")
        
        if primary:
            return f"""
                QPushButton {{
                    background-color: {HyprlandStyles.ACCENT_PRIMARY};
                    color: {HyprlandStyles.BACKGROUND_PRIMARY};
                    border: none;
                    padding: {padding};
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                    font-family: {HyprlandStyles.FONT_FAMILY};
                }}
                QPushButton:hover {{
                    background-color: #8ab4f8;
                }}
                QPushButton:pressed {{
                    background-color: #6699ff;
                    padding: {padding};
                }}
                QPushButton:disabled {{
                    background-color: {HyprlandStyles.TEXT_MUTED};
                    color: {HyprlandStyles.TEXT_SECONDARY};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: transparent;
                    color: {HyprlandStyles.ACCENT_PRIMARY};
                    border: 1px solid {HyprlandStyles.ACCENT_PRIMARY};
                    padding: {padding};
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                    font-family: {HyprlandStyles.FONT_FAMILY};
                }}
                QPushButton:hover {{
                    background-color: {HyprlandStyles.ACCENT_PRIMARY};
                    color: {HyprlandStyles.BACKGROUND_PRIMARY};
                }}
                QPushButton:pressed {{
                    background-color: #6699ff;
                    border-color: #6699ff;
                }}
            """
    
    @staticmethod
    def get_input_style():
        return f"""
            QLineEdit, QComboBox {{
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 13px;
                color: {HyprlandStyles.TEXT_PRIMARY};
                font-family: {HyprlandStyles.FONT_FAMILY};
                selection-background-color: {HyprlandStyles.ACCENT_PRIMARY};
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {HyprlandStyles.ACCENT_PRIMARY};
                background-color: {HyprlandStyles.BACKGROUND_CARD};
            }}
            QLineEdit[error="true"] {{
                border-color: {HyprlandStyles.ACCENT_ERROR};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {HyprlandStyles.TEXT_SECONDARY};
                width: 0px;
                height: 0px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 6px;
                color: {HyprlandStyles.TEXT_PRIMARY};
                selection-background-color: {HyprlandStyles.ACCENT_PRIMARY};
                selection-color: {HyprlandStyles.BACKGROUND_PRIMARY};
                outline: none;
            }}
        """
    
    @staticmethod
    def get_label_style(heading=False, size="medium"):
        sizes = {
            "small": "11px",
            "medium": "13px",
            "large": "16px",
            "xl": "20px"
        }
        font_size = sizes.get(size, "13px")
        weight = "bold" if heading else "normal"
        color = HyprlandStyles.TEXT_PRIMARY if heading else HyprlandStyles.TEXT_SECONDARY
        
        return f"""
            QLabel {{
                color: {color};
                font-size: {font_size};
                font-weight: {weight};
                font-family: {HyprlandStyles.FONT_FAMILY};
                background: transparent;
            }}
        """
    
    @staticmethod
    def get_card_style():
        return f"""
            QFrame[card="true"] {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 8px;
                padding: 0px;
            }}
            QGroupBox {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 8px;
                padding: 20px;
                margin-top: 10px;
                font-weight: bold;
                color: {HyprlandStyles.TEXT_PRIMARY};
                font-family: {HyprlandStyles.FONT_FAMILY};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: {HyprlandStyles.TEXT_PRIMARY};
                font-weight: bold;
                background-color: {HyprlandStyles.BACKGROUND_CARD};
            }}
        """
    
    @staticmethod
    def get_table_style():
        return f"""
            QTableWidget {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 8px;
                gridline-color: {HyprlandStyles.BORDER_COLOR};
                font-size: 12px;
                font-family: {HyprlandStyles.FONT_FAMILY};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {HyprlandStyles.BORDER_COLOR};
                color: {HyprlandStyles.TEXT_SECONDARY};
                background-color: {HyprlandStyles.BACKGROUND_CARD};
            }}
            QTableWidget::item:selected {{
                background-color: {HyprlandStyles.ACCENT_PRIMARY};
                color: {HyprlandStyles.BACKGROUND_PRIMARY};
                border: none;
            }}
            QHeaderView::section {{
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid {HyprlandStyles.BORDER_COLOR};
                font-weight: bold;
                color: {HyprlandStyles.TEXT_PRIMARY};
            }}
            QTableCornerButton::section {{
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                border: none;
                border-bottom: 2px solid {HyprlandStyles.BORDER_COLOR};
                border-right: 1px solid {HyprlandStyles.BORDER_COLOR};
            }}
        """
    
    @staticmethod
    def get_window_style():
        return f"""
            QMainWindow, QWidget {{
                background-color: {HyprlandStyles.BACKGROUND_PRIMARY};
                color: {HyprlandStyles.TEXT_PRIMARY};
                font-family: {HyprlandStyles.FONT_FAMILY};
                border: none;
            }}
        """
    
    @staticmethod
    def get_scroll_area_style():
        return f"""
            QScrollArea {{
                background-color: {HyprlandStyles.BACKGROUND_PRIMARY};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {HyprlandStyles.TEXT_MUTED};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {HyprlandStyles.ACCENT_PRIMARY};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """
    
    @staticmethod
    def get_tab_widget_style():
        return f"""
            QTabWidget::pane {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 4px;
            }}
            QTabWidget::tab-bar {{
                alignment: left;
            }}
            QTabBar::tab {{
                background-color: {HyprlandStyles.BACKGROUND_SECONDARY};
                color: {HyprlandStyles.TEXT_SECONDARY};
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid {HyprlandStyles.BORDER_COLOR};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                color: {HyprlandStyles.TEXT_PRIMARY};
                border-color: {HyprlandStyles.BORDER_COLOR};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {HyprlandStyles.BACKGROUND_CARD};
                color: {HyprlandStyles.ACCENT_PRIMARY};
            }}
        """
