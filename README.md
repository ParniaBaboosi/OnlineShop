# 🛍️ Online Shop Management System
A comprehensive **Online Shop Management System** built with **Python** and **Microsoft SQL Server**. 
This project was developed as a Database course project and includes a full CLI (Command Line Interface) for managing users, products, orders, and payments.
## ✨ Features

### 👤 Authentication
- **Register** as Customer or Seller
- **Login** with email and password
- **Logout** functionality

### 🛒 Customer Features
- View all products with price, stock, category, and seller info
- Search products by name or description
- Place orders with address selection
- View order history with order details
- Automatic stock reduction after purchase

### 🏪 Seller Features
- **Add** new products (name, category, price, stock, description)
- **Edit** existing products (update name, price, or stock)
- **Quick stock update** (change stock quantity only)
- **Low stock alert** (view products below threshold)
- **Delete** products from store

---

## 🛠️ Technologies Used

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| Database | Microsoft SQL Server |
| Database Driver | PyODBC |
| IDE | VS Code |
| Version Control | Git & GitHub |

---
## 🚀 How to Run

### Prerequisites
- Python 3.x installed
- Microsoft SQL Server (Local or Express)
- SQL Server Management Studio (SSMS)
- ODBC Driver 17 for SQL Server

### Setup Instructions

1. **Clone the repository**
   ``` bash
   git clone https://github.com/
   ParniaBaboosi/OnlineShop.git
   cd OnlineShop
   ```
2. **Install Python dependencies**
   ``` bash 
   pip install pyodbc
   ```
3. **Configure database connection**

- Open config.py and update your server details:

  ```python
  SERVER = 'localhost'  # or 'LAPTOP-XXXX' or '.'
  DATABASE = 'OnlineShop'
  ```

4. **Run the SQL script**

- Open making tables.sql in SSMS

- Execute it to create all tables and insert sample data 
5. **Run the application**

   ```bash
   cd "PYTHON onlineshop"
   python main.py
   ```
