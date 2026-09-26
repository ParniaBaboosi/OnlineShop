# services/review_service.py
class ReviewService:
    def __init__(self, db):
        self.db = db
    
    def create(self, user_id, product_id, rating, comment):
        query = """
            INSERT INTO Review (User_ID, Product_ID, Rating, Comment, Created_At)
            VALUES (?, ?, ?, ?, GETDATE())
        """
        return self.db.execute_command(query, (user_id, product_id, rating, comment))
    
    def update(self, user_id, product_id, rating, comment):
        query = """
            UPDATE Review 
            SET Rating = ?, Comment = ? 
            WHERE User_ID = ? AND Product_ID = ?
        """
        return self.db.execute_command(query, (rating, comment, user_id, product_id))
    
    def get_product_reviews(self, product_id):
        query = """
            SELECT u.Name, r.Rating, r.Comment, r.Created_At
            FROM Review r
            INNER JOIN [User] u ON r.User_ID = u.User_ID
            WHERE r.Product_ID = ?
            ORDER BY r.Created_At DESC
        """
        return self.db.execute_query(query, (product_id,))
    
    def get_avg_rating(self, product_id):
        query = "SELECT AVG(Rating) FROM Review WHERE Product_ID = ?"
        result = self.db.execute_query(query, (product_id,))
        return result[0][0] if result and result[0][0] else 0
    
    def has_user_reviewed(self, user_id, product_id):
        query = "SELECT COUNT(*) FROM Review WHERE User_ID = ? AND Product_ID = ?"
        result = self.db.execute_query(query, (user_id, product_id))
        return result and result[0][0] > 0
    
    def get_all_products(self):
        query = "SELECT Product_ID, Product_Name, Price FROM Product"
        return self.db.execute_query(query)