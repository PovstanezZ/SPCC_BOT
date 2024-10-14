import sqlite3
import os

dbPath = os.path.join('D:','\SPCC_BOT','DataBase', 'PCBuild.db')
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS builds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        cpu TEXT,
        gpu TEXT,
        ram TEXT,
        storage TEXT,
        budget INTEGER,
        usage TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component_type TEXT NOT NULL,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        usage TEXT NOT NULL
    )
''')

components_data = [
    # CPU - процессоры
    ('CPU', 'Intel Core i9-11900K', 45000, 'игры'),
    ('CPU', 'AMD Ryzen 9 5900X', 40000, 'игры'),
    ('CPU', 'Intel Core i7-11700K', 35000, 'игры'),
    ('CPU', 'AMD Ryzen 7 5800X', 30000, 'игры'),
    ('CPU', 'Intel Core i5-11600K', 25000, 'игры'),
    ('CPU', 'AMD Ryzen 9 5950X', 60000, 'графика'),
    ('CPU', 'Intel Core i9-12900K', 50000, 'графика'),
    ('CPU', 'AMD Ryzen 7 5700G', 30000, 'графика'),
    ('CPU', 'Intel Core i7-12700K', 40000, 'графика'),
    ('CPU', 'AMD Ryzen 5 5600G', 20000, 'графика'),
    ('CPU', 'Intel Core i5-10400F', 15000, 'офис'),
    ('CPU', 'AMD Ryzen 5 3500', 13000, 'офис'),
    ('CPU', 'Intel Core i3-10100', 10000, 'офис'),
    ('CPU', 'AMD Athlon 3000G', 6000, 'офис'),
    ('CPU', 'Intel Pentium Gold G6400', 5000, 'офис'),
    ('CPU', 'Intel Core i5-12400', 20000, 'универсальный'),
    ('CPU', 'AMD Ryzen 5 5600X', 23000, 'универсальный'),
    ('CPU', 'Intel Core i3-12100', 12000, 'универсальный'),
    ('CPU', 'AMD Ryzen 3 3100', 10000, 'универсальный'),
    ('CPU', 'Intel Core i7-10700', 30000, 'универсальный'),
    ('CPU', 'Intel Celeron G5905', 3000, 'бюджет'),
    ('CPU', 'AMD A6-9500', 3500, 'бюджет'),
    ('CPU', 'Intel Pentium G4560', 4500, 'бюджет'),
    ('CPU', 'AMD Ryzen 3 1200', 8000, 'бюджет'),
    ('CPU', 'Intel Core i3-9100F', 9000, 'бюджет'),

    # GPU - видеокарты
    ('GPU', 'NVIDIA GeForce RTX 3090', 150000, 'игры'),
    ('GPU', 'NVIDIA GeForce RTX 3080', 100000, 'игры'),
    ('GPU', 'AMD Radeon RX 6800 XT', 90000, 'игры'),
    ('GPU', 'NVIDIA GeForce RTX 3070', 70000, 'игры'),
    ('GPU', 'AMD Radeon RX 6700 XT', 50000, 'игры'),
    ('GPU', 'NVIDIA Quadro RTX 5000', 200000, 'графика'),
    ('GPU', 'AMD Radeon Pro VII', 160000, 'графика'),
    ('GPU', 'NVIDIA Quadro P2200', 90000, 'графика'),
    ('GPU', 'AMD FirePro W9100', 180000, 'графика'),
    ('GPU', 'NVIDIA GeForce RTX 2080 Ti', 80000, 'графика'),
    ('GPU', 'NVIDIA GeForce GTX 1650', 20000, 'офис'),
    ('GPU', 'AMD Radeon RX 550', 10000, 'офис'),
    ('GPU', 'NVIDIA GeForce GT 1030', 8000, 'офис'),
    ('GPU', 'AMD Radeon Vega 8', 0, 'офис'),
    ('GPU', 'Intel UHD Graphics 630', 0, 'офис'),
    ('GPU', 'NVIDIA GeForce RTX 3060', 40000, 'универсальный'),
    ('GPU', 'AMD Radeon RX 6600', 35000, 'универсальный'),
    ('GPU', 'NVIDIA GeForce GTX 1660 Super', 30000, 'универсальный'),
    ('GPU', 'AMD Radeon RX 5600 XT', 25000, 'универсальный'),
    ('GPU', 'NVIDIA GeForce GTX 1060', 20000, 'универсальный'),
    ('GPU', 'NVIDIA GeForce GT 710', 4000, 'бюджет'),
    ('GPU', 'AMD Radeon R5 230', 3000, 'бюджет'),
    ('GPU', 'NVIDIA GeForce GTX 1050 Ti', 12000, 'бюджет'),
    ('GPU', 'AMD Radeon RX 460', 7000, 'бюджет'),
    ('GPU', 'NVIDIA GeForce GTX 750 Ti', 8000, 'бюджет'),

    # RAM - оперативная память
    ('RAM', 'Corsair Vengeance LPX 16GB (2 x 8GB)', 8000, 'игры'),
    ('RAM', 'G.Skill Ripjaws V 32GB (2 x 16GB)', 16000, 'игры'),
    ('RAM', 'Kingston HyperX Fury 16GB (2 x 8GB)', 8500, 'игры'),
    ('RAM', 'Crucial Ballistix 16GB (2 x 8GB)', 9000, 'игры'),
    ('RAM', 'TeamGroup T-Force Vulcan Z 32GB (2 x 16GB)', 17000, 'игры'),
    ('RAM', 'G.Skill Trident Z Royal 64GB (2 x 32GB)', 40000, 'графика'),
    ('RAM', 'Corsair Vengeance RGB Pro 64GB (2 x 32GB)', 38000, 'графика'),
    ('RAM', 'Kingston HyperX Predator 32GB (2 x 16GB)', 18000, 'графика'),
    ('RAM', 'Crucial Ballistix 64GB (2 x 32GB)', 35000, 'графика'),
    ('RAM', 'TeamGroup T-Force Delta RGB 32GB (2 x 16GB)', 20000, 'графика'),
    ('RAM', 'Corsair ValueSelect 8GB (1 x 8GB)', 4000, 'офис'),
    ('RAM', 'Kingston KVR 8GB (1 x 8GB)', 3800, 'офис'),
    ('RAM', 'TeamGroup Elite 8GB (1 x 8GB)', 3500, 'офис'),
    ('RAM', 'Crucial Basics 8GB (1 x 8GB)', 3300, 'офис'),
    ('RAM', 'ADATA Premier 4GB (1 x 4GB)', 2000, 'офис'),
    ('RAM', 'Corsair Vengeance LPX 32GB (2 x 16GB)', 16000, 'универсальный'),
    ('RAM', 'G.Skill Ripjaws V 16GB (2 x 8GB)', 9000, 'универсальный'),
    ('RAM', 'Kingston Fury 32GB (2 x 16GB)', 15000, 'универсальный'),
    ('RAM', 'TeamGroup T-Force Dark 16GB (2 x 8GB)', 8500, 'универсальный'),
    ('RAM', 'Crucial Ballistix 32GB (2 x 16GB)', 14000, 'универсальный'),
    ('RAM', 'TeamGroup Elite 4GB (1 x 4GB)', 1800, 'бюджет'),
    ('RAM', 'ADATA Premier 2GB (1 x 2GB)', 1000, 'бюджет'),
    ('RAM', 'Kingston KVR 4GB (1 x 4GB)', 1500, 'бюджет'),
    ('RAM', 'Crucial Basics 4GB (1 x 4GB)', 1300, 'бюджет'),
    ('RAM', 'TeamGroup Elite 2GB (1 x 2GB)', 900, 'бюджет'),

    # Storage - накопители
    ('Storage', 'Samsung 970 Evo Plus 1TB NVMe SSD', 15000, 'игры'),
    ('Storage', 'Western Digital Black 1TB NVMe SSD', 14000, 'игры'),
    ('Storage', 'Crucial P5 1TB NVMe SSD', 13000, 'игры'),
    ('Storage', 'Kingston A2000 1TB NVMe SSD', 12000, 'игры'),
    ('Storage', 'ADATA XPG SX8200 Pro 1TB NVMe SSD', 11000, 'игры'),
    ('Storage', 'Samsung 980 Pro 2TB NVMe SSD', 30000, 'графика'),
    ('Storage', 'Western Digital Black 2TB NVMe SSD', 28000, 'графика'),
    ('Storage', 'Crucial P5 Plus 2TB NVMe SSD', 27000, 'графика'),
    ('Storage', 'Kingston KC2500 2TB NVMe SSD', 25000, 'графика'),
    ('Storage', 'Sabrent Rocket 4TB NVMe SSD', 40000, 'графика'),
    ('Storage', 'Kingston A400 240GB SSD', 3000, 'офис'),
    ('Storage', 'Crucial BX500 240GB SSD', 2500, 'офис'),
    ('Storage', 'Western Digital Blue 500GB SSD', 4000, 'офис'),
    ('Storage', 'ADATA SU650 240GB SSD', 2800, 'офис'),
    ('Storage', 'Samsung 860 Evo 500GB SSD', 5000, 'офис'),
    ('Storage', 'Samsung 970 Evo Plus 500GB NVMe SSD', 8000, 'универсальный'),
    ('Storage', 'Crucial P5 500GB NVMe SSD', 7000, 'универсальный'),
    ('Storage', 'Western Digital Blue 1TB SSD', 6000, 'универсальный'),
    ('Storage', 'Kingston A2000 500GB NVMe SSD', 7500, 'универсальный'),
    ('Storage', 'ADATA XPG SX8200 Pro 500GB NVMe SSD', 6500, 'универсальный'),
    ('Storage', 'Western Digital Blue 1TB HDD', 3000, 'бюджет'),
    ('Storage', 'Seagate Barracuda 1TB HDD', 3500, 'бюджет'),
    ('Storage', 'Toshiba P300 1TB HDD', 3200, 'бюджет'),
    ('Storage', 'Western Digital Green 240GB SSD', 2000, 'бюджет'),
    ('Storage', 'Crucial BX500 120GB SSD', 1500, 'бюджет')
]

cursor.executemany('''
    INSERT INTO components (component_type, name, price, usage) 
    VALUES (?, ?, ?, ?)
''', components_data)

conn.commit()
conn.close()

print(f'База данных создана по пути: {dbPath}')