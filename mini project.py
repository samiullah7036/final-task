
import mysql.connector
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="S@miullah7036",
    port=3306,
    database="expense_manager"
)

print("Connection Successful...!")  
from abc import ABC, abstractmethod
import mysql.connector
from functools import reduce

# CREATE CURSOR
cursor = conn.cursor()

# ---------------- ABSTRACT CLASS ----------------
class Person(ABC):
    def __init__(self, name):
        self._name = name

    @abstractmethod
    def display(self):
        pass

# ---------------- USER CLASS ----------------
class User(Person):
     def __init__(self, name):
        super().__init__(name)

     def create_user(self):
        query = "INSERT INTO users (name) VALUES (%s)"
        cursor.execute(query, (self._name,))
        conn.commit()
        return cursor.lastrowid   # auto ID

     def display(self):
        print(f"User: {self._name}")

# ---------------- EXPENSE CLASS ----------------
class Expense(User):
    def __init__(self, name, user_id):
        super().__init__(name)
        self.__user_id = user_id

    def add_expense(self, amount, category, description, date):
        query = """
        INSERT INTO expenses (user_id, amount, category, description, date)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.__user_id, amount, category, description, date))
        conn.commit()

    def view_expenses(self):
        query = """
        SELECT users.name, expenses.amount, expenses.category, expenses.date
        FROM expenses
        JOIN users ON users.user_id = expenses.user_id
        WHERE users.user_id = %s
        """
        cursor.execute(query, (self.__user_id,))
        for row in cursor.fetchall():
            print(row)

    def total_expense(self):
        cursor.execute("SELECT amount FROM expenses WHERE user_id = %s", (self.__user_id,))
        data = cursor.fetchall()
        amounts = list(map(lambda x: x[0], data))
        total = reduce(lambda x, y: x + y, amounts, 0)
        print("Total:", total)

    def highest_expense(self):
        cursor.execute("SELECT amount FROM expenses WHERE user_id = %s", (self.__user_id,))
        data = cursor.fetchall()
        amounts = list(map(lambda x: x[0], data))
        highest = reduce(lambda x, y: x if x > y else y, amounts)
        print("Highest:", highest)

    def smart_insight(self):
        cursor.execute("SELECT category, amount FROM expenses WHERE user_id = %s", (self.__user_id,))
        data = cursor.fetchall()

        total = 0
        category_sum = {}

        for cat, amt in data:
            total += amt
            category_sum[cat] = category_sum.get(cat, 0) + amt

        for cat, amt in category_sum.items():
            if amt > total * 0.4:
                print(f"⚠️ Too much spending on {cat}")

# ---------------- MAIN ----------------
u = User("Sai")
uid = u.create_user()

exp = Expense("Sai", uid)

exp.add_expense(500, "Food", "Lunch", "2026-04-06")
exp.add_expense(2000, "Shopping", "Clothes", "2026-04-06")

exp.display()
exp.view_expenses()
exp.total_expense()
exp.highest_expense()
exp.smart_insight()

conn.close()