import psycopg2
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from datetime import datetime


#Nawiazywanie polaczenia z baza danych
connection = psycopg2.connect (host = DB_HOST, user = DB_USER, password = DB_PASSWORD, dbname = DB_NAME)
cursor = connection.cursor ()

#Tworzenie tabeli tasks - funkcja
def create_table ():
    cursor.execute ("""CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    due_date DATE NOT NULL); """)
    connection.commit ()

#Funkcja do obslugi bazy danych (dodaje nowe zadanie do bazy danych)
def add_task (title, content, due_date):  
    if not due_date:
        due_date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute ("""INSERT INTO tasks (title, content, due_date)
                    VALUES (%s, %s, %s) """, (title, content, due_date))

    connection.commit ()

#Aktualizacja zadania
def update_task (task_id, title, content, due_date):
    if not due_date:
        due_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute ("UPDATE tasks SET title = %s, content = %s, due_date = %s WHERE id= %s;", 
                    (title, content, due_date, task_id))
    
    connection.commit ()

#Kasowanie zadania
def delete_task (task_id):
    cursor.execute ("DELETE FROM tasks WHERE id= %s;", (task_id,))
    connection.commit ()

#Wczytanie listy zadan
def load_tasks ():
    cursor.execute ("SELECT * FROM tasks")
    return cursor.fetchall ()