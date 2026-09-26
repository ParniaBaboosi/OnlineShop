# services/payment_service.py
import random
import datetime

class PaymentService:
    def __init__(self, db):
        self.db = db
    
    def create(self, order_id, amount, method, status):
        transaction_id = f"TXN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        tracking_code = f"TRK-{order_id}-{random.randint(10000, 99999)}"
        approved_date = datetime.date.today() if status == 'success' else None
        note = f"Order #{order_id} - {method}"
        
        query = """
            INSERT INTO Payment (
                Order_ID, Payment_Date, Amount, Payment_Method, Payment_Status,
                Transaction_ID, Tracking_Code, Approved_Date, Payment_Note
            )
            VALUES (?, GETDATE(), ?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_command(query, (
            order_id, amount, method, status,
            transaction_id, tracking_code, approved_date, note
        ))
    
    def get_payment_methods(self):
        return [
            {'id': 'credit_card', 'name': 'Credit Card'},
            {'id': 'debit_card', 'name': 'Debit Card'},
            {'id': 'cash_on_delivery', 'name': 'Cash on Delivery'},
            {'id': 'online_payment', 'name': 'Digital Wallet'},
            {'id': 'crypto', 'name': 'Crypto Currency'}
        ]