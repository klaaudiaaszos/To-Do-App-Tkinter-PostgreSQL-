import tkinter as tk
from tkinter import messagebox
import db


root = tk.Tk()
root.title ("Zarzadzanie zadaniami")
root.geometry ("800x400")

frame_add_task = tk.Frame (root, padx = 10, pady = 10)
frame_add_task.pack (fill = 'x')

tk.Label(frame_add_task, text = "Tytul: ").pack (side = "left")
entry_title = tk.Entry (frame_add_task)
entry_title.pack (side = "left", expand = True, fill = "x")

tk.Label(frame_add_task, text = "Tresc: ").pack (side = "left")
entry_content = tk.Entry (frame_add_task)
entry_content.pack (side = "left", expand = True, fill = "x")

tk.Label(frame_add_task, text = "Data wykonania (RRRR-MM-DD): ").pack (side = "left")
entry_due_date = tk.Entry (frame_add_task)
entry_due_date.pack (side = "left", expand = True, fill = "x")

def add_task_gui():
    db.add_task (entry_title.get(), entry_content.get(), entry_due_date.get())
    refresh_tasks()

def delete_task_gui(task_id):
    db.delete_task(task_id)
    refresh_tasks()

def update_task_gui(task_id, title, content, due_date):
    db.update_task(task_id, title, content, due_date)
    button_add_task.config(text="Dodaj", command=add_task_gui)
    refresh_tasks()

#Przyciski do dodawania nowego zadania
button_add_task = tk.Button (frame_add_task, text = "Dodaj", width = 20,
                          command = add_task_gui)
button_add_task.pack (side = "right")

frame_tasks = tk.Frame (root, bg = "white")
frame_tasks.pack (fill = "both", expand = True)

#Dodawanie zadan do GUI
def refresh_tasks():
    #Czyszczenie listy zadan w GUI
    for widget in frame_tasks.winfo_children():
        widget.destroy ()

    tasks = db.load_tasks()

    for task in tasks:
        task_frame = tk.Frame (frame_tasks, bg= "white", pady= 10)
        task_frame.pack (fill = "x")

        tk.Label(task_frame, text = f"{task[1]} (do wykonania: {task[3]})", bg= "white").pack(side = "left")
        tk.Button(task_frame, text = "Edytuj", command = lambda task=task: edit_task (task)).pack(side = "right")
        tk.Button(task_frame, text = "Usun", command = lambda task_id=task[0]: delete_task_gui (task_id)).pack(side = "right")

#Edycja zadania (wypelnia formularz danymi zadania, wybranego do edycji)
def edit_task (task):
    entry_title.delete (0, tk.END)
    entry_title.insert (0, task[1])
    entry_content.delete (0, tk.END)
    entry_content.insert (0, task[2])
    entry_due_date.delete (0, tk.END)
    entry_due_date.insert (0, str(task[3]))
    button_add_task.config (text = "Zapisz", width = 25, 
                command = lambda: update_task_gui (task[0], entry_title.get(), entry_content.get(), entry_due_date.get()))
    
#Funkcja zamykajaca polaczenie z baza danych przy zamykaniu okna
def on_closing ():
    if messagebox.askokcancel ("Quit", "Czy napewno chcesz wyjsc?"):
        db.cursor.close ()
        db.connection.close ()
        root.destroy ()

refresh_tasks()