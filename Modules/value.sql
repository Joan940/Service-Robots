DROP DATABASE IF EXISTS campberingin;
CREATE DATABASE campberingin;
USE campberingin;

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL,       -- Nomor meja
    queue_number INT NOT NULL,       -- Nomor antrian
    item_name VARCHAR(255) NOT NULL, -- Nama item
    quantity INT DEFAULT 1,          -- Jumlah item
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan pesanan
);