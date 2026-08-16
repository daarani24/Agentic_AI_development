import sqlite3

DATABASE="database/sample.db"

def create_database():
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    marks INTEGER NOT NULL
    )
    """)

    students=[
        (1,"Ram","AI&DS",92),
        (2,"Durga","CSE",85),
        (3,"Shiva","AI&DS",96),
        (4,"Seeta","ECE",88),
        (5,"Karthik","CSE",68)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO students
        (id, name, department, marks)
        VALUES (?,?,?,?)
    """,students)

    connection.commit()
    connection.close()

    print("Database created successfully.")
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    create_database()