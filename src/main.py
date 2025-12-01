import sys
import os
from PyQt6.QtWidgets import QApplication, QStackedWidget

from views.login_window import LoginWindow
from views.main_window import MainWindow
from models.auth import AuthModel
from models.budget import BudgetModel
from controllers.budget_controller import BudgetController
from views.styles.styles import HyprlandStyles

class BudgetManagerApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        HyprlandStyles.setup_app_style(self.app)
        
        # Set application properties for Linux desktop
        self.app.setApplicationName("Budget Manager")
        self.app.setApplicationVersion("1.0.0")
        self.app.setDesktopFileName("budget-manager")
        
        # Initialize models and controller
        self.auth_model = AuthModel()
        self.budget_model = BudgetModel()
        self.controller = BudgetController(self.budget_model)
        
        # Create stacked widget for login/main window
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setWindowTitle("Budget Manager")
        
        # Create windows
        self.login_window = LoginWindow(self.auth_model)
        self.main_window = MainWindow(self.controller)
        
        # Add to stacked widget
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.main_window)
        
        # Connect signals
        self.login_window.login_successful.connect(self.show_main_window)
        
    def show_main_window(self):
        self.stacked_widget.setCurrentIndex(1)
        self.stacked_widget.setGeometry(100, 100, 1300, 800)
        self.stacked_widget.show()
        
    def run(self):
        self.stacked_widget.show()
        return self.app.exec()

if __name__ == "__main__":
    app = BudgetManagerApp()
    sys.exit(app.run())
