from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import json
import os

@dataclass
class Transaction:
    id: str
    amount: float
    category: str
    description: str
    date: str
    type: str  # 'income' or 'expense'

class BudgetModel:
    def __init__(self, data_file="data/budget_data.json"):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.categories = {
            'income': ['Salary', 'Freelance', 'Investment', 'Other'],
            'expense': ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Healthcare']
        }
        self.load_data()
    
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.save_data()
    
    def delete_transaction(self, transaction_id: str):
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        self.save_data()
    
    def get_balance(self) -> float:
        income = sum(t.amount for t in self.transactions if t.type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.type == 'expense')
        return income - expenses
    
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        return [t for t in self.transactions if t.category == category]
    
    def get_recent_transactions(self, limit: int = 10) -> List[Transaction]:
        return sorted(self.transactions, key=lambda x: x.date, reverse=True)[:limit]
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = [
                        Transaction(**t) for t in data.get('transactions', [])
                    ]
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            data = {
                'transactions': [
                    {
                        'id': t.id,
                        'amount': t.amount,
                        'category': t.category,
                        'description': t.description,
                        'date': t.date,
                        'type': t.type
                    } for t in self.transactions
                ]
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
