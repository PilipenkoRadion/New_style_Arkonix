import sqlite3


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # ---------- Пользователи ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'client' -- client, staff, admin
    )
    """)

    # ---------- Отзывы ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------- Заявки клиентов ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        service TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'new',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # ---------- Чаты ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        staff_id INTEGER,
        service_name TEXT,
        status TEXT DEFAULT 'waiting', -- waiting, in_progress, finished
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES users(id),
        FOREIGN KEY (staff_id) REFERENCES users(id)
    )
    """)

    # ---------- Сообщения ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        sender_id INTEGER,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chat_id) REFERENCES chats(id),
        FOREIGN KEY (sender_id) REFERENCES users(id)
    )
    """)

    # ---------- СОЗДАНИЕ ТЕСТОВЫХ ПОЛЬЗОВАТЕЛЕЙ ----------
    print("\n🔧 Создание тестовых пользователей...")

    # Админ
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role) 
            VALUES ('admin', 'admin123', 'admin')
        """)
        print("✅ Создан АДМИН: username='admin', password='admin123'")
    except sqlite3.IntegrityError:
        print("ℹ️  Админ уже существует")

    # Сотрудник
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role) 
            VALUES ('staff', 'staff123', 'staff')
        """)
        print("✅ Создан СОТРУДНИК: username='staff', password='staff123'")
    except sqlite3.IntegrityError:
        print("ℹ️  Сотрудник уже существует")

    # Тестовый клиент
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role) 
            VALUES ('client', 'client123', 'client')
        """)
        print("✅ Создан КЛИЕНТ (для теста): username='client', password='client123'")
    except sqlite3.IntegrityError:
        print("ℹ️  Клиент уже существует")

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print("✅ База данных успешно инициализирована!")
    print("📋 Созданы таблицы: users, reviews, requests, chats, messages")
    print("=" * 60)
    print("\n👥 АККАУНТЫ ДЛЯ ВХОДА:")
    print("   🛡️  АДМИН:     username='admin'  password='admin123'")
    print("   👔 СОТРУДНИК: username='staff'  password='staff123'")
    print("   👤 КЛИЕНТ:    username='client' password='client123'")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    init_db()
