import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def calculate_tipi(population, signal_strength, distance, internet_users, complaints, fiber, network_type):
    # Sub-scores
    s_pop = min(population / 50000.0, 1.0) * 100.0
    s_sig = (1.0 - (signal_strength - 1) / 4.0) * 100.0
    s_dist = min(distance / 10.0, 1.0) * 100.0
    
    net_scores = {"2G": 100.0, "3G": 75.0, "4G": 40.0, "5G": 10.0}
    s_net = net_scores.get(network_type, 10.0)
    
    s_comp = min(complaints / 100.0, 1.0) * 100.0
    s_user = float(internet_users)
    s_fib = 100.0 if fiber.strip().lower() == "no" else 0.0
    
    # Weights
    w_sig = 0.20
    w_comp = 0.20
    w_pop = 0.15
    w_dist = 0.15
    w_net = 0.15
    w_fib = 0.10
    w_user = 0.05
    
    score = (w_pop * s_pop + 
             w_sig * s_sig + 
             w_dist * s_dist + 
             w_net * s_net + 
             w_comp * s_comp + 
             w_user * s_user + 
             w_fib * s_fib)
    
    if score >= 75.0:
        cat = "High"
    elif score >= 45.0:
        cat = "Medium"
    else:
        cat = "Low"
        
    return round(score, 2), cat

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Create Areas Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        population INTEGER NOT NULL,
        signal_strength INTEGER NOT NULL,
        distance REAL NOT NULL,
        internet_users INTEGER NOT NULL,
        complaints INTEGER NOT NULL,
        fiber TEXT NOT NULL,
        network_type TEXT NOT NULL,
        priority_score REAL NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Insert Default Admin User if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
        print("Default admin user created: admin / admin123")
    
    # Seed Mock Areas if the table is empty
    cursor.execute("SELECT COUNT(*) FROM areas")
    count = cursor.fetchone()[0]
    if count == 0:
        mock_data = [
            ("Maharashtra East Circle - Wardha", 45000, 2, 7.5, 40, 85, "No", "3G"),
            ("Kerala South Circle - Wayanad", 12000, 1, 12.0, 30, 95, "No", "2G"),
            ("Tamil Nadu Circle - Salem Rural", 85000, 3, 4.2, 55, 60, "Yes", "4G"),
            ("Bihar Central Circle - Vaishali", 120000, 1, 9.8, 25, 150, "No", "2G"),
            ("UP East Circle - Gorakhpur Rural", 95000, 2, 8.0, 35, 110, "No", "3G"),
            ("Karnataka North Circle - Bagalkot", 38000, 4, 3.1, 70, 25, "Yes", "4G"),
            ("West Bengal Circle - Purulia", 62000, 2, 11.2, 45, 90, "No", "3G"),
            ("Gujarat Circle - Kutch Border Area", 15000, 1, 15.4, 20, 80, "No", "2G"),
            ("Rajasthan West Circle - Jaisalmer Outskirts", 8000, 2, 18.0, 15, 45, "No", "2G"),
            ("Punjab Circle - Firozpur Rural", 52000, 3, 5.0, 65, 40, "Yes", "4G"),
            ("NE-I Circle - Shillong Suburbs", 24000, 4, 6.2, 80, 20, "Yes", "5G"),
            ("Madhya Pradesh Circle - Jhabua", 78000, 1, 10.5, 30, 130, "No", "2G"),
        ]
        
        for item in mock_data:
            name, pop, sig, dist, users, comp, fib, net = item
            score, cat = calculate_tipi(pop, sig, dist, users, comp, fib, net)
            cursor.execute('''
            INSERT INTO areas (name, population, signal_strength, distance, internet_users, complaints, fiber, network_type, priority_score, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, pop, sig, dist, users, comp, fib, net, score, cat))
        print("Mock telecom circle database seeded successfully!")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
