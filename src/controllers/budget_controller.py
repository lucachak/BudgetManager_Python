from models.budget import BudgetModel, Transaction
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class BudgetController:
    def __init__(self, model: BudgetModel):
        self.model = model
        self.monthly_income = 0
    
    def add_income(self, amount: float, category: str, description: str):
        transaction = Transaction(
            id=str(uuid.uuid4()),
            amount=amount,
            category=category,
            description=description,
            date=datetime.now().isoformat(),
            type='income'
        )
        self.model.add_transaction(transaction)
    
    def add_expense(self, amount: float, category: str, description: str):
        transaction = Transaction(
            id=str(uuid.uuid4()),
            amount=amount,
            category=category,
            description=description,
            date=datetime.now().isoformat(),
            type='expense'
        )
        self.model.add_transaction(transaction)
    
    def delete_transaction(self, transaction_id: str):
        self.model.delete_transaction(transaction_id)
    
    def get_current_balance(self) -> float:
        return self.model.get_balance()
    
    def get_category_summary(self) -> Dict:
        summary = {}
        for transaction in self.model.transactions:
            if transaction.category not in summary:
                summary[transaction.category] = {'income': 0, 'expense': 0}
            if transaction.type == 'income':
                summary[transaction.category]['income'] += transaction.amount
            else:
                summary[transaction.category]['expense'] += transaction.amount
        return summary
    
    def get_recent_transactions(self, limit: int = 10):
        return self.model.get_recent_transactions(limit)
    
    def get_balance_history(self) -> List[Tuple[str, float]]:
        """Get balance history for charting"""
        transactions = sorted(self.model.transactions, key=lambda x: x.date)
        balance_history = []
        running_balance = 0
        
        for transaction in transactions:
            if transaction.type == 'income':
                running_balance += transaction.amount
            else:
                running_balance -= transaction.amount
            
            date_str = transaction.date.split('T')[0]
            balance_history.append((date_str, running_balance))
        
        return balance_history
    
    def get_monthly_summary(self) -> Dict:
        """Get monthly income/expense summary"""
        monthly_data = {}
        
        for transaction in self.model.transactions:
            # Extract year-month from date
            date_obj = datetime.fromisoformat(transaction.date.replace('Z', '+00:00'))
            month_key = date_obj.strftime("%Y-%m")
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {'income': 0, 'expense': 0}
            
            if transaction.type == 'income':
                monthly_data[month_key]['income'] += transaction.amount
            else:
                monthly_data[month_key]['expense'] += transaction.amount
        
        return monthly_data

    def set_monthly_income(self, amount:float) ->None:
        if amount > 0:
            self.monthly_income = amount
        else:
            raise ValueError("Must be a valid income")


    def get_monthly_income(self) -> float:
        if self.monthly_income > 0 or self.monthly_income is not None: 
            return self.monthly_income
        else:
            return 0.0 

