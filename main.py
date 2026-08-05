# main.py
import os
from database import Database

class OnlineShopApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # ============================================================
    # DISPLAY MENU
    # ============================================================
    def display_main_menu(self):
        self.clear_screen()
        print("=" * 50)
        print("🛍️  ONLINE SHOP")
        print("=" * 50)
        if self.current_user:
            print(f"👤 User: {self.current_user[1]} ({self.current_user[2]})")
            print("-" * 50)
            if self.current_user[2] == 'seller':
                # Seller Menu
                print("1. 📦 View Products")
                print("2. ➕ Add New Product")
                print("3. ✏️ Edit Product")
                print("4. 📦 Update Stock (Quick)")
                print("5. ⚠️ Low Stock Alert")
                print("6. 🗑️ Delete Product")
                print("7. 🔍 Search Product")
                print("8. 🚪 Logout")
            else:
                # Customer Menu
                print("1. 📦 View Products")
                print("2. 🛒 New Order")
                print("3. 📋 My Orders")
                print("4. ⭐ Rate a Product")
                print("5. 📝 View Product Reviews")
                print("6. 🔍 Search Product")
                print("7. 🚪 Logout")
        else:
            print("1. 📝 Register")
            print("2. 🔑 Login")
        print("0. ❌ Exit")
        print("=" * 50)
    
    # ============================================================
    # REGISTER & LOGIN
    # ============================================================
    def register(self):
        """Register new user"""
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
        
        # Check if email already exists
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
        """Login to system"""
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
    
    # ============================================================
    # COMMON FUNCTIONS (For all users)
    # ============================================================
    def show_products(self):
        """Show all products with average rating and review count"""
        self.clear_screen()
        print("=" * 50)
        print("📦 PRODUCT LIST")
        print("=" * 50)
        
        query = """
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, 
                   p.Price, p.Stock_Quantity, u.Name AS Seller,
                   ISNULL(AVG(CAST(r.Rating AS FLOAT)), 0) AS Avg_Rating,
                   COUNT(r.Review_ID) AS Review_Count
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            INNER JOIN [User] u ON p.Seller_ID = u.User_ID
            LEFT JOIN Review r ON p.Product_ID = r.Product_ID
            GROUP BY p.Product_ID, p.Product_Name, c.Category_Name, 
                     p.Price, p.Stock_Quantity, u.Name
        """
        products = self.db.execute_query(query)
        
        if products:
            print("-" * 100)
            print(f"{'ID':<4} {'Product Name':<22} {'Category':<10} {'Price':<8} {'Stock':<6} {'Rating':<7} {'Reviews':<7} {'Seller':<12}")
            print("-" * 100)
            for p in products:
                rating = f"{p[6]:.1f}" if p[6] > 0 else "-"
                print(f"{p[0]:<4} {p[1][:21]:<22} {p[2][:9]:<10} ${p[3]:<8} {p[4]:<6} {rating:<7} {p[7]:<7} {p[5][:11]:<12}")
        else:
            print("❌ No products found!")
        
        input("\nPress Enter...")
    
    def search_product(self):
        """Search products by name or description with ratings"""
        self.clear_screen()
        print("=" * 50)
        print("🔍 SEARCH PRODUCT")
        print("=" * 50)
        
        keyword = input("Enter search keyword: ")
        
        query = """
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, 
                   p.Price, p.Stock_Quantity,
                   ISNULL(AVG(CAST(r.Rating AS FLOAT)), 0) AS Avg_Rating,
                   COUNT(r.Review_ID) AS Review_Count
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            LEFT JOIN Review r ON p.Product_ID = r.Product_ID
            WHERE p.Product_Name LIKE ? OR p.Description LIKE ?
            GROUP BY p.Product_ID, p.Product_Name, c.Category_Name, 
                     p.Price, p.Stock_Quantity
        """
        products = self.db.execute_query(query, (f'%{keyword}%', f'%{keyword}%'))
        
        if products:
            print("\n📦 Search Results:")
            print("-" * 70)
            for p in products:
                rating = f"{p[5]:.1f}" if p[5] > 0 else "-"
                print(f"{p[0]}. {p[1]} - {p[2]} - ${p[3]} (Stock: {p[4]}) ⭐ {rating} ({p[6]} reviews)")
        else:
            print("❌ No products found!")
        
        input("\nPress Enter...")
    
    # ============================================================
    # SELLER FUNCTIONS (Only for sellers)
    # ============================================================
    def add_product(self):
        """Add new product (Seller only)"""
        self.clear_screen()
        print("=" * 50)
        print("➕ ADD NEW PRODUCT")
        print("=" * 50)
        
        name = input("Product Name: ")
        
        # Show categories
        cat_query = "SELECT Category_ID, Category_Name FROM Category"
        categories = self.db.execute_query(cat_query)
        if categories:
            print("\n📂 Categories:")
            for c in categories:
                print(f"  {c[0]}. {c[1]}")
        else:
            print("❌ No categories found!")
            input("\nPress Enter...")
            return
        
        try:
            category_id = int(input("Category ID: "))
            price = float(input("Price: $"))
            stock = int(input("Stock Quantity: "))
            description = input("Description: ")
        except ValueError:
            print("❌ Invalid input!")
            input("\nPress Enter...")
            return
        
        query = """
            INSERT INTO Product (Product_Name, Category_ID, Seller_ID, Price, Stock_Quantity, Created_At, Description)
            VALUES (?, ?, ?, ?, ?, GETDATE(), ?)
        """
        if self.db.execute_command(query, (name, category_id, self.current_user[0], price, stock, description)):
            print("\n✅ Product added successfully!")
        else:
            print("\n❌ Failed to add product!")
        
        input("\nPress Enter...")
    
    def edit_product(self):
        """Edit existing product (Seller only)"""
        self.clear_screen()
        print("=" * 50)
        print("✏️ EDIT PRODUCT")
        print("=" * 50)
        
        # Show only seller's products
        query = """
            SELECT Product_ID, Product_Name, Price, Stock_Quantity 
            FROM Product
            WHERE Seller_ID = ?
        """
        products = self.db.execute_query(query, (self.current_user[0],))
        
        if not products:
            print("❌ You have no products to edit!")
            input("\nPress Enter...")
            return
        
        print("\nYour Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]} (Stock: {p[3]})")
        
        try:
            product_id = int(input("\nSelect Product ID to edit: "))
            
            # Check if product belongs to seller
            check_query = "SELECT * FROM Product WHERE Product_ID = ? AND Seller_ID = ?"
            result = self.db.execute_query(check_query, (product_id, self.current_user[0]))
            if not result:
                print("❌ You don't own this product!")
                input("\nPress Enter...")
                return
            
            current = result[0]
            print(f"\nCurrent: Name={current[1]}, Price=${current[4]}, Stock={current[5]}")
            print("\nLeave blank to keep current value.")
            
            new_name = input(f"New Name (current: {current[1]}): ") or current[1]
            
            new_price_input = input(f"New Price (current: {current[4]}): ")
            new_price = float(new_price_input) if new_price_input else current[4]
            
            new_stock_input = input(f"New Stock (current: {current[5]}): ")
            new_stock = int(new_stock_input) if new_stock_input else current[5]
            
            update_query = "UPDATE Product SET Product_Name = ?, Price = ?, Stock_Quantity = ? WHERE Product_ID = ? AND Seller_ID = ?"
            params = (new_name, new_price, new_stock, product_id, self.current_user[0])
            
            if self.db.execute_command(update_query, params):
                print("\n✅ Product updated successfully!")
            else:
                print("\n❌ Failed to update product!")
                
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        
        input("\nPress Enter...")
    
    def update_stock(self):
        """Update stock quantity only (Seller only)"""
        self.clear_screen()
        print("=" * 50)
        print("📦 UPDATE STOCK")
        print("=" * 50)
        
        # Show seller's products
        query = """
            SELECT Product_ID, Product_Name, Stock_Quantity 
            FROM Product
            WHERE Seller_ID = ?
        """
        products = self.db.execute_query(query, (self.current_user[0],))
        
        if not products:
            print("❌ You have no products!")
            input("\nPress Enter...")
            return
        
        print("\nYour Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - Stock: {p[2]}")
        
        try:
            product_id = int(input("\nSelect Product ID: "))
            new_stock = int(input("New Stock Quantity: "))
            
            if new_stock < 0:
                print("❌ Stock cannot be negative!")
                input("\nPress Enter...")
                return
            
            update_query = "UPDATE Product SET Stock_Quantity = ? WHERE Product_ID = ? AND Seller_ID = ?"
            if self.db.execute_command(update_query, (new_stock, product_id, self.current_user[0])):
                print("\n✅ Stock updated successfully!")
            else:
                print("\n❌ Failed to update stock!")
                
        except ValueError:
            print("❌ Invalid input!")
        
        input("\nPress Enter...")
    
    def show_low_stock(self):
        """Show products with low stock (Seller only)"""
        self.clear_screen()
        print("=" * 50)
        print("⚠️ LOW STOCK ALERT")
        print("=" * 50)
        
        threshold_input = input("Enter stock threshold (default: 10): ")
        try:
            threshold = int(threshold_input) if threshold_input else 10
        except ValueError:
            threshold = 10
        
        query = """
            SELECT Product_ID, Product_Name, Stock_Quantity
            FROM Product
            WHERE Seller_ID = ? AND Stock_Quantity <= ?
            ORDER BY Stock_Quantity ASC
        """
        products = self.db.execute_query(query, (self.current_user[0], threshold))
        
        if products:
            print(f"\n📦 Products with stock <= {threshold}:")
            print("-" * 40)
            for p in products:
                status = "🔴 CRITICAL" if p[2] == 0 else "🟡 LOW"
                print(f"  {p[0]}. {p[1]} - Stock: {p[2]} {status}")
        else:
            print(f"\n✅ All products have stock > {threshold}")
        
        input("\nPress Enter...")
    
    def delete_product(self):
        """Delete product (Seller only)"""
        self.clear_screen()
        print("=" * 50)
        print("🗑️ DELETE PRODUCT")
        print("=" * 50)
        
        # Show only seller's products
        query = """
            SELECT Product_ID, Product_Name, Price, Stock_Quantity 
            FROM Product
            WHERE Seller_ID = ?
        """
        products = self.db.execute_query(query, (self.current_user[0],))
        
        if not products:
            print("❌ You have no products to delete!")
            input("\nPress Enter...")
            return
        
        print("\nYour Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]} (Stock: {p[3]})")
        
        try:
            product_id = int(input("\nSelect Product ID to delete: "))
            
            # Check if product belongs to seller
            check_query = "SELECT COUNT(*) FROM Product WHERE Product_ID = ? AND Seller_ID = ?"
            result = self.db.execute_query(check_query, (product_id, self.current_user[0]))
            if not result or result[0][0] == 0:
                print("❌ You don't own this product!")
                input("\nPress Enter...")
                return
            
            confirm = input(f"⚠️ Are you sure you want to delete product {product_id}? (y/n): ")
            if confirm.lower() == 'y':
                delete_query = "DELETE FROM Product WHERE Product_ID = ? AND Seller_ID = ?"
                if self.db.execute_command(delete_query, (product_id, self.current_user[0])):
                    print("\n✅ Product deleted successfully!")
                else:
                    print("\n❌ Failed to delete product!")
            else:
                print("\n❌ Deletion cancelled.")
                
        except ValueError:
            print("❌ Invalid input!")
        
        input("\nPress Enter...")
    
    # ============================================================
    # CUSTOMER FUNCTIONS (Only for customers)
    # ============================================================
    def add_address(self):
        """Add new address for current user"""
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
        """Create new order (Customer only)"""
        self.clear_screen()
        print("=" * 50)
        print("🛒 NEW ORDER")
        print("=" * 50)
        
        # Show available products
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
            # Insert order
            order_query = """
                INSERT INTO [Order] (User_ID, Address_ID, Order_Date, Total_Amount)
                VALUES (?, ?, GETDATE(), 0)
            """
            self.db.execute_command(order_query, (self.current_user[0], address_id))
            
            # Get Order ID
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
                
                # Update stock
                update_stock = "UPDATE Product SET Stock_Quantity = Stock_Quantity - ? WHERE Product_ID = ?"
                self.db.execute_command(update_stock, (quantity, product_id))
            
            # Update total amount
            update_total = "UPDATE [Order] SET Total_Amount = ? WHERE Order_ID = ?"
            self.db.execute_command(update_total, (total, order_id))
            
            # Insert payment
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
        """Show current user's orders (Customer only)"""
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
    
    # ============================================================
    # REVIEW FUNCTIONS (Customers only)
    # ============================================================
    
    def rate_product(self):
        """Submit a rating and review for a product (Customer only)"""
        self.clear_screen()
        print("=" * 50)
        print("⭐ RATE A PRODUCT")
        print("=" * 50)
        
        # Show all products
        query = "SELECT Product_ID, Product_Name, Price FROM Product"
        products = self.db.execute_query(query)
        
        if not products:
            print("❌ No products available!")
            input("\nPress Enter...")
            return
        
        print("\n📦 Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]}")
        
        try:
            product_id = int(input("\nSelect Product ID: "))
            
            check_query = "SELECT Product_Name FROM Product WHERE Product_ID = ?"
            result = self.db.execute_query(check_query, (product_id,))
            if not result:
                print("❌ Invalid product ID!")
                input("\nPress Enter...")
                return
            
            check_review = "SELECT COUNT(*) FROM Review WHERE User_ID = ? AND Product_ID = ?"
            review_result = self.db.execute_query(check_review, (self.current_user[0], product_id))
            if review_result and review_result[0][0] > 0:
                print("⚠️ You have already reviewed this product!")
                update = input("Would you like to update your review? (y/n): ")
                if update.lower() == 'y':
                    self.update_review(product_id)
                    input("\nPress Enter to continue...")
                return
            
            print(f"\n📝 Reviewing: {result[0][0]}")
            print("\nRating: 0.0 = Very Bad, 5.0 = Excellent")
            print("💡 You can use decimal numbers (e.g., 4.5, 3.7)")
            
            rating_input = input("Rating (0.0 - 5.0): ")
            rating = float(rating_input)
            
            if rating < 0 or rating > 5:
                print("❌ Rating must be between 0 and 5!")
                input("\nPress Enter...")
                return
            
            rating = round(rating, 1)
            
            comment = input("Comment (optional): ")
            if not comment:
                comment = None
            
            insert_query = """
                INSERT INTO Review (User_ID, Product_ID, Rating, Comment, Created_At)
                VALUES (?, ?, ?, ?, GETDATE())
            """
            if self.db.execute_command(insert_query, (self.current_user[0], product_id, rating, comment)):
                print(f"\n✅ Review submitted successfully! Rating: {rating:.1f}")
            else:
                print("\n❌ Failed to submit review!")
                
        except ValueError:
            print("❌ Invalid input! Please enter a number (e.g., 4.5)")
        
        input("\nPress Enter to continue...")
    
    def update_review(self, product_id):
        """Update existing review"""
        print("\n✏️ Update your review")
        print("Leave blank to keep current value.")
        
        # Get current review
        query = """
            SELECT Rating, Comment FROM Review 
            WHERE User_ID = ? AND Product_ID = ?
        """
        current = self.db.execute_query(query, (self.current_user[0], product_id))
        
        if not current:
            print("❌ You haven't reviewed this product yet!")
            return
        
        print(f"\nCurrent Rating: {current[0][0]:.1f}")
        print(f"Current Comment: {current[0][1] or 'No comment'}")
        
        try:
            new_rating_input = input("New Rating (0.0 - 5.0, blank to keep): ")
            if new_rating_input:
                new_rating = float(new_rating_input)
                if new_rating < 0 or new_rating > 5:
                    print("❌ Rating must be between 0 and 5!")
                    return
                new_rating = round(new_rating, 1)
            else:
                new_rating = current[0][0]
            
            new_comment = input("New Comment (blank to keep): ")
            if not new_comment:
                new_comment = current[0][1]
            
            update_query = """
                UPDATE Review 
                SET Rating = ?, Comment = ? 
                WHERE User_ID = ? AND Product_ID = ?
            """
            if self.db.execute_command(update_query, (new_rating, new_comment, self.current_user[0], product_id)):
                print(f"\n✅ Review updated successfully! New Rating: {new_rating:.1f}")
            else:
                print("\n❌ Failed to update review!")
                
        except ValueError:
            print("❌ Invalid input! Please enter a number (e.g., 4.5)")
    
    def view_product_reviews(self):
        """View all reviews for a specific product"""
        self.clear_screen()
        print("=" * 50)
        print("📝 VIEW PRODUCT REVIEWS")
        print("=" * 50)
        
        # Show all products
        query = """
            SELECT Product_ID, Product_Name, Price
            FROM Product
        """
        products = self.db.execute_query(query)
        
        if not products:
            print("❌ No products available!")
            input("\nPress Enter...")
            return
        
        print("\n📦 Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]}")
        
        try:
            product_id = int(input("\nSelect Product ID: "))
            
            # Get product name
            product_query = "SELECT Product_Name FROM Product WHERE Product_ID = ?"
            product_result = self.db.execute_query(product_query, (product_id,))
            if not product_result:
                print("❌ Invalid product ID!")
                input("\nPress Enter...")
                return
            
            print(f"\n📝 Reviews for: {product_result[0][0]}")
            print("-" * 50)
            
            # Get reviews with user name
            review_query = """
                SELECT u.Name, r.Rating, r.Comment, r.Created_At
                FROM Review r
                INNER JOIN [User] u ON r.User_ID = u.User_ID
                WHERE r.Product_ID = ?
                ORDER BY r.Created_At DESC
            """
            reviews = self.db.execute_query(review_query, (product_id,))
            
            if reviews:
                # Calculate average
                avg_query = "SELECT AVG(Rating) FROM Review WHERE Product_ID = ?"
                avg_result = self.db.execute_query(avg_query, (product_id,))
                avg_rating = avg_result[0][0] if avg_result and avg_result[0][0] else 0
                
                print(f"⭐ Average Rating: {avg_rating:.2f}/5.0")
                print(f"📊 Total Reviews: {len(reviews)}")
                print("-" * 50)
                
                for r in reviews:
                    rating = r[1]
                    full_stars = int(rating)
                    half_star = 1 if (rating - full_stars) >= 0.5 else 0
                    empty_stars = 5 - full_stars - half_star
                    
                    stars_display = "⭐" * full_stars + "½" * half_star + "☆" * empty_stars
                    
                    print(f"👤 {r[0]}")
                    print(f"   {stars_display} ({rating:.1f}/5.0)")
                    print(f"   📝 {r[2] if r[2] else 'No comment'}")
                    print(f"   📅 {r[3]}")
                    print("-" * 40)
            else:
                print("❌ No reviews yet for this product!")
                print("💡 Be the first to review this product!")
                
        except ValueError:
            print("❌ Invalid input!")
        
        input("\nPress Enter...")
    
    # ============================================================
    # MAIN RUN LOOP
    # ============================================================
    def run(self):
        """Main application loop"""
        if not self.db.connect():
            print("❌ Cannot connect to database!")
            return
        
        while True:
            self.display_main_menu()
            choice = input("Your choice: ")
            
            if not self.current_user:
                # Not logged in
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '0':
                    break
            else:
                if self.current_user[2] == 'seller':
                    # Seller menu
                    if choice == '1':
                        self.show_products()
                    elif choice == '2':
                        self.add_product()
                    elif choice == '3':
                        self.edit_product()
                    elif choice == '4':
                        self.update_stock()
                    elif choice == '5':
                        self.show_low_stock()
                    elif choice == '6':
                        self.delete_product()
                    elif choice == '7':
                        self.search_product()
                    elif choice == '8':
                        self.current_user = None
                        print("✅ Logged out successfully!")
                        input("\nPress Enter...")
                    elif choice == '0':
                        break
                else:
                    # Customer menu
                    if choice == '1':
                        self.show_products()
                    elif choice == '2':
                        self.create_order()
                    elif choice == '3':
                        self.show_my_orders()
                    elif choice == '4':
                        self.rate_product()
                    elif choice == '5':
                        self.view_product_reviews()
                    elif choice == '6':
                        self.search_product()
                    elif choice == '7':
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