import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .task import Task, TaskBase, TaskHistory
from .ui import TaskSchedulerUI

class TaskSchedulerApp(TaskSchedulerUI):
    def __init__(self, root):
        super().__init__(root)
        self.history = TaskHistory()

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

        self.Ttree.insert("", tk.END, values=(task.task_description, task.task_time, task.task_date))
        self.history.add_history("Added", task.task_description, timestamp)
        self.task_description_var.set("")
        self.task_time_var.set("")
        self.task_date_var.set("")

root = tk.Tk()
app = TaskSchedulerApp(root)
root.mainloop()