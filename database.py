import sqlite3

conn=sqlite3.connect("crm.db")
#A file named crm.db is created even if it doesnt exist.

cursor=conn.cursor()

#Create the tables

cursor.execute("""
CREATE TABLE customers (
    cust_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    tier  TEXT
)
""")
               
cursor.execute("""
INSERT INTO customers
VALUES(
       1,
       'Ankit Chabra',
       'ankit@gmail.com',
       'Gold'
)
               
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_name TEXT,
    category TEXT,
    price REAL,
    purchase_date TEXT,
    delivered_date TEXT,
    final_sale INTEGER,
    FOREIGN KEY(customer_id)
        REFERENCES customers(cust_id)
)
""")


cursor.execute("""
INSERT INTO customers Values
(2,'Rohit Arora','rohit21@gmail.com','Silver'),
(3,'Sejal Sharma','sejal@gmail.com','Silver'),
(4,'Sumit Shah','sumit@gmail.com','Gold'),
(5,'Kritika Jha','kritika@gmail.com','Bronze'),
(6,'Ravi Kumar','ravi@gmail.com','Gold'),
(7,'Shweta Malhotra','shweta@gmail.com','Silver'),
(8,'Kushal Kamra','kushal@gmail.com','Bronze'),
(9,'Ankita Khanna','khanna@gmail.com','Bronze'),
(10,'Lata Ahuja','ahuja@gmail.com','Gold'),
(11,'Garv Kalra','garv@gmail.com','Silver'),
(12,'Latika Chawla','chawla@gmail.com','Bronze'),
(13,'Harsh Tyagi','harsh@gmail.com','Gold'),
(14,'Rahul Bora','rahul@gmail.com','Silver'),
(15,'Khushi Singh','khushi@gmail.com','Bronze')
""")               



cursor.execute("""
INSERT INTO orders VALUES
(1,3,'earphones','Electronics',670,'07-05-2026','09-05-2026',1),
(2,8,'Phillips Iron','Electronics',900,'05-04-2026','09-04-2026',0),
(3,15,'Kids Frock','Clothes',200,'15-05-2026','16-05-2026',0),
(4,13,'Bloomers','Clothes',100,'03-05-2026','05-05-2026',0),
(5,7,'Blue Skirt','Clothes',67,'02-04-2026','04-04-2026',0),
(6,13,'Blender','Electronics',96,'04-03-2026','05-03-2026',1),
(7,4,'Foundation','Beauty Products',599,'06-05-2026','07-05-2026',0),
(8,1,'T-shirts','Clothes',400,'03-05-2026','07-05-2026',1),
(9,3,'Samsung smart phone','Electronics',700,'09-05-2026','11-05-2026',0),
(10,4,'Lenovo Laptop','Electronics','800','12-05-2026','17-05-2026',1),
(11,5,'Lipstick','Beauty Products',79,'24-05-2026','25-05-2026',0),
(12,7,'Suit Dupatta','Clothes',100,'13-05-2026','15-05-2026',0),
(13,2,'Lakme Kajal','Beauty Products',100,'15-05-2026','16-05-2026',1),
(14,6,'Redmi TV','Electronics',300,'02-03-2026','06-03-2026',0),
(15,7,'Saree','Clothes',20,'06-05-2026','08-05-2026',0)
""")

cursor.execute("""
Select * from orders
""")

rows=cursor.fetchall()
result=[(row) for row in rows]
print(result)

conn.commit()

conn.close()