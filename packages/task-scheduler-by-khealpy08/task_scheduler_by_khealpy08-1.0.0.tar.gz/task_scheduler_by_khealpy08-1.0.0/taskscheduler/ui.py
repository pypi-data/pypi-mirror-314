import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime

class TaskSchedulerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")
        self.root.geometry("930x780")

        self.tasks = []
        self.history = None

        self.init_ui()

    def init_ui(self):
        # Top frame
        tframe = tk.Frame(self.root, bg="deep sky blue", height=60)
        tframe.pack(side="top", fill="x")
        tk.Label(
            tframe,
            text="Welcome To Task Scheduler!",
            font=("Times New Roman", 20, "bold"),
            bg="deep sky blue",
        ).pack(pady=10)

        self.time_label = tk.Label(tframe, font=("Times New Roman", 14), bg="deep sky blue")
        self.time_label.pack()
        self.update_time()

        # Parent frame
        parentframe = tk.Frame(self.root)
        parentframe.pack(fill="both", expand=True)

        # Left frame
        self.init_left_frame(parentframe)

        # Right frame
        self.init_right_frame(parentframe)

    def init_left_frame(self, parentframe):
        blframe = tk.Frame(parentframe, bg="ivory4", width=375)
        blframe.pack(side="left", fill="both", expand=True)

        self.task_description_var = tk.StringVar()
        self.task_time_var = tk.StringVar()
        self.task_date_var = tk.StringVar()

        tk.Label(
            blframe,
            text="   Task Description:   ",
            font=("Times New Roman", 13, "bold"),
            bg="ivory4",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(blframe, width=30, textvariable=self.task_description_var).grid(row=0, column=2, sticky="ew")
        tk.Label(
            blframe,
            text="Task Time (HH:MM):",
            font=("Times New Roman", 13, "bold"),
            bg="ivory4",
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(blframe, width=30, textvariable=self.task_time_var).grid(row=1, column=2, sticky="ew")
        tk.Label(
            blframe,
            text="Task Date (MM:DD):",
            font=("Times New Roman", 13, "bold"),
            bg="ivory4",
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(blframe, width=30, textvariable=self.task_date_var).grid(row=2, column=2, sticky="ew")
        tk.Button(
            blframe,
            text="Add Task",
            font=("Times New Roman", 13, "bold"),
            height=3,
            width=8,
            cursor="hand2",
            command=self.add_task,
        ).grid(row=0, column=3, padx=10, pady=5, rowspan=3)

        calendar_frame = tk.Frame(blframe, bg="ivory4")
        calendar_frame.grid(row=3, column=0, columnspan=4, sticky="ew")
        self.calendar = Calendar(
            calendar_frame,
            selectmode="day",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            font=("Times New Roman", 15),
        )
        self.calendar.pack(padx=5, pady=5)

    def init_right_frame(self, parentframe):
        brframe = tk.Frame(parentframe, bg="ivory4", width=375)
        brframe.pack(side="right", fill="both", expand=True)
        tk.Label(
            brframe,
            text="Task Scheduled",
            font=("Times New Roman", 15, "bold"),
            bg="ivory4",
        ).grid(row=0, column=0, padx=150, pady=5, sticky="w")
        self.Ttree = ttk.Treeview(brframe, columns=("Task", "Time", "Date"), show="headings", height=30)
        self.Ttree.heading("Task", text="Task")
        self.Ttree.heading("Time", text="Time")
        self.Ttree.heading("Date", text="Date")
        self.Ttree.column("Task", width=200, anchor="w")
        self.Ttree.column("Time", width=100, anchor="center")
        self.Ttree.column("Date", width=100, anchor="center")
        self.Ttree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def update_time(self):
        import time

        current_time = time.strftime("%H:%M:%S %p")
        self.time_label.config(text=f"Current Time: {current_time}")
        self.time_label.after(1000, self.update_time)
