import sqlite3
from fastmcp import FastMCP
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "expense.db")

mcp = FastMCP(name="expense_mcp")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           description TEXT NOT NULL,
                       amount REAL NOT NULL,
                       category TEXT NOT NULL,
                       date TEXT NOT NULL)''')
    conn.commit()

init_db()


@mcp.tool
def add_expense(description: str, amount: float, category: str, date: str) -> str:
    """Add a new expense to the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO expenses (description, amount, category, date)
                          VALUES (?, ?, ?, ?)''', (description, amount, category, date))
    conn.commit()
    return "Expense added successfully!"

@mcp.tool
def summarize_expenses() -> list:
    """Retrieve all expenses from the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM expenses''')
        expenses = cursor.fetchall()
    return expenses

@mcp.tool
def get_expense_for_duration(init_date, final_date):
    """Retrieve data for a specific duration"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
SELECT * FROM expenses
WHERE date BETWEEN ? AND ?
''', (init_date, final_date))
        expenses = cursor.fetchall()
    return expenses


def main() -> None:
    mcp.run(transport="http", host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()



