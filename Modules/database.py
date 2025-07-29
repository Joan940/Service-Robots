import mysql.connector

import mysql.connector

# Fungsi untuk menghubungkan ke database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kipaza",
        database="campberingin"
    )

# Fungsi untuk menambahkan pesanan
def addOrders(table_number, queue_number, item_name, quantity):
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    query = "INSERT INTO orders (table_number, queue_number, item_name, quantity) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (table_number, queue_number, item_name, quantity))
    db_connection.commit()

    cursor.close()
    db_connection.close()

# Fungsi untuk mengambil semua pesanan
def getOrders():
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    query = "SELECT * FROM orders"
    cursor.execute(query)

    orders = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return orders

