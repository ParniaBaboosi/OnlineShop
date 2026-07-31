# config.py
SERVER = 'LAPTOP-DQK5928F'  # یا 'localhost' یا '.'
DATABASE = 'OnlineShop'

CONNECTION_STRING = f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={SERVER};
    DATABASE={DATABASE};
    Trusted_Connection=yes;
"""