import tkinter as tk
from taskscheduler.ui import TaskSchedulerApp

def main():
    root = tk.Tk()
    app = TaskSchedulerApp(root)
    root.mainloop()

main()
