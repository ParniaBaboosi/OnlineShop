# database.py
import pyodbc
from config import CONNECTION_STRING

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = pyodbc.connect(CONNECTION_STRING)
            self.cursor = self.connection.cursor()
            print("✅ Connected to database successfully!")
            return True
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("✅ Disconnected.")
    
    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Query error: {e}")
            return None
    
    def execute_command(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Command error: {e}")
            self.connection.rollback()
            return False
    
    def get_last_id(self):
        """Get last inserted ID using SCOPE_IDENTITY()"""
        try:
            self.cursor.execute("SELECT SCOPE_IDENTITY()")
            result = self.cursor.fetchone()
            if result and result[0]:
                return result[0]
            return None
        except Exception as e:
            print(f"❌ Error getting last ID: {e}")
            return None