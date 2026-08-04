-- ============================================
-- استفاده از دیتابیس OnlineShop
-- ============================================
USE OnlineShop;
GO

-- ============================================
-- ایجاد جدول User
-- ============================================
CREATE TABLE [User] (
    User_ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Password NVARCHAR(50) NOT NULL,
    User_Type NVARCHAR(20) CHECK (User_Type IN ('customer', 'seller', 'admin')) NOT NULL,
    Created_At DATE NOT NULL
);

-- ============================================
-- ایجاد جدول Category
-- ============================================
CREATE TABLE Category (
    Category_ID INT IDENTITY(1,1) PRIMARY KEY,
    Category_Name NVARCHAR(50) NOT NULL,
    Description NVARCHAR(200) NULL
);

-- ============================================
-- ایجاد جدول Address
-- ============================================
CREATE TABLE Address (
    Address_ID INT IDENTITY(1,1) PRIMARY KEY,
    User_ID INT NOT NULL,
    State NVARCHAR(50) NOT NULL,
    City NVARCHAR(50) NOT NULL,
    Street NVARCHAR(100) NOT NULL,
    Postal_Code NVARCHAR(20) NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES [User](User_ID) ON DELETE CASCADE
);

-- ============================================
-- ایجاد جدول Product
-- ============================================
CREATE TABLE Product (
    Product_ID INT IDENTITY(1,1) PRIMARY KEY,
    Product_Name NVARCHAR(100) NOT NULL,
    Category_ID INT NOT NULL,
    Seller_ID INT NOT NULL,
    Price DECIMAL(18,2) NOT NULL CHECK (Price >= 0),
    Stock_Quantity INT NOT NULL CHECK (Stock_Quantity >= 0),
    Created_At DATE NOT NULL,
    Description NVARCHAR(500) NULL,
    FOREIGN KEY (Category_ID) REFERENCES Category(Category_ID),
    FOREIGN KEY (Seller_ID) REFERENCES [User](User_ID)
);

-- ============================================
-- ایجاد جدول Cart
-- ============================================
CREATE TABLE Cart (
    Cart_ID INT IDENTITY(1,1) PRIMARY KEY,
    User_ID INT NOT NULL,
    Created_At DATE NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES [User](User_ID)
);

-- ============================================
-- ایجاد جدول Order
-- ============================================
CREATE TABLE [Order] (
    Order_ID INT IDENTITY(1,1) PRIMARY KEY,
    User_ID INT NOT NULL,
    Address_ID INT NOT NULL,
    Order_Date DATE NOT NULL,
    Total_Amount DECIMAL(18,2) NOT NULL CHECK (Total_Amount >= 0),
    FOREIGN KEY (User_ID) REFERENCES [User](User_ID),
    FOREIGN KEY (Address_ID) REFERENCES Address(Address_ID)
);

-- ============================================
-- ایجاد جدول Order_Item
-- ============================================
CREATE TABLE Order_Item (
    Order_Item_ID INT IDENTITY(1,1) PRIMARY KEY,
    Order_ID INT NOT NULL,
    Product_ID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    Price DECIMAL(18,2) NOT NULL CHECK (Price >= 0),
    FOREIGN KEY (Order_ID) REFERENCES [Order](Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);

-- ============================================
-- ایجاد جدول Payment
-- ============================================
CREATE TABLE Payment (
    Payment_ID INT IDENTITY(1,1) PRIMARY KEY,
    Order_ID INT NOT NULL,
    Payment_Date DATE NOT NULL,
    Amount DECIMAL(18,2) NOT NULL CHECK (Amount >= 0),
    Payment_Method NVARCHAR(20) CHECK (Payment_Method IN ('online', 'cash', 'card')),
    Payment_Status NVARCHAR(20) CHECK (Payment_Status IN ('success', 'pending', 'failed')) NOT NULL,
    FOREIGN KEY (Order_ID) REFERENCES [Order](Order_ID)
);

-- ============================================
-- ایجاد جدول Review
-- ============================================
CREATE TABLE Review (
    Review_ID INT IDENTITY(1,1) PRIMARY KEY,
    User_ID INT NOT NULL,
    Product_ID INT NOT NULL,
    Rating INT CHECK (Rating BETWEEN 1 AND 5) NOT NULL,
    Comment NVARCHAR(500) NULL,
    Created_At DATE NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES [User](User_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);