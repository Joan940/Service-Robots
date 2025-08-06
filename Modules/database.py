import mysql.connector
import Modules.varGlobals as varGlobals

from Modules.colors import (
    custom as cc,
    tts,
    tts2
)


###################################################################################################
#                                       CONNECT TO DATABASE                                       #
###################################################################################################

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",          # Ganti dengan username database Anda
            password = "kipaza",    # Ganti dengan password database Anda
            database = "campberingin"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    

###################################################################################################
#                                          RESET DATABASE                                         #
###################################################################################################

def reset_database():

    print("Mereset database...")
    
    db_connection = connect_to_db()
    if db_connection is None:
        return

    cursor = db_connection.cursor()

    try:
        # Perintah untuk menghapus database jika ada
        cursor.execute("DROP DATABASE IF EXISTS campberingin")
        print("Database campberingin berhasil dihapus (jika ada).")
        
        # Perintah untuk membuat database baru
        cursor.execute("CREATE DATABASE campberingin")
        print("Database campberingin berhasil dibuat.")
        
        # Ganti ke database yang baru dibuat
        cursor.execute("USE campberingin")

        # Perintah untuk membuat tabel orders
        create_table_query = """
        CREATE TABLE orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            table_number INT NOT NULL,
            queue_number INT NOT NULL,
            item_name VARCHAR(255) NOT NULL,
            quantity INT DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        print("Tabel 'orders' berhasil dibuat.")

    except mysql.connector.Error as err:
        print(f"Terjadi error saat mereset database: {err}")
    finally:
        cursor.close()
        db_connection.close()
        print("Reset database selesai.")


###################################################################################################
#                                        MENAMBAH PESANAN                                         #
###################################################################################################
def addOrders(table_number, queue_number, item_name, quantity):
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    query = "INSERT INTO orders (table_number, queue_number, item_name, quantity) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (table_number, queue_number, item_name, quantity))
    db_connection.commit()

    cursor.close()
    db_connection.close()


###################################################################################################
#                                      MENGAMBIL DATA PESANAN                                     #
###################################################################################################
    
def getOrders():
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    query = "SELECT * FROM orders ORDER BY id DESC LIMIT 5"
    cursor.execute(query)

    orders = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return orders