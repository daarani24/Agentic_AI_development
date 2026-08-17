import sqlite3

DATABASE="database/sample.db"

def get_database_schema():
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables=cursor.fetchall()
    schema={}

    for table in tables:
        table_name=table[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns=cursor.fetchall()

        schema[table_name]=[
            {
                "name":column[1],
                "type":column[2]
            }
            for column in columns
        ]

    connection.close()
    return schema

def execute_sql(query):
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()

    try:
        cursor.execute(query)
        results=cursor.fetchall()
        connection.close()
        return{
            "success":True,
            "results":results
        }
    
    except sqlite3.Error as error:
        connection.close()
        return{
            "success":False,
            "error":str(error)
        }

if __name__=="__main__":
    print("Database schema:")
    print(get_database_schema())

    print("\nValid SQL:")
    print(execute_sql("SELECT * FROM students"))

    print("\nInvalid SQL:")
    print(execute_sql("SELECT * FROM students WHERE score > 80"))
