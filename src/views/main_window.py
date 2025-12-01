from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QComboBox, 
                            QTableWidget, QTableWidgetItem, QTabWidget,
                            QMessageBox, QHeaderView, QFormLayout, QGroupBox,
                            QFrame, QScrollArea, QSizePolicy, QSpacerItem,
                            QSplitter)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QDate
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QFont
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QLineSeries, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import QDateTime

from controllers.budget_controller import BudgetController
from views.styles.styles import HyprlandStyles

from views.empty_window import EmptyWindow

class MainWindow(QMainWindow):
    def __init__(self, controller: BudgetController):
        super().__init__()
        self.controller = controller
        self.setup_ui()
        self.apply_styles()
        self.refresh_data()
        
        # Auto-refresh every 10 seconds
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(10000)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left sidebar - Quick stats
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Main content area
        content_frame = QFrame()
        content_frame.setProperty("card", "true")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with balance
        header_frame = self.create_header()
        content_layout.addWidget(header_frame)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        content_layout.addWidget(self.tabs)
        
        # Transaction Tab
        transaction_tab = QWidget()
        transaction_layout = QVBoxLayout(transaction_tab)
        transaction_layout.addWidget(self.create_transaction_form())
        transaction_layout.addWidget(self.create_transactions_table())
        self.tabs.addTab(transaction_tab, "Transactions")
        
        # Analytics Tab
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout(analytics_tab)
        analytics_layout.addWidget(self.create_analytics_widget())
        self.tabs.addTab(analytics_tab, "Analytics")
        
        # Empty View Tab
        empty_view_tab = self.create_empty_view()
        self.tabs.addTab(empty_view_tab, "Empty View")
        
        main_layout.addWidget(content_frame, 1)
    
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setProperty("card", "true")
        sidebar.setFixedWidth(280)
        sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Quick stats title
        stats_title = QLabel("Quick Stats")
        stats_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(stats_title)
        
        # Stats cards
        layout.addWidget(self.create_stat_card(
            "Total Balance", self.controller.get_current_balance(), HyprlandStyles.ACCENT_PRIMARY))
        layout.addWidget(self.create_stat_card(
            "Monthly Income", self.controller.get_monthly_income(), HyprlandStyles.ACCENT_SUCCESS))
        layout.addWidget(self.create_stat_card(
            "Monthly Expense", "0.00", HyprlandStyles.ACCENT_ERROR))
        layout.addWidget(self.create_stat_card(
            "Transactions", "0", HyprlandStyles.ACCENT_SECONDARY))
        
        layout.addStretch()
        
        # Quick actions
        actions_title = QLabel("Quick Actions")
        actions_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(actions_title)
        
        quick_income_btn = QPushButton("+ Quick Income")
        quick_income_btn.setStyleSheet(HyprlandStyles.get_button_style(size="small"))
        quick_income_btn.clicked.connect(self.quick_income)
        
        quick_expense_btn = QPushButton("- Quick Expense")
        quick_expense_btn.setStyleSheet(HyprlandStyles.get_button_style(primary=False, size="small"))
        quick_expense_btn.clicked.connect(self.quick_expense)
        
        layout.addWidget(quick_income_btn)
        layout.addWidget(quick_expense_btn)
        
        layout.addStretch()
        
        # Navigation section
        nav_title = QLabel("Navigation")
        nav_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(nav_title)
        
        empty_view_btn = QPushButton("Empty View")
        empty_view_btn.setStyleSheet(HyprlandStyles.get_button_style(size="medium"))
        empty_view_btn.clicked.connect(self.show_empty_view)
        layout.addWidget(empty_view_btn)
        
        return sidebar
    
    def create_stat_card(self, title: str, value: str, color: str):
        card = QFrame()
        card.setProperty("card", "true")
        card.setFixedHeight(80)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        
        value_label = QLabel(f"${value}")
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: bold;
                font-family: {HyprlandStyles.FONT_FAMILY};
            }}
        """)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
    
    def create_header(self):
        header = QFrame()
        header.setProperty("card", "true")
        header.setFixedHeight(100)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Balance info
        balance_info = QVBoxLayout()
        
        balance_title = QLabel("Current Balance")
        balance_title.setStyleSheet(HyprlandStyles.get_label_style(size="medium"))
        
        self.balance_label = QLabel("$0.00")
        self.balance_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                font-family: {HyprlandStyles.FONT_FAMILY};
            }}
        """)
        
        balance_info.addWidget(balance_title)
        balance_info.addWidget(self.balance_label)
        
        layout.addLayout(balance_info)
        layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(HyprlandStyles.get_button_style(size="medium"))
        refresh_btn.clicked.connect(self.refresh_data)
        
        layout.addWidget(refresh_btn)
        
        return header
    
    def create_transaction_form(self):
        group = QGroupBox("Add New Transaction")
        layout = QFormLayout(group)
        layout.setVerticalSpacing(12)
        layout.setHorizontalSpacing(20)
        
        # First row
        row1_layout = QHBoxLayout()
        
        type_layout = QVBoxLayout()
        type_label = QLabel("Type")
        type_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Income", "Expense"])
        self.type_combo.currentTextChanged.connect(self.update_categories)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        
        category_layout = QVBoxLayout()
        category_label = QLabel("Category")
        category_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        self.category_combo = QComboBox()
        self.update_categories()
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        
        amount_layout = QVBoxLayout()
        amount_label = QLabel("Amount")
        amount_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        
        row1_layout.addLayout(type_layout)
        row1_layout.addLayout(category_layout)
        row1_layout.addLayout(amount_layout)
        row1_layout.addStretch()
        
        # Second row
        row2_layout = QHBoxLayout()
        
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Description")
        desc_label.setStyleSheet(HyprlandStyles.get_label_style(size="small"))
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Transaction description")
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.description_input)
        
        button_layout = QVBoxLayout()
        button_layout.addStretch()
        add_button = QPushButton("Add Transaction")
        add_button.setStyleSheet(HyprlandStyles.get_button_style(size="medium"))
        add_button.clicked.connect(self.add_transaction)
        
        button_layout.addWidget(add_button)
        
        row2_layout.addLayout(desc_layout, 1)
        row2_layout.addLayout(button_layout)
        
        layout.addRow(row1_layout)
        layout.addRow(row2_layout)
        
        return group
    
    def create_transactions_table(self):
        frame = QFrame()
        frame.setProperty("card", "true")
        layout = QVBoxLayout(frame)
        
        table_title = QLabel("Recent Transactions")
        table_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(table_title)
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(6)
        self.transactions_table.setHorizontalHeaderLabels([
            "Date", "Type", "Category", "Description", "Amount", "Actions"
        ])
        header = self.transactions_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.transactions_table.setColumnWidth(5, 100)
        
        layout.addWidget(self.transactions_table)
        return frame
    
    def create_analytics_widget(self):
        frame = QFrame()
        frame.setProperty("card", "true")
        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        
        # Charts section
        charts_title = QLabel("Financial Analytics")
        charts_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="xl"))
        layout.addWidget(charts_title)
        
        # Create splitter for charts
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Income vs Expense chart
        income_expense_chart = self.create_income_expense_chart()
        splitter.addWidget(income_expense_chart)
        
        # Balance over time chart
        balance_chart = self.create_balance_chart()
        splitter.addWidget(balance_chart)
        
        # Set splitter proportions
        splitter.setSizes([400, 400])
        layout.addWidget(splitter)
        
        # Category summary table
        summary_title = QLabel("Category Summary")
        summary_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(summary_title)
        
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(3)
        self.summary_table.setHorizontalHeaderLabels(["Category", "Income", "Expense"])
        header = self.summary_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.summary_table)
        
        return frame
    
    def create_income_expense_chart(self):
        """Create bar chart showing income vs expenses by category"""
        chart_frame = QFrame()
        chart_frame.setProperty("card", "true")
        layout = QVBoxLayout(chart_frame)
        
        chart_title = QLabel("Income vs Expenses by Category")
        chart_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(chart_title)
        
        # Create chart
        self.income_expense_chart = QChart()
        self.income_expense_chart.setBackgroundBrush(QColor(HyprlandStyles.BACKGROUND_CARD))
        self.income_expense_chart.setTitleBrush(QColor(HyprlandStyles.TEXT_PRIMARY))
        self.income_expense_chart.setTitle("Income vs Expenses")
        
        # Create chart view
        self.income_expense_chart_view = QChartView(self.income_expense_chart)
        self.income_expense_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.income_expense_chart_view.setMinimumHeight(400)
        
        layout.addWidget(self.income_expense_chart_view)
        
        return chart_frame
    
    def create_balance_chart(self):
        """Create line chart showing balance over time"""
        chart_frame = QFrame()
        chart_frame.setProperty("card", "true")
        layout = QVBoxLayout(chart_frame)
        
        chart_title = QLabel("Balance Over Time")
        chart_title.setStyleSheet(HyprlandStyles.get_label_style(heading=True, size="large"))
        layout.addWidget(chart_title)
        
        # Create chart
        self.balance_chart = QChart()
        self.balance_chart.setBackgroundBrush(QColor(HyprlandStyles.BACKGROUND_CARD))
        self.balance_chart.setTitleBrush(QColor(HyprlandStyles.TEXT_PRIMARY))
        self.balance_chart.setTitle("Balance Trend")
        
        # Create chart view
        self.balance_chart_view = QChartView(self.balance_chart)
        self.balance_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.balance_chart_view.setMinimumHeight(400)
        
        layout.addWidget(self.balance_chart_view)
        
        return chart_frame
    
    def create_empty_view(self):
        """Create an empty view widget"""
        empty_window = EmptyWindow()
        return empty_window
    
    def show_empty_view(self):
        """Switch to the empty view tab"""
        # Find the index of the empty view tab
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "Empty View":
                self.tabs.setCurrentIndex(i)
                break
    
    def update_charts(self):
        """Update both charts with current data"""
        self.update_income_expense_chart()
        self.update_balance_chart()
    
    def update_income_expense_chart(self):
        """Update income vs expense bar chart"""
        # Clear existing series and axes
        self.income_expense_chart.removeAllSeries()
        axes = list(self.income_expense_chart.axes())
        for axis in axes:
            self.income_expense_chart.removeAxis(axis)
        
        summary = self.controller.get_category_summary()
        
        if not summary:
            # Show empty state
            return
        
        # Create bar sets
        income_set = QBarSet("Income")
        income_set.setColor(QColor(HyprlandStyles.ACCENT_SUCCESS))
        
        expense_set = QBarSet("Expenses")
        expense_set.setColor(QColor(HyprlandStyles.ACCENT_ERROR))
        
        categories = []
        
        for category, amounts in summary.items():
            categories.append(category)
            income_set.append(amounts['income'])
            expense_set.append(amounts['expense'])
        
        # Create series
        series = QBarSeries()
        series.append(income_set)
        series.append(expense_set)
        
        # Add series to chart
        self.income_expense_chart.addSeries(series)
        
        # Create axis
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor(HyprlandStyles.TEXT_PRIMARY))
        
        axis_y = QValueAxis()
        axis_y.setLabelsColor(QColor(HyprlandStyles.TEXT_PRIMARY))
        axis_y.setTitleText("Amount ($)")
        axis_y.setTitleBrush(QColor(HyprlandStyles.TEXT_PRIMARY))
        
        # Qt6 way: Add axes to chart first, then attach to series
        self.income_expense_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.income_expense_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        
        # Style the chart
        self.income_expense_chart.legend().setVisible(True)
        self.income_expense_chart.legend().setLabelColor(QColor(HyprlandStyles.TEXT_PRIMARY))
        self.income_expense_chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
    
    def update_balance_chart(self):
        """Update balance over time line chart"""
        # Clear existing series and axes
        self.balance_chart.removeAllSeries()
        axes = list(self.balance_chart.axes())
        for axis in axes:
            self.balance_chart.removeAxis(axis)
        
        transactions = self.controller.model.transactions
        
        if not transactions:
            return
        
        # Sort transactions by date
        sorted_transactions = sorted(transactions, key=lambda x: x.date)
        
        # Create line series for balance
        balance_series = QLineSeries()
        balance_series.setName("Balance")
        balance_series.setColor(QColor(HyprlandStyles.ACCENT_PRIMARY))
        
        # Calculate running balance
        running_balance = 0
        dates = []
        balances = []
        
        for transaction in sorted_transactions:
            if transaction.type == 'income':
                running_balance += transaction.amount
            else:
                running_balance -= transaction.amount
            
            # Use simplified date for demonstration
            date_str = transaction.date.split('T')[0]
            dates.append(date_str)
            balances.append(running_balance)
        
        # Add points to series (limit to last 30 points for readability)
        max_points = min(30, len(dates))
        recent_dates = dates[-max_points:]
        recent_balances = balances[-max_points:]
        
        for i, (date_str, balance) in enumerate(zip(recent_dates, recent_balances)):
            balance_series.append(i, balance)
        
        # Add series to chart
        self.balance_chart.addSeries(balance_series)
        
        # Create axis - use value axis for X since bar category axis has issues with line series
        axis_x = QValueAxis()
        axis_x.setTitleText("Transaction Sequence")
        axis_x.setTitleBrush(QColor(HyprlandStyles.TEXT_PRIMARY))
        axis_x.setLabelsColor(QColor(HyprlandStyles.TEXT_PRIMARY))
        axis_x.setRange(0, max(1, len(recent_dates) - 1))
        axis_x.setTickCount(min(6, len(recent_dates)))
        
        axis_y = QValueAxis()
        axis_y.setLabelsColor(QColor(HyprlandStyles.TEXT_PRIMARY))
        axis_y.setTitleText("Balance ($)")
        axis_y.setTitleBrush(QColor(HyprlandStyles.TEXT_PRIMARY))
        
        # Set axes to chart - Qt6 way
        self.balance_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.balance_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        
        # Attach series to axes
        balance_series.attachAxis(axis_x)
        balance_series.attachAxis(axis_y)
        
        # Style the chart
        self.balance_chart.legend().setVisible(True)
        self.balance_chart.legend().setLabelColor(QColor(HyprlandStyles.TEXT_PRIMARY))
        self.balance_chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)  
    def apply_styles(self):
        self.setStyleSheet(HyprlandStyles.get_window_style())
        
        # Apply styles to all components
        if hasattr(self, 'amount_input'):
            self.amount_input.setStyleSheet(HyprlandStyles.get_input_style())
        if hasattr(self, 'description_input'):
            self.description_input.setStyleSheet(HyprlandStyles.get_input_style())
        if hasattr(self, 'type_combo'):
            self.type_combo.setStyleSheet(HyprlandStyles.get_input_style())
        if hasattr(self, 'category_combo'):
            self.category_combo.setStyleSheet(HyprlandStyles.get_input_style())
        
        # Style tables
        if hasattr(self, 'transactions_table'):
            self.transactions_table.setStyleSheet(HyprlandStyles.get_table_style())
        if hasattr(self, 'summary_table'):
            self.summary_table.setStyleSheet(HyprlandStyles.get_table_style())
    
    def update_categories(self):
        self.category_combo.clear()
        transaction_type = self.type_combo.currentText().lower()
        categories = self.controller.model.categories.get(transaction_type, [])
        self.category_combo.addItems(categories)
    
    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_combo.currentText()
            description = self.description_input.text()
            transaction_type = self.type_combo.currentText().lower()
            
            if transaction_type == 'income':
                self.controller.add_income(amount, category, description)
            else:
                self.controller.add_expense(amount, category, description)
            
            self.refresh_data()
            self.clear_form()
            
        except ValueError:
            self.show_error("Please enter a valid amount!")
    
    def clear_form(self):
        self.amount_input.clear()
        self.description_input.clear()
    
    def refresh_data(self):
        # Update balance
        balance = self.controller.get_current_balance()
        balance_color = HyprlandStyles.ACCENT_SUCCESS if balance >= 0 else HyprlandStyles.ACCENT_ERROR
        self.balance_label.setText(f"${balance:,.2f}")
        self.balance_label.setStyleSheet(f"""
            QLabel {{
                color: {balance_color};
                font-size: 28px;
                font-weight: bold;
                font-family: {HyprlandStyles.FONT_FAMILY};
            }}
        """)
        
        # Update transactions table
        transactions = self.controller.get_recent_transactions(20)
        self.transactions_table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            date = transaction.date.split('T')[0]
            self.transactions_table.setItem(row, 0, QTableWidgetItem(date))
            self.transactions_table.setItem(row, 1, QTableWidgetItem(transaction.type.title()))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(transaction.category))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(transaction.description))
            
            amount_item = QTableWidgetItem(f"${transaction.amount:,.2f}")
            if transaction.type == 'income':
                amount_item.setForeground(QColor(HyprlandStyles.ACCENT_SUCCESS))
            else:
                amount_item.setForeground(QColor(HyprlandStyles.ACCENT_ERROR))
            self.transactions_table.setItem(row, 4, amount_item)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet(HyprlandStyles.get_button_style(primary=False, size="small"))
            delete_btn.clicked.connect(lambda checked, tid=transaction.id: self.delete_transaction(tid))
            self.transactions_table.setCellWidget(row, 5, delete_btn)
        
        # Update summary table
        summary = self.controller.get_category_summary()
        self.summary_table.setRowCount(len(summary))
        
        for row, (category, amounts) in enumerate(summary.items()):
            self.summary_table.setItem(row, 0, QTableWidgetItem(category))
            
            income_item = QTableWidgetItem(f"${amounts['income']:,.2f}")
            income_item.setForeground(QColor(HyprlandStyles.ACCENT_SUCCESS))
            self.summary_table.setItem(row, 1, income_item)
            
            expense_item = QTableWidgetItem(f"${amounts['expense']:,.2f}")
            expense_item.setForeground(QColor(HyprlandStyles.ACCENT_ERROR))
            self.summary_table.setItem(row, 2, expense_item)
        
        # Update charts
        self.update_charts()
    
    def delete_transaction(self, transaction_id: str):
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this transaction?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_transaction(transaction_id)
            self.refresh_data()
    
    def quick_income(self):
        self.type_combo.setCurrentText("Income")
        self.amount_input.setFocus()
    
    def quick_expense(self):
        self.type_combo.setCurrentText("Expense")
        self.amount_input.setFocus()
    
    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec()

    def paintEvent(self, event):
        # Custom paint for modern look
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(HyprlandStyles.BACKGROUND_PRIMARY))
        gradient.setColorAt(1, QColor(HyprlandStyles.BACKGROUND_SECONDARY))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

