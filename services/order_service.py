# services/order_service.py
import random
import datetime

class OrderService:
    def __init__(self, db):
        self.db = db
    
    def create(self, user_id, address_id, items):
        try:
            order_query = """
                INSERT INTO [Order] (User_ID, Address_ID, Order_Date, Total_Amount)
                VALUES (?, ?, GETDATE(), 0)
            """
            self.db.execute_command(order_query, (user_id, address_id))
            
            order_id_query = "SELECT MAX(Order_ID) FROM [Order]"
            result = self.db.execute_query(order_id_query)
            order_id = result[0][0] if result else None
            
            if not order_id:
                return None, "Failed to create order!"
            
            total = 0
            for item in items:
                price_query = "SELECT Price, Stock_Quantity FROM Product WHERE Product_ID = ?"
                price_result = self.db.execute_query(price_query, (item['product_id'],))
                if not price_result:
                    continue
                
                price = price_result[0][0]
                stock = price_result[0][1]
                
                if stock < item['quantity']:
                    continue
                
                item_query = """
                    INSERT INTO Order_Item (Order_ID, Product_ID, Quantity, Price)
                    VALUES (?, ?, ?, ?)
                """
                self.db.execute_command(item_query, (order_id, item['product_id'], item['quantity'], price))
                total += price * item['quantity']
                
                update_stock = "UPDATE Product SET Stock_Quantity = Stock_Quantity - ? WHERE Product_ID = ?"
                self.db.execute_command(update_stock, (item['quantity'], item['product_id']))
            
            update_total = "UPDATE [Order] SET Total_Amount = ? WHERE Order_ID = ?"
            self.db.execute_command(update_total, (total, order_id))
            
            return order_id, total
            
        except Exception as e:
            return None, str(e)
    
    def get_user_orders(self, user_id):
        query = """
            SELECT o.Order_ID, o.Order_Date, o.Total_Amount, 
                   COUNT(oi.Order_Item_ID) AS Item_Count,
                   p.Payment_Method, p.Payment_Status, p.Transaction_ID,
                   p.Tracking_Code, p.Approved_Date, p.Amount
            FROM [Order] o
            LEFT JOIN Order_Item oi ON o.Order_ID = oi.Order_ID
            LEFT JOIN Payment p ON o.Order_ID = p.Order_ID
            WHERE o.User_ID = ?
            GROUP BY o.Order_ID, o.Order_Date, o.Total_Amount,
                     p.Payment_Method, p.Payment_Status, p.Transaction_ID,
                     p.Tracking_Code, p.Approved_Date, p.Amount
            ORDER BY o.Order_Date DESC
        """
        return self.db.execute_query(query, (user_id,))
    
    def get_order_details(self, order_id):
        query = """
            SELECT p.Product_Name, oi.Quantity, oi.Price
            FROM Order_Item oi
            INNER JOIN Product p ON oi.Product_ID = p.Product_ID
            WHERE oi.Order_ID = ?
        """
        return self.db.execute_query(query, (order_id,))
    
    def get_addresses(self, user_id):
        query = "SELECT Address_ID, City, Street FROM Address WHERE User_ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def add_address(self, user_id, state, city, street, postal_code):
        query = """
            INSERT INTO Address (User_ID, State, City, Street, Postal_Code)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_command(query, (user_id, state, city, street, postal_code))
    
    def get_available_products(self):
        query = """
            SELECT Product_ID, Product_Name, Price, Stock_Quantity, 
                   Colors, Size, Brand
            FROM Product
            WHERE Stock_Quantity > 0
        """
        return self.db.execute_query(query)