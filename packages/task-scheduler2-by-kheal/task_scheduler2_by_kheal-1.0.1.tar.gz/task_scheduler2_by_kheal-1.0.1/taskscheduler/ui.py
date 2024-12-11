import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import calendar
import time
from taskscheduler.utils import TaskHistory

class TaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")
        self.root.geometry("915x780")
        self.root.resizable(False, False)

        self.Username = StringVar(value="")
        self.getbio = StringVar(value="")
        self.greeting = StringVar(value="Hi! Welcome to your task scheduler!")
        self.bio = StringVar(value="bio") 
        self.address = StringVar(value="")
        self.cnum = StringVar(value="")

        self.tasks = []
        self.history = TaskHistory()

        self.init_ui()

    def init_ui(self):
        # Top frame
        tframe = tk.Frame(self.root, bg="deep sky blue", height=60)
        tframe.pack(side="top", fill="x")
        tk.Label(
            tframe,
            textvariable=self.greeting,
            font=("Times New Roman", 20, "bold"),
            bg="deep sky blue",
        ).pack(anchor="n", pady=8)

        tk.Label(
            tframe,
            textvariable=self.bio,
            font=("Times New Roman", 14),
            bg="deep sky blue",
        ).pack(anchor="center")
    
    
        self.account = tk.Button(tframe, 
                                 text="Add Account", 
                                 font=("Times New Roman", 12, "bold"),
                                 height=1,
                                 width=10,
                                 command=self.sign_up,
                                 cursor="hand2").pack(side=RIGHT, anchor="s", pady=5, padx=5)
        
        self.time_label = tk.Label(tframe, font=("Times New Roman", 14), bg="deep sky blue")
        self.time_label.pack(side=RIGHT, anchor="s", padx=250)
        self.update_time()

        # Parent frame
        parentframe = tk.Frame(self.root)
        parentframe.pack(fill="both", expand=True)

        # Left frame
        self.init_left_frame(parentframe)
        
        # Right frame
        self.init_right_frame(parentframe)

    def sign_up(self):
        nwindow = Toplevel()
        nwindow.title("Sign Up An Account")
        nwindow.geometry("300x300")
        nwindow.resizable(False, False)

        nframe = tk.Frame(nwindow)
        nframe.pack(side="left",fill="both")

        tk.Label(nframe, text="Enter Username:", font=("Times New Roman", 12)).grid(row=0, column=0, pady=5, padx=5)
        tk.Entry(nframe, font=("Times New Roman", 12), width=20, textvariable=self.Username).grid(row=0, column=1, pady=5)

        tk.Label(nframe, text="Enter Address:   ", font=("Times New Roman", 12)).grid(row=1, column=0, pady=5, padx=5)
        tk.Entry(nframe, font=("Times New Roman", 12), width=20, textvariable=self.address).grid(row=1, column=1, columnspan=2, pady=5)

        tk.Label(nframe, text="Contact Number:   ", font=("Times New Roman", 12)).grid(row=2, column=0, pady=5, padx=5)
        tk.Entry(nframe, font=("Times New Roman", 12), width=20, textvariable=self.cnum).grid(row=2, column=1, columnspan=2, pady=5)

        tk.Label(nframe, text="BIO", font=("Times New Roman", 12)).grid(row=3, column=0, columnspan=2, pady=5)
        bio_text = tk.Text(nframe, font=("Times New Roman", 12), width=30, height=6)
        bio_text.grid(row=5, column=0, columnspan=2, rowspan=5, padx=5)

        tk.Button(
            nframe,
            text="Save",
            font=("Times New Roman", 12),
            command=lambda: self.update_greeting_bio(nwindow, bio_text),
        ).grid(row=10, column=0, columnspan=2, pady=10)

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

        # Calendar
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

        # Task history
        tk.Label(
            blframe,
            text="Your Task History",
            font=("Times New Roman", 15, "bold"),
            bg="ivory3",
        ).grid(row=4, column=0, columnspan=4, sticky="nesw")
        history = tk.Frame(blframe, bg="ivory3")
        history.grid(row=5, column=0, columnspan=4, sticky="nesw")
        self.Htree = ttk.Treeview(history, columns=("Action", "Task", "Date/Time Stamp"), show="headings", height=11)
        self.Htree.heading("Action", text="Action")
        self.Htree.heading("Task", text="Task")
        self.Htree.heading("Date/Time Stamp", text="Date/Time Stamp")
        self.Htree.column("Action", width=200, anchor="w")
        self.Htree.column("Task", width=100, anchor="center")
        self.Htree.column("Date/Time Stamp", width=100, anchor="center")
        self.Htree.pack(padx=10, pady=8, fill="both")

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

        # Popup menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Delete", command=self.delete_task)
        self.menu.add_command(label="Modify", command=self.modify_task)
        self.Ttree.bind("<Button-3>", self.show_menu)

