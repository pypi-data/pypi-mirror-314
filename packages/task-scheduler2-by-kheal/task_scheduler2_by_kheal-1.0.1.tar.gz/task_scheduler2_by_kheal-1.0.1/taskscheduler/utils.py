import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import calendar
import time

class TaskBase:
    def __init__(self):
        self.task_description = ""
        self.task_time = ""
        self.task_date = ""

    def validate_time(self, time_string):
        try:
            hour, minute = map(int, time_string.split(":"))
            return 0 <= hour <= 24 and 0 <= minute <= 60
        except ValueError:
            return False

    def validate_date(self, date_string):
        try:
            month, day = map(int, date_string.split(":"))
            return 1 <= month <= 12 and 1 <= day <= 31
        except ValueError:
            return False
    
    def update_time(self):
        current_time = time.strftime("%H:%M:%S %p")
        self.time_label.config(text=f"Current Time: {current_time}")
        self.time_label.after(1000, self.update_time)

    def add_task(self):
        task_desc = self.task_description_var.get()
        task_time = self.task_time_var.get()
        task_date = self.task_date_var.get()

        if not task_desc:
            messagebox.showerror("Error", "Task description cannot be empty.")
            return

        if not TaskBase().validate_time(task_time):
            messagebox.showerror("Error", "Invalid time format. Use HH:MM (24-hour format).")
            return

        if not TaskBase().validate_date(task_date):
            messagebox.showerror("Error", "Invalid date format. Use MM:DD.")
            return

        task = Task(task_desc, task_time, task_date)
        self.tasks.append(task)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add to Scheduled Treeview
        self.Ttree.insert("", tk.END, values=(task.task_description, task.task_time, task.task_date))

        # Record the action in the History Treeview
        self.Htree.insert("", tk.END, values=("Added", task.task_description, timestamp))
        self.history.add_history("Added", task.task_description, timestamp)

        # Clear the entry fields
        self.task_description_var.set("")
        self.task_time_var.set("")
        self.task_date_var.set("")

    def update_greeting_bio(self, nwindow, bio_text):
        username = self.Username.get()
        bio = bio_text.get("1.0", "end").strip()

        if username:
            self.greeting.set(f"Hi! {username}, welcome to your task scheduler!")

        self.bio.set(bio if bio else " ")
        nwindow.destroy()

    def show_menu(self, event):
        selected_item = self.Ttree.identify_row(event.y)
        if selected_item:
            self.Ttree.selection_set(selected_item)
            self.menu.post(event.x_root, event.y_root)

    def delete_task(self):
        selected_item = self.Ttree.selection()
        if selected_item:
            task_values = self.Ttree.item(selected_item, "values")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Record the action in the History Treeview
            self.Htree.insert("", tk.END, values=("Deleted", task_values[0], timestamp))
            self.history.add_history("Deleted", task_values[0], timestamp)

            # Delete from Scheduled Treeview
            self.Ttree.delete(selected_item)

    def modify_task(self):
        selected_item = self.Ttree.selection()
        if selected_item:
            task_values = self.Ttree.item(selected_item, "values")
            self.task_description_var.set(task_values[0])
            self.task_time_var.set(task_values[1])
            self.task_date_var.set(task_values[2])

            # Record the action in the History Treeview
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.Htree.insert("", tk.END, values=("Modified", task_values[0], timestamp))
            self.history.add_history("Modified", task_values[0], timestamp)

            # Delete the original item
            self.Ttree.delete(selected_item)

class Task(TaskBase):
    def __init__(self, description, time, date):
        super().__init__()
        self.task_description = description
        self.task_time = time
        self.task_date = date

class TaskHistory:
    def __init__(self):
        self.history = []

    def add_history(self, action, task, timestamp):
        self.history.append((action, task, timestamp))

    def get_history(self):
        return self.history
