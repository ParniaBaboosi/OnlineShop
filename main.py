# main.py
import os
import random
import datetime
from database import Database
from services import UserService, ProductService, OrderService, PaymentService, ReviewService

class OnlineShopApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.user_service = UserService(self.db)
        self.product_service = ProductService(self.db)
        self.order_service = OrderService(self.db)
        self.payment_service = PaymentService(self.db)
        self.review_service = ReviewService(self.db)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_main_menu(self):
        self.clear_screen()
        print("=" * 50)
        print("🛍️  ONLINE SHOP")
        print("=" * 50)
        if self.current_user:
            print(f"👤 User: {self.current_user['name']} ({self.current_user['type']})")
            print("-" * 50)
            if self.current_user['type'] == 'seller':
                print("1. 📦 View Products")
                print("2. ➕ Add New Product")
                print("3. ✏️ Edit Product")
                print("4. 📦 Update Stock (Quick)")
                print("5. ⚠️ Low Stock Alert")
                print("6. 🗑️ Delete Product")
                print("7. 🔍 Search Product")
                print("8. 🚪 Logout")
            else:
                print("1. 📦 View Products")
                print("2. 🛒 New Order")
                print("3. 📋 My Orders & Transactions")
                print("4. ⭐ Rate a Product")
                print("5. 📝 View Product Reviews")
                print("6. 🔍 Search Product")
                print("7. 🚪 Logout")
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
        
        success, msg = self.user_service.register(name, email, password, user_type)
        print(f"\n{'✅' if success else '❌'} {msg}")
        input("\nPress Enter...")
    
    def login(self):
        self.clear_screen()
        print("=" * 50)
        print("🔑 LOGIN FORM")
        print("=" * 50)
        
        email = input("Email: ")
        password = input("Password: ")
        
        user = self.user_service.login(email, password)
        if user:
            self.current_user = user
            print(f"\n✅ Welcome {user['name']}!")
        else:
            print("\n❌ Invalid email or password!")
        
        input("\nPress Enter...")
    
    def show_products(self):
        self.clear_screen()
        print("=" * 80)
        print("📦 PRODUCT LIST")
        print("=" * 80)
        
        products = self.product_service.get_all()
        
        if products:
            while True:
                self.clear_screen()
                print("=" * 80)
                print("📦 PRODUCT LIST")
                print("=" * 80)
                
                print("-" * 130)
                print(f"{'ID':<4} {'Name':<18} {'Brand':<10} {'Category':<12} {'Price':<10} {'Stock':<6} {'Rating':<6} {'Seller':<10}")
                print("-" * 130)
                for p in products:
                    rating = f"{p[19]:.1f}" if p[19] > 0 else "-"
                    brand = p[6] or "-"
                    discount_price = p[13] or p[3]
                    
                    print(f"{p[0]:<4} {p[1][:17]:<18} {brand[:9]:<10} {p[2][:11]:<12} ${discount_price:<10} {p[4]:<6} {rating:<6} {p[5][:9]:<10}")
                
                print("\n" + "-" * 130)
                print("📌 Options:")
                print("   Enter Product ID to view details")
                print("   0. Back to main menu")
                
                try:
                    choice = input("\nYour choice: ")
                    if choice == '0':
                        break
                    view_id = int(choice)
                    if view_id > 0:
                        self.show_product_details(view_id)
                        input("\nPress Enter to continue...")
                except ValueError:
                    print("❌ Invalid input!")
                    input("\nPress Enter...")
        else:
            print("❌ No products found!")
            input("\nPress Enter...")
    
    def show_product_details(self, product_id):
        print("=" * 80)
        print("📦 PRODUCT DETAILS")
        print("=" * 80)
        
        result = self.product_service.get_by_id(product_id)
        
        if result:
            p = result[0]
            rating = f"{p[24]:.1f}" if p[24] > 0 else "No ratings"
            
            print(f"\n🆔 ID: {p[0]}")
            print(f"📝 Name: {p[1]}")
            print(f"📂 Category: {p[2]}")
            print(f"💰 Price: ${p[3]}")
            if p[13] and p[13] > 0:
                print(f"   🔥 Discount: {p[13]:.0f}% → ${p[14]:.2f}")
            print(f"📦 Stock: {p[4]}")
            print(f"👤 Seller: {p[5]}")
            print(f"🏷️ Brand: {p[6] or 'N/A'}")
            print(f"🎨 Colors: {p[7] or 'N/A'}")
            print(f"📏 Sizes: {p[8] or 'N/A'}")
            print(f"🧵 Material: {p[9] or 'N/A'}")
            print(f"⚖️ Weight: {p[10] or 'N/A'} g")
            print(f"👤 Gender: {p[11] or 'N/A'}")
            print(f"🌤️ Season: {p[12] or 'N/A'}")
            print(f"⭐ Rating: {rating} ({p[25]} reviews)")
            print(f"👁️ Views: {p[18] or 0}")
            print(f"📈 Sales: {p[19] or 0}")
            print(f"🛡️ Warranty: {p[20] or 'N/A'}")
            print(f"🔄 Return Policy: {p[21] or 'N/A'}")
            if p[22]:
                print(f"🎬 Video: {p[22]}")
            if p[23]:
                print(f"🖼️ Image: {p[23]}")
            
            statuses = []
            if p[15]: statuses.append("⭐ Featured")
            if p[16]: statuses.append("🆕 New")
            if p[17]: statuses.append("🏆 Best Seller")
            if statuses:
                print(f"🏷️ Status: {', '.join(statuses)}")
        else:
            print("❌ Product not found!")
        
        print("-" * 80)
    
    def search_product(self):
        self.clear_screen()
        print("=" * 80)
        print("🔍 SEARCH PRODUCT")
        print("=" * 80)
        
        print("\n🔎 Search by:")
        print("  1. Keyword (name, brand, color, material)")
        print("  2. Price range")
        print("  3. Gender")
        print("  4. Season")
        print("  5. Brand")
        
        search_type = input("\nChoose search type (1-5): ")
        keyword = input("Enter search keyword: ")
        
        products = self.product_service.search(keyword)
        
        if products:
            print(f"\n📦 Search Results ({len(products)} found):")
            print("-" * 100)
            print(f"{'ID':<4} {'Name':<20} {'Brand':<10} {'Category':<12} {'Price':<10} {'Stock':<6} {'Rating':<6}")
            print("-" * 100)
            for p in products:
                rating = f"{p[-1]:.1f}" if p[-1] > 0 else "-"
                price = p[5] if p[5] and p[5] > 0 else p[4]
                brand = p[2] or "-"
                print(f"{p[0]:<4} {p[1][:19]:<20} {brand[:9]:<10} {p[3][:11]:<12} ${price:<10} {p[6]:<6} {rating:<6}")
            
            try:
                view_id = int(input("\nEnter Product ID to view details (0 to skip): "))
                if view_id > 0:
                    self.show_product_details(view_id)
                    input("\nPress Enter to continue...")
            except ValueError:
                pass
        else:
            print("❌ No products found matching your search!")
        
        input("\nPress Enter...")
    
    # ============================================================
    # SELLER FUNCTIONS
    # ============================================================
    
    def add_product(self):
        self.clear_screen()
        print("=" * 60)
        print("➕ ADD NEW PRODUCT")
        print("=" * 60)
        
        name = input("Product Name: ")
        
        categories = self.product_service.get_categories()
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
            
            print("\n📋 Product Details (press Enter to skip optional fields):")
            brand = input("Brand: ") or None
            colors = input("Colors (comma separated): ") or None
            size = input("Sizes (comma separated): ") or None
            material = input("Material: ") or None
            weight_input = input("Weight (grams): ")
            weight = float(weight_input) if weight_input else None
            gender = input("Gender (Men/Women/Unisex/Kids): ") or None
            season = input("Season: ") or None
            discount_input = input("Discount (%): ")
            discount = float(discount_input) if discount_input else 0
            is_featured = input("Is Featured? (y/n): ").lower() == 'y'
            is_new = input("Is New? (y/n): ").lower() == 'y'
            is_best_seller = input("Is Best Seller? (y/n): ").lower() == 'y'
            warranty = input("Warranty: ") or None
            return_policy = input("Return Policy: ") or None
            image_url = input("Image URL: ") or None
            video_url = input("Video URL: ") or None
            
        except ValueError:
            print("❌ Invalid input!")
            input("\nPress Enter...")
            return
        
        if self.product_service.add(
            self.current_user['id'], name, category_id, price, stock, description,
            brand, colors, size, material, weight, gender, season,
            discount, is_featured, is_new, is_best_seller,
            warranty, return_policy, image_url, video_url
        ):
            discount_price = price - (price * discount / 100) if discount > 0 else price
            print("\n✅ Product added successfully!")
            print(f"   📊 Final Price: ${discount_price:.2f}")
        else:
            print("\n❌ Failed to add product!")
        
        input("\nPress Enter...")
    
    def edit_product(self):
        self.clear_screen()
        print("=" * 50)
        print("✏️ EDIT PRODUCT")
        print("=" * 50)
        
        products = self.product_service.get_seller_products(self.current_user['id'])
        
        if not products:
            print("❌ You have no products to edit!")
            input("\nPress Enter...")
            return
        
        print("\nYour Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]} (Stock: {p[3]})")
        
        try:
            product_id = int(input("\nSelect Product ID to edit: "))
            current = self.product_service.get_by_id(product_id)
            if not current:
                print("❌ You don't own this product!")
                input("\nPress Enter...")
                return
            
            current = current[0]
            print(f"\nCurrent: Name={current[1]}, Price=${current[3]}, Stock={current[4]}")
            print("\nLeave blank to keep current value.")
            
            new_name = input(f"New Name (current: {current[1]}): ") or current[1]
            new_price_input = input(f"New Price (current: {current[3]}): ")
            new_price = float(new_price_input) if new_price_input else current[3]
            new_stock_input = input(f"New Stock (current: {current[4]}): ")
            new_stock = int(new_stock_input) if new_stock_input else current[4]
            
            if self.product_service.update(product_id, self.current_user['id'], new_name, new_price, new_stock):
                print("\n✅ Product updated successfully!")
            else:
                print("\n❌ Failed to update product!")
        except ValueError:
            print("❌ Invalid input!")
        
        input("\nPress Enter...")
    
    def update_stock(self):
        self.clear_screen()
        print("=" * 50)
        print("📦 UPDATE STOCK")
        print("=" * 50)
        
        products = self.product_service.get_seller_products(self.current_user['id'])
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
            
            if self.product_service.update_stock(product_id, self.current_user['id'], new_stock):
                print("\n✅ Stock updated successfully!")
            else:
                print("\n❌ Failed to update stock!")
        except ValueError:
            print("❌ Invalid input!")
        
        input("\nPress Enter...")
    
    def show_low_stock(self):
        self.clear_screen()
        print("=" * 50)
        print("⚠️ LOW STOCK ALERT")
        print("=" * 50)
        
        threshold_input = input("Enter stock threshold (default: 10): ")
        threshold = int(threshold_input) if threshold_input else 10
        
        products = self.product_service.get_low_stock(self.current_user['id'], threshold)
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
        self.clear_screen()
        print("=" * 50)
        print("🗑️ DELETE PRODUCT")
        print("=" * 50)
        
        products = self.product_service.get_seller_products(self.current_user['id'])
        if not products:
            print("❌ You have no products to delete!")
            input("\nPress Enter...")
            return
        
        print("\nYour Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]} (Stock: {p[3]})")
        
        try:
            product_id = int(input("\nSelect Product ID to delete: "))
            confirm = input(f"⚠️ Are you sure you want to delete product {product_id}? (y/n): ")
            if confirm.lower() == 'y':
                if self.product_service.delete(product_id, self.current_user['id']):
                    print("\n✅ Product deleted successfully!")
                else:
                    print("\n❌ Failed to delete product!")
            else:
                print("\n❌ Deletion cancelled.")
        except ValueError:
            print("❌ Invalid input!")
        
        input("\nPress Enter...")
    
    # ============================================================
    # CUSTOMER FUNCTIONS
    # ============================================================
    
    def add_address(self):
        print("\n📌 ADD NEW ADDRESS")
        state = input("State: ")
        city = input("City: ")
        street = input("Street: ")
        postal_code = input("Postal Code: ")
        
        if self.order_service.add_address(self.current_user['id'], state, city, street, postal_code):
            print("✅ Address added successfully!")
            return True
        else:
            print("❌ Failed to add address!")
            return False
    
    def create_order(self):
        self.clear_screen()
        print("=" * 60)
        print("🛒 NEW ORDER")
        print("=" * 60)
        
        products = self.order_service.get_available_products()
        
        if not products:
            print("❌ No products available for purchase!")
            input("\nPress Enter...")
            return
        
        print("\nAvailable Products:")
        print("-" * 80)
        print(f"{'ID':<4} {'Name':<18} {'Brand':<10} {'Price':<10} {'Stock':<6} {'Colors':<15} {'Sizes':<12}")
        print("-" * 80)
        for p in products:
            colors = p[4][:14] if p[4] else "-"
            sizes = p[5][:11] if p[5] else "-"
            brand = p[6][:9] if p[6] else "-"
            print(f"{p[0]:<4} {p[1][:17]:<18} {brand:<10} ${p[2]:<10} {p[3]:<6} {colors:<15} {sizes:<12}")
        print("-" * 80)
        print("Enter 0 to finish ordering\n")
        
        addresses = self.order_service.get_addresses(self.current_user['id'])
        
        if not addresses:
            print("\n⚠️ You have no address registered!")
            add_addr = input("Would you like to add an address? (y/n): ")
            if add_addr.lower() == 'y':
                if not self.add_address():
                    input("\nPress Enter...")
                    return
                addresses = self.order_service.get_addresses(self.current_user['id'])
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
        
        items = []
        total = 0
        
        while True:
            print("\n" + "-" * 40)
            print(f"📦 Add product to order (Total: ${total:.2f})")
            print("Enter 0 to finish ordering")
            print("-" * 40)
            
            try:
                product_id = int(input("Product ID (0 to finish): "))
                if product_id == 0:
                    break
                
                product = self.product_service.get_by_id(product_id)
                if not product:
                    print("❌ Invalid product ID or out of stock!")
                    continue
                
                p = product[0]
                colors, sizes = self.product_service.get_variants(product_id)
                
                print(f"\n📝 {p[1]} - ${p[3]}")
                
                selected_color = None
                if colors and len(colors) > 1:
                    print("\n🎨 Available Colors:")
                    for i, c in enumerate(colors, 1):
                        print(f"  {i}. {c.strip()}")
                    color_choice = input("Choose color (number): ")
                    try:
                        idx = int(color_choice) - 1
                        if 0 <= idx < len(colors):
                            selected_color = colors[idx].strip()
                        else:
                            print("❌ Invalid color!")
                            continue
                    except ValueError:
                        selected_color = colors[0].strip()
                elif colors:
                    selected_color = colors[0].strip()
                    print(f"🎨 Color: {selected_color}")
                
                selected_size = None
                if sizes and len(sizes) > 1:
                    print("\n📏 Available Sizes:")
                    for i, s in enumerate(sizes, 1):
                        print(f"  {i}. {s.strip()}")
                    size_choice = input("Choose size (number): ")
                    try:
                        idx = int(size_choice) - 1
                        if 0 <= idx < len(sizes):
                            selected_size = sizes[idx].strip()
                        else:
                            print("❌ Invalid size!")
                            continue
                    except ValueError:
                        selected_size = sizes[0].strip()
                elif sizes:
                    selected_size = sizes[0].strip()
                    print(f"📏 Size: {selected_size}")
                
                quantity = int(input(f"Quantity (Stock: {p[4]}): "))
                if quantity <= 0:
                    print("❌ Quantity must be greater than 0!")
                    continue
                if quantity > p[4]:
                    print(f"❌ Not enough stock! Available: {p[4]}")
                    continue
                
                items.append({
                    'product_id': p[0],
                    'name': p[1],
                    'price': p[3],
                    'quantity': quantity,
                    'color': selected_color,
                    'size': selected_size
                })
                total += p[3] * quantity
                print(f"✅ Added: {p[1]} x{quantity} - ${p[3] * quantity:.2f}")
                
            except ValueError:
                print("❌ Invalid input!")
        
        if not items:
            print("❌ Order cancelled.")
            input("\nPress Enter...")
            return
        
        # Payment selection
        print("\n" + "=" * 50)
        print("💳 SELECT PAYMENT METHOD")
        print("=" * 50)
        methods = self.payment_service.get_payment_methods()
        for i, m in enumerate(methods, 1):
            print(f"{i}. {m['name']}")
        print("-" * 50)
        
        method_choice = input("Choose payment method (1-5): ")
        method_map = {str(i+1): m for i, m in enumerate(methods)}
        
        if method_choice not in method_map:
            print("❌ Invalid payment method!")
            input("\nPress Enter...")
            return
        
        payment_method = method_map[method_choice]
        
        print("\n" + "=" * 50)
        print("⏳ Processing payment...")
        print(f"💳 Method: {payment_method['name']}")
        print("-" * 50)
        
        is_successful = random.random() < 0.95
        
        if is_successful:
            print("✅ Payment Successful!")
            status = 'success'
        else:
            print("❌ Payment Failed!")
            print("💡 Please try again or use another method.")
            status = 'failed'
        
        try:
            order_id, total = self.order_service.create(self.current_user['id'], address_id, items)
            
            if not order_id:
                raise Exception("Failed to create order!")
            
            self.payment_service.create(order_id, total, payment_method['id'], status)
            
            print("\n" + "=" * 50)
            print("📋 ORDER SUMMARY")
            print("=" * 50)
            print(f"🆔 Order ID: {order_id}")
            print(f"📅 Date: {datetime.date.today()}")
            print(f"💰 Total: ${total}")
            print(f"💳 Payment: {payment_method['name']}")
            print(f"📊 Status: {'✅ Success' if status == 'success' else '❌ Failed'}")
            
            print("\n📦 Items:")
            for item in items:
                variant_info = ""
                if item.get('color'):
                    variant_info += f" Color: {item['color']}"
                if item.get('size'):
                    variant_info += f" Size: {item['size']}"
                print(f"   - {item['name']} x{item['quantity']} - ${item['price'] * item['quantity']:.2f}{variant_info}")
            
            if status == 'success':
                print("\n✅ Your order has been placed successfully!")
            else:
                print("\n❌ Payment failed. Please try again.")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error creating order: {e}")
        
        input("\nPress Enter...")
    
    def show_my_orders(self):
        self.clear_screen()
        print("=" * 80)
        print("📋 MY ORDERS & TRANSACTIONS")
        print("=" * 80)
        
        orders = self.order_service.get_user_orders(self.current_user['id'])
        
        if orders:
            for o in orders:
                status_icon = "✅" if o[5] == 'success' else "⏳" if o[5] == 'pending' else "❌"
                method_display = o[4].replace('_', ' ').title() if o[4] else '-'
                
                print(f"\n{'='*70}")
                print(f"🆔 ORDER #{o[0]}")
                print(f"📅 Date: {o[1]}")
                print(f"💰 Total: ${o[2]}")
                print(f"📦 Items: {o[3]}")
                print("-" * 70)
                print(f"💳 Payment: {method_display}")
                print(f"📊 Status: {status_icon} {o[5]}")
                print(f"🔢 Transaction ID: {o[6] or 'N/A'}")
                print(f"📌 Tracking Code: {o[7] or 'N/A'}")
                if o[8]:
                    print(f"✅ Approved: {o[8]}")
                print("=" * 70)
                
                details = self.order_service.get_order_details(o[0])
                if details:
                    print("📦 Items:")
                    for d in details:
                        print(f"   - {d[0]} x{d[1]} = ${d[2] * d[1]:.2f}")
        else:
            print("❌ You have no orders!")
        
        input("\nPress Enter...")
    
    # ============================================================
    # REVIEW FUNCTIONS
    # ============================================================
    
    def rate_product(self):
        self.clear_screen()
        print("=" * 50)
        print("⭐ RATE A PRODUCT")
        print("=" * 50)
        
        products = self.review_service.get_all_products()
        
        if not products:
            print("❌ No products available!")
            input("\nPress Enter...")
            return
        
        print("\n📦 Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]}")
        
        try:
            product_id = int(input("\nSelect Product ID: "))
            product_name = self.product_service.get_by_id(product_id)
            if not product_name:
                print("❌ Invalid product ID!")
                input("\nPress Enter...")
                return
            
            if self.review_service.has_user_reviewed(self.current_user['id'], product_id):
                print("⚠️ You have already reviewed this product!")
                update = input("Would you like to update your review? (y/n): ")
                if update.lower() == 'y':
                    self.update_review(product_id)
                    input("\nPress Enter to continue...")
                return
            
            print(f"\n📝 Reviewing: {product_name[0][1]}")
            print("\nRating: 0.0 = Very Bad, 5.0 = Excellent")
            
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
            
            if self.review_service.create(self.current_user['id'], product_id, rating, comment):
                print(f"\n✅ Review submitted successfully! Rating: {rating:.1f}")
            else:
                print("\n❌ Failed to submit review!")
        except ValueError:
            print("❌ Invalid input! Please enter a number (e.g., 4.5)")
        
        input("\nPress Enter to continue...")
    
    def update_review(self, product_id):
        print("\n✏️ Update your review")
        print("Leave blank to keep current value.")
        
        current = self.db.execute_query(
            "SELECT Rating, Comment FROM Review WHERE User_ID = ? AND Product_ID = ?",
            (self.current_user['id'], product_id)
        )
        
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
            
            if self.review_service.update(self.current_user['id'], product_id, new_rating, new_comment):
                print(f"\n✅ Review updated successfully! New Rating: {new_rating:.1f}")
            else:
                print("\n❌ Failed to update review!")
        except ValueError:
            print("❌ Invalid input! Please enter a number (e.g., 4.5)")
    
    def view_product_reviews(self):
        self.clear_screen()
        print("=" * 50)
        print("📝 VIEW PRODUCT REVIEWS")
        print("=" * 50)
        
        products = self.review_service.get_all_products()
        
        if not products:
            print("❌ No products available!")
            input("\nPress Enter...")
            return
        
        print("\n📦 Products:")
        for p in products:
            print(f"  {p[0]}. {p[1]} - ${p[2]}")
        
        try:
            product_id = int(input("\nSelect Product ID: "))
            product_name = self.product_service.get_by_id(product_id)
            if not product_name:
                print("❌ Invalid product ID!")
                input("\nPress Enter...")
                return
            
            print(f"\n📝 Reviews for: {product_name[0][1]}")
            print("-" * 50)
            
            reviews = self.review_service.get_product_reviews(product_id)
            avg_rating = self.review_service.get_avg_rating(product_id)
            
            if reviews:
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
    # MAIN LOOP
    # ============================================================
    
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
                if self.current_user['type'] == 'seller':
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