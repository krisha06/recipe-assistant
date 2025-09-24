import sqlite3

DB_PATH = "recipes.db"

def create_db():
    import os
    conn = sqlite3.connect(DB_PATH)
    print(f"Creating DB at {os.path.abspath(DB_PATH)}")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            ingredients TEXT,
            instructions TEXT,
            cooking_time TEXT,
            diet TEXT,
            source_url TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_recipe(recipe_dict, source_url=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recipes (title, ingredients, instructions, cooking_time, diet, source_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        recipe_dict.get("title"),
        recipe_dict.get("ingredients"),
        recipe_dict.get("instructions"),
        recipe_dict.get("cooking_time"),
        recipe_dict.get("diet"),
        source_url
    ))
    conn.commit()
    conn.close()