# services/user_service.py
class UserService:
    def __init__(self, db):
        self.db = db
    
    def register(self, name, email, password, user_type):
        check_query = "SELECT COUNT(*) FROM [User] WHERE Email = ?"
        result = self.db.execute_query(check_query, (email,))
        if result and result[0][0] > 0:
            return False, "This email is already registered!"
        
        query = """
            INSERT INTO [User] (Name, Email, Password, User_Type, Created_At)
            VALUES (?, ?, ?, ?, GETDATE())
        """
        if self.db.execute_command(query, (name, email, password, user_type)):
            return True, "Registration successful!"
        return False, "Registration failed!"
    
    def login(self, email, password):
        query = "SELECT User_ID, Name, User_Type FROM [User] WHERE Email = ? AND Password = ?"
        result = self.db.execute_query(query, (email, password))
        if result:
            return {'id': result[0][0], 'name': result[0][1], 'type': result[0][2]}
        return None
    
    def get_user_by_id(self, user_id):
        query = "SELECT User_ID, Name, Email, User_Type FROM [User] WHERE User_ID = ?"
        result = self.db.execute_query(query, (user_id,))
        if result:
            return {'id': result[0][0], 'name': result[0][1], 'email': result[0][2], 'type': result[0][3]}
        return None