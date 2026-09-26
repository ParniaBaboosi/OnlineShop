# services/product_service.py
class ProductService:
    def __init__(self, db):
        self.db = db
    
    def get_all(self):
        query = """
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, 
                   p.Price, p.Stock_Quantity, u.Name AS Seller,
                   p.Brand, p.Colors, p.Size, p.Material,
                   p.Gender, p.Season, p.Discount, p.Discount_Price,
                   p.IsFeatured, p.IsNew, p.IsBestSeller,
                   p.Warranty, p.Return_Policy,
                   ISNULL(AVG(CAST(r.Rating AS FLOAT)), 0) AS Avg_Rating,
                   COUNT(r.Review_ID) AS Review_Count
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            INNER JOIN [User] u ON p.Seller_ID = u.User_ID
            LEFT JOIN Review r ON p.Product_ID = r.Product_ID
            GROUP BY p.Product_ID, p.Product_Name, c.Category_Name, 
                     p.Price, p.Stock_Quantity, u.Name,
                     p.Brand, p.Colors, p.Size, p.Material,
                     p.Gender, p.Season, p.Discount, p.Discount_Price,
                     p.IsFeatured, p.IsNew, p.IsBestSeller,
                     p.Warranty, p.Return_Policy
            ORDER BY p.Product_ID
        """
        return self.db.execute_query(query)
    
    def get_by_id(self, product_id):
        query = """
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, 
                   p.Price, p.Stock_Quantity, u.Name AS Seller,
                   p.Brand, p.Colors, p.Size, p.Material,
                   p.Weight, p.Gender, p.Season, 
                   p.Discount, p.Discount_Price,
                   p.IsFeatured, p.IsNew, p.IsBestSeller,
                   p.Views, p.Sales_Count,
                   p.Warranty, p.Return_Policy,
                   p.Video_URL, p.Image_URL,
                   ISNULL(AVG(CAST(r.Rating AS FLOAT)), 0) AS Avg_Rating,
                   COUNT(r.Review_ID) AS Review_Count
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            INNER JOIN [User] u ON p.Seller_ID = u.User_ID
            LEFT JOIN Review r ON p.Product_ID = r.Product_ID
            WHERE p.Product_ID = ?
            GROUP BY p.Product_ID, p.Product_Name, c.Category_Name, 
                     p.Price, p.Stock_Quantity, u.Name,
                     p.Brand, p.Colors, p.Size, p.Material,
                     p.Weight, p.Gender, p.Season, 
                     p.Discount, p.Discount_Price,
                     p.IsFeatured, p.IsNew, p.IsBestSeller,
                     p.Views, p.Sales_Count,
                     p.Warranty, p.Return_Policy,
                     p.Video_URL, p.Image_URL
        """
        return self.db.execute_query(query, (product_id,))
    
    def search(self, keyword):
        query = """
            SELECT p.Product_ID, p.Product_Name, p.Brand, c.Category_Name,
                   p.Price, p.Discount_Price, p.Stock_Quantity,
                   p.Colors, p.Size, p.Material,
                   ISNULL(AVG(CAST(r.Rating AS FLOAT)), 0) AS Avg_Rating
            FROM Product p
            INNER JOIN Category c ON p.Category_ID = c.Category_ID
            LEFT JOIN Review r ON p.Product_ID = r.Product_ID
            WHERE p.Product_Name LIKE ? OR p.Brand LIKE ? OR p.Colors LIKE ? 
               OR p.Material LIKE ? OR p.Description LIKE ?
            GROUP BY p.Product_ID, p.Product_Name, p.Brand, c.Category_Name,
                     p.Price, p.Discount_Price, p.Stock_Quantity,
                     p.Colors, p.Size, p.Material
        """
        return self.db.execute_query(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    
    def add(self, seller_id, name, category_id, price, stock, description,
            brand=None, colors=None, size=None, material=None, weight=None,
            gender=None, season=None, discount=0, is_featured=False,
            is_new=False, is_best_seller=False, warranty=None,
            return_policy=None, image_url=None, video_url=None):
        discount_price = price - (price * discount / 100) if discount > 0 else price
        query = """
            INSERT INTO Product (
                Product_Name, Category_ID, Seller_ID, Price, Stock_Quantity, 
                Created_At, Description,
                Brand, Colors, Size, Material, Weight, Gender, Season,
                Discount, Discount_Price, IsFeatured, IsNew, IsBestSeller,
                Video_URL, Image_URL, Warranty, Return_Policy
            )
            VALUES (?, ?, ?, ?, ?, GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_command(query, (
            name, category_id, seller_id, price, stock, description,
            brand, colors, size, material, weight, gender, season,
            discount, discount_price, is_featured, is_new, is_best_seller,
            video_url, image_url, warranty, return_policy
        ))
    
    def update(self, product_id, seller_id, name, price, stock):
        query = "UPDATE Product SET Product_Name = ?, Price = ?, Stock_Quantity = ? WHERE Product_ID = ? AND Seller_ID = ?"
        return self.db.execute_command(query, (name, price, stock, product_id, seller_id))
    
    def update_stock(self, product_id, seller_id, stock):
        query = "UPDATE Product SET Stock_Quantity = ? WHERE Product_ID = ? AND Seller_ID = ?"
        return self.db.execute_command(query, (stock, product_id, seller_id))
    
    def delete(self, product_id, seller_id):
        query = "DELETE FROM Product WHERE Product_ID = ? AND Seller_ID = ?"
        return self.db.execute_command(query, (product_id, seller_id))
    
    def get_low_stock(self, seller_id, threshold=10):
        query = """
            SELECT Product_ID, Product_Name, Stock_Quantity
            FROM Product
            WHERE Seller_ID = ? AND Stock_Quantity <= ?
            ORDER BY Stock_Quantity ASC
        """
        return self.db.execute_query(query, (seller_id, threshold))
    
    def get_variants(self, product_id):
        query = "SELECT Colors, Size FROM Product WHERE Product_ID = ?"
        result = self.db.execute_query(query, (product_id,))
        if result:
            colors = result[0][0].split(',') if result[0][0] else []
            sizes = result[0][1].split(',') if result[0][1] else []
            return colors, sizes
        return [], []
    
    def get_categories(self):
        query = "SELECT Category_ID, Category_Name FROM Category"
        return self.db.execute_query(query)