# main.py
import os
from database import Database

class OnlineShopApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_main_menu(self):
        self.clear_screen()
        print("=" * 50)
        print("🛍️  ONLINE SHOP")
        print("=" * 50)
        if self.current_user:
            print(f"👤 User: {self.current_user[1]} ({self.current_user[2]})")
            print("-" * 50)
            print("1. 📦 View Products")
            print("2. 🛒 New Order")
            print("3. 📋 My Orders")
            print("4. 🔍 Search Product")
            print("5. 🚪 Logout")
        else:
            print("1. 📝 Register")
            print("2. 🔑 Login")
        print("0. ❌ Exit")
        print("=" * 50)
    
    def register(self):
        self.clear_screen()
        print("=" * 50)
        print("📝 REGISTRATION FORM")
        print("=" * 50)
        
        name = input("Full Name: ")
        email = input("Email: ")
        password = input("Password: ")
        
        print("\nUser Type:")
        print("1. Customer")
        print("2. Seller")
        user_type_choice = input("Choose (1 or 2): ")
        user_type = 'customer' if user_type_choice == '1' else 'seller'
        
        check_query = "SELECT COUNT(*) FROM [User] WHERE Email = ?"
        result = self.db.execute_query(check_query, (email,))
        if result and result[0][0] > 0:
            print("\n❌ This email is already registered!")
            input("\nPress Enter...")
            return
        
        query = """
            INSERT INTO [User] (Name, Email, Password, User_Type, Created_At)
            VALUES (?, ?, ?, ?, GETDATE())
        """
        if self.db.execute_command(query, (name, email, password, user_type)):
            print("\n✅ Registration successful!")
            print("🔑 You can now login.")
        else:
            print("\n❌ Registration failed!")
        
        input("\nPress Enter...")
    
    def login(self):
        self.clear_screen()
        print("=" * 50)
        print("🔑 LOGIN FORM")
        print("=" * 50)
        
        email = input("Email: ")
        password = input("Password: ")
        
        query = "SELECT User_ID, Name, User_Type FROM [User] WHERE Email = ? AND Password = ?"
        result = self.db.execute_query(query, (email, password))
        
        if result:
            self.current_user = result[0]
            print(f"\n✅ Welcome {self.current_user[1]}!")
        else:
            print("\n❌ Invalid email or password!")
        
        input("\nPress Enter...")
    
    def show_products(self):
        self.clear_screen()
        print("=" * 50)
        print("📦 PRODUCT LIST")
        print("=" * 50)
        
        query = """
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, 
                   p.Price, p.Stock_Quantity, u.Name AS Seller
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            INNER JOIN [User] u ON p.Seller_ID = u.User_ID
        """
        products = self.db.execute_query(query)
        
        if products:
            print("-" * 80)
            print(f"{'ID':<4} {'Product Name':<25} {'Category':<12} {'Price':<10} {'Stock':<8} {'Seller':<15}")
            print("-" * 80)
            for p in products:
                print(f"{p[0]:<4} {p[1][:24]:<25} {p[2][:11]:<12} ${p[3]:<10} {p[4]:<8} {p[5][:14]:<15}")
        else:
            print("❌ No products found!")
        
        input("\nPress Enter...")
    
    def add_address(self):
        print("\n📌 ADD NEW ADDRESS")
        state = input("State: ")
        city = input("City: ")
        street = input("Street: ")
        postal_code = input("Postal Code: ")
        
        query = """
            INSERT INTO Address (User_ID, State, City, Street, Postal_Code)
            VALUES (?, ?, ?, ?, ?)
        """
        if self.db.execute_command(query, (self.current_user[0], state, city, street, postal_code)):
            print("✅ Address added successfully!")
            return True
        else:
            print("❌ Failed to add address!")
            return False
    
    def create_order(self):
        self.clear_screen()
        print("=" * 50)
        print("🛒 NEW ORDER")
        print("=" * 50)
        
        # Show products
        query = """
            SELECT Product_ID, Product_Name, Price, Stock_Quantity 
            FROM Product
            WHERE Stock_Quantity > 0
        """
        products = self.db.execute_query(query)
        
        if not products:
            print("❌ No products available for purchase!")
            input("\nPress Enter...")
            return
        
        print("\nAvailable Products:")
        print("-" * 50)
        for p in products:
            print(f"{p[0]}. {p[1]} - ${p[2]} (Stock: {p[3]})")
        print("-" * 50)
        
        # Get user's address
        address_query = "SELECT Address_ID, City, Street FROM Address WHERE User_ID = ?"
        addresses = self.db.execute_query(address_query, (self.current_user[0],))
        
        if not addresses:
            print("\n⚠️ You have no address registered!")
            add_addr = input("Would you like to add an address? (y/n): ")
            if add_addr.lower() == 'y':
                if not self.add_address():
                    input("\nPress Enter...")
                    return
                addresses = self.db.execute_query(address_query, (self.current_user[0],))
                if not addresses:
                    print("❌ Failed to add address!")
                    input("\nPress Enter...")
                    return
            else:
                print("❌ You need an address to place an order!")
                input("\nPress Enter...")
                return
        
        print("\n📌 Your Addresses:")
        for a in addresses:
            print(f"{a[0]}. {a[1]} - {a[2]}")
        
        try:
            address_id = int(input("\nSelect Address ID: "))
            valid = False
            for a in addresses:
                if a[0] == address_id:
                    valid = True
                    break
            if not valid:
                print("❌ Invalid Address ID!")
                input("\nPress Enter...")
                return
        except ValueError:
            print("❌ Invalid input!")
            input("\nPress Enter...")
            return
        
        # Select products
        items = []
        while True:
            try:
                product_id = int(input("Product ID (0 to finish): "))
                if product_id == 0:
                    break
                quantity = int(input("Quantity: "))
                items.append((product_id, quantity))
            except ValueError:
                print("❌ Invalid input!")
        
        if not items:
            print("❌ Order cancelled.")
            input("\nPress Enter...")
            return
        
        # Create order
        try:
            # 1. Insert order
            order_query = """
                INSERT INTO [Order] (User_ID, Address_ID, Order_Date, Total_Amount)
                VALUES (?, ?, GETDATE(), 0)
            """
            self.db.execute_command(order_query, (self.current_user[0], address_id))
            
            # 2. Get Order ID - استفاده از MAX به جای SCOPE_IDENTITY
            order_id_query = "SELECT MAX(Order_ID) FROM [Order]"
            result = self.db.execute_query(order_id_query)
            
            if result and result[0][0]:
                order_id = result[0][0]
            else:
                raise Exception("Failed to get Order ID!")
            
            print(f"📝 Order #{order_id} created...")
            
            total = 0
            for product_id, quantity in items:
                price_query = "SELECT Price, Stock_Quantity FROM Product WHERE Product_ID = ?"
                price_result = self.db.execute_query(price_query, (product_id,))
                if not price_result:
                    print(f"⚠️ Product {product_id} not found!")
                    continue
                
                price = price_result[0][0]
                stock = price_result[0][1]
                
                if stock < quantity:
                    print(f"⚠️ Not enough stock for product {product_id}! Available: {stock}")
                    continue
                
                item_query = """
                    INSERT INTO Order_Item (Order_ID, Product_ID, Quantity, Price)
                    VALUES (?, ?, ?, ?)
                """
                self.db.execute_command(item_query, (order_id, product_id, quantity, price))
                total += price * quantity
                
                update_stock = "UPDATE Product SET Stock_Quantity = Stock_Quantity - ? WHERE Product_ID = ?"
                self.db.execute_command(update_stock, (quantity, product_id))
            
            update_total = "UPDATE [Order] SET Total_Amount = ? WHERE Order_ID = ?"
            self.db.execute_command(update_total, (total, order_id))
            
            payment_query = """
                INSERT INTO Payment (Order_ID, Payment_Date, Amount, Payment_Method, Payment_Status)
                VALUES (?, GETDATE(), ?, 'online', 'success')
            """
            self.db.execute_command(payment_query, (order_id, total))
            
            print(f"\n✅ Order #{order_id} created successfully!")
            print(f"💰 Total Amount: ${total}")
            
        except Exception as e:
            print(f"❌ Error creating order: {e}")
        
        input("\nPress Enter...")
    
    def show_my_orders(self):
        self.clear_screen()
        print("=" * 50)
        print("📋 MY ORDERS")
        print("=" * 50)
        
        query = """
            SELECT o.Order_ID, o.Order_Date, o.Total_Amount, 
                   COUNT(oi.Order_Item_ID) AS Item_Count
            FROM [Order] o
            LEFT JOIN Order_Item oi ON o.Order_ID = oi.Order_ID
            WHERE o.User_ID = ?
            GROUP BY o.Order_ID, o.Order_Date, o.Total_Amount
            ORDER BY o.Order_Date DESC
        """
        orders = self.db.execute_query(query, (self.current_user[0],))
        
        if orders:
            for o in orders:
                print(f"\n🆔 Order: {o[0]}")
                print(f"   📅 Date: {o[1]}")
                print(f"   💰 Total: ${o[2]}")
                print(f"   📦 Items: {o[3]}")
                print("-" * 30)
                
                detail_query = """
                    SELECT p.Product_Name, oi.Quantity, oi.Price
                    FROM Order_Item oi
                    INNER JOIN Product p ON oi.Product_ID = p.Product_ID
                    WHERE oi.Order_ID = ?
                """
                details = self.db.execute_query(detail_query, (o[0],))
                if details:
                    print("   Details:")
                    for d in details:
                        print(f"     - {d[0]} (Qty: {d[1]}, Price: ${d[2]})")
        else:
            print("❌ You have no orders!")
        
        input("\nPress Enter...")
    
    def search_product(self):
        self.clear_screen()
        print("=" * 50)
        print("🔍 SEARCH PRODUCT")
        print("=" * 50)
        
        keyword = input("Enter search keyword: ")
        
        query = """
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, 
                   p.Price, p.Stock_Quantity
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            WHERE p.Product_Name LIKE ? OR p.Description LIKE ?
        """
        products = self.db.execute_query(query, (f'%{keyword}%', f'%{keyword}%'))
        
        if products:
            print("\n📦 Search Results:")
            print("-" * 60)
            for p in products:
                print(f"{p[0]}. {p[1]} - {p[2]} - ${p[3]} (Stock: {p[4]})")
        else:
            print("❌ No products found!")
        
        input("\nPress Enter...")
    
    def run(self):
        if not self.db.connect():
            print("❌ Cannot connect to database!")
            return
        
        while True:
            self.display_main_menu()
            choice = input("Your choice: ")
            
            if not self.current_user:
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '0':
                    break
            else:
                if choice == '1':
                    self.show_products()
                elif choice == '2':
                    self.create_order()
                elif choice == '3':
                    self.show_my_orders()
                elif choice == '4':
                    self.search_product()
                elif choice == '5':
                    self.current_user = None
                    print("✅ Logged out successfully!")
                    input("\nPress Enter...")
                elif choice == '0':
                    break
        
        self.db.disconnect()
        print("👋 Goodbye!")

if __name__ == "__main__":
    app = OnlineShopApp()
    app.run()