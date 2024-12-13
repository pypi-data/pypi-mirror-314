# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
import tkinter as tk
from tkinter import messagebox
from time import sleep
from threading import Thread
from rpio.utils.constants import *
from rpio.logging.logger import *

class Executer_GUI:

    STATUS_COLORS = {
        StepStatus.PENDING: "#a9a9a9",
        StepStatus.RUNNING: "#1e90ff",
        StepStatus.PASSED: "#32cd32",
        StepStatus.FAILED: "#ff6347"
    }
    STATUS_ICONS = {
        StepStatus.PENDING: "●",  # Grayed-out dot
        StepStatus.RUNNING: "⏳",  # Hourglass for running
        StepStatus.PASSED: "✔️",   # Checkmark for passed
        StepStatus.FAILED: "❌"    # Cross for failed
    }

    def __init__(self, tasks,name):
        self.logger = Logger(name="Custom logger", path="../", verbose=False)
        self.name = name
        self.tasks = tasks
        self.root = tk.Tk()
        self.root.title("Workflow "+name+" Status")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e1e")  # Dark background for a polished look
        self.task_widgets = {}
        self.create_gui()

    def create_gui(self):
        title = tk.Label(self.root, text="Workflow "+self.name+" Status", font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="white")
        title.pack(pady=10)

        self.status_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.status_frame.pack(pady=5, fill="x")

        for task_name in self.tasks:
            self.add_task(task_name)

        self.start_button = tk.Button(
            self.root,
            text="Start Workflow",
            command=self.start_workflow,
            font=("Arial", 12, "bold"),
            bg="#1e90ff",
            fg="white",
            bd=0,
            padx=10,
            pady=5
        )
        self.start_button.pack(pady=20)

    def add_task(self, task_name):
        # Task label with status icon
        task_label = tk.Label(
            self.status_frame,
            text=f"{self.STATUS_ICONS[StepStatus.PENDING]} {task_name}",
            font=("Arial", 12),
            fg=self.STATUS_COLORS[StepStatus.PENDING],
            bg="#1e1e1e",
            anchor="w",
            padx=10,
            pady=5
        )
        task_label.pack(fill="x", pady=2)

        # Store task label for updating later
        self.task_widgets[task_name] = task_label

    def start_workflow(self):
        self.start_button.config(state=tk.DISABLED)
        self.logger.syslog(msg="Workflow --"+self.name+"-- started")
        Thread(target=self.run_tasks).start()

    def run_tasks(self):
        for task_name, func in self.tasks.items():
            self.update_status(task_name, StepStatus.RUNNING)
            try:
                result = func()
                if result:
                    self.update_status(task_name, StepStatus.PASSED)
                    self.logger.syslog(msg="Task <<" + task_name + ">> successfully completed")
                else:
                    self.update_status(task_name, StepStatus.FAILED)
                    self.logger.syslog(msg="Task <<" + task_name + ">> failed to complete")
            except Exception as e:
                self.update_status(task_name, StepStatus.FAILED)
                messagebox.showerror("Error", f"Task '{task_name}' failed with error: {e}")
                break
            sleep(1)  # Simulate delay between checks

        self.start_button.config(state=tk.NORMAL)

    def update_status(self, task_name, status):
        label = self.task_widgets[task_name]
        label.config(
            text=f"{self.STATUS_ICONS[status]} {task_name}",
            fg=self.STATUS_COLORS[status]
        )
        label.update()

class Executer_headless:

    def __init__(self, tasks,name):
        self.tasks = tasks
        self.name = name
        self.logger = Logger(name="Custom logger", path="../", verbose=False)


    def start_workflow(self):
        self.logger.syslog(msg="Workflow " + self.name + " started")
        Thread(target=self.run_tasks).start()

    def run_tasks(self):
        for task_name, func in self.tasks.items():
            try:
                result = func()
                if result:
                    print("Task '{}' succeeded".format(task_name))
                    self.logger.syslog(msg="Task <<" + task_name + ">> successfully completed")
                else:
                    print("Task '{}' failed".format(task_name))
                    self.logger.syslog(msg="Task <<" + task_name + ">> failed to complete")
            except Exception as e:
                print("Error", f"Task '{task_name}' failed with error: {e}")
                break
            sleep(1)  # Simulate delay between checks