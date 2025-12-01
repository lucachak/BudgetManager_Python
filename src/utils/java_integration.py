import json
import requests
from models.budget import BudgetModel

class JavaIntegration:
    def __init__(self, base_url: str = "http://localhost:8080/api"):
        self.base_url = base_url
    
    def export_to_java(self, model: BudgetModel):
        """Export budget data to Java application"""
        data = {
            'transactions': [
                {
                    'id': t.id,
                    'amount': t.amount,
                    'category': t.category,
                    'description': t.description,
                    'date': t.date,
                    'type': t.type
                } for t in model.transactions
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/budget/import",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def import_from_java(self, model: BudgetModel):
        """Import budget data from Java application"""
        try:
            response = requests.get(f"{self.base_url}/budget/export")
            if response.status_code == 200:
                data = response.json()
                # Merge with existing data
                for transaction_data in data.get('transactions', []):
                    # Avoid duplicates based on ID
                    if not any(t.id == transaction_data['id'] for t in model.transactions):
                        model.transactions.append(transaction_data)
                model.save_data()
                return True
        except Exception as e:
            print(f"Import failed: {e}")
        return False
