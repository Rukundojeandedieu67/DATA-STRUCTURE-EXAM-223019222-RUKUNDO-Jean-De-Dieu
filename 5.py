import tkinter as tk
from tkinter import messagebox, ttk
import re

class Node:
    """Node class for the Doubly Linked List"""
    def __init__(self, task, plate_id):
        self.task = task
        self.plate_id = plate_id
        self.next = None
        self.prev = None

class DoublyLinkedList:
    """Doubly Linked List to manage tasks"""
    def __init__(self):
        self.head = None
        self.tail = None

    def add_task(self, task, plate_id):
        new_node = Node(task, plate_id)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove_task(self):
        if not self.head:
            return None
        removed_node = self.head
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return removed_node

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(f"{current.task} - {current.plate_id}")
            current = current.next
        return tasks

class MaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Maintenance Tracker")
        self.root.state("zoomed")
        self.root.configure(bg="#f7f7f7")

        # Predefined Task List
        self.task_options = [
            "Select an Operation",  # Default option
            "Oil Change",
            "Tire Rotation",
            "Brake Inspection",
            "Battery Check",
            "Filter Replacement",
            "Coolant Flush",
            "Alignment Check",
            "Spark Plug Replacement",
            "Timing Belt Inspection",
            "Transmission Fluid Change"
        ]

        title_label = tk.Label(root, text="Car Maintenance Tracker", font=("Helvetica", 26, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=20)

        self.plate_frame = tk.Frame(root, bg="#f7f7f7")
        self.plate_frame.pack(pady=15)

        tk.Label(self.plate_frame, text="Enter Plate ID (e.g., RAA123A for Car):", font=("Helvetica", 14), bg="#f7f7f7", fg="#333").grid(row=0, column=0, padx=10)
        self.plate_id_entry = tk.Entry(self.plate_frame, font=("Helvetica", 14), width=20, bd=2, relief="solid", highlightcolor="#4CAF50", highlightthickness=2)
        self.plate_id_entry.grid(row=0, column=1, padx=10)

        input_frame = tk.Frame(root, bg="#f7f7f7")
        input_frame.pack(pady=10)

        self.task_var = tk.StringVar()
        self.task_var.set(self.task_options[0])  # Default selection

        self.task_dropdown = ttk.Combobox(input_frame, textvariable=self.task_var, values=self.task_options, font=("Helvetica", 14), state="readonly", width=25)
        self.task_dropdown.grid(row=0, column=0, padx=5)

        add_buttons_frame = tk.Frame(input_frame, bg="#f7f7f7")
        add_buttons_frame.grid(row=0, column=1, padx=10)

        tk.Button(add_buttons_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Helvetica", 14), relief="flat", width=12, height=2).grid(row=0, column=0, padx=5, pady=5)

        tk.Label(root, text="Pending Maintenance Tasks:", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

        self.tasks_listbox = tk.Listbox(root, font=("Helvetica", 14), height=8, width=50, bd=2, relief="solid", selectmode=tk.SINGLE, bg="#f0f0f0", fg="#333")
        self.tasks_listbox.pack(pady=5)

        self.tasks_listbox.insert(tk.END, "OPERATION                PLATE ID")
        self.tasks_listbox.insert(tk.END, "-" * 50)

        tk.Button(root, text="Remove Task", command=self.remove_task, bg="#FF5722", fg="white", font=("Helvetica", 14), relief="flat", width=20, height=2).pack(pady=10)

        self.tasks = DoublyLinkedList()

        # Close button handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def validate_plate_id(self, plate_id):
        car_pattern = r"^RA[A-G]\d{3}[A-Z]$"
        if re.match(car_pattern, plate_id):
            return True
        return False

    def add_task(self):
        plate_id = self.plate_id_entry.get()
        task = self.task_var.get()

        if not plate_id:
            self.show_error("Plate ID Error", "Plate ID cannot be empty. Please enter a valid Plate ID.")
            return

        if not self.validate_plate_id(plate_id):
            self.show_error("Plate ID Error", "Invalid Plate ID. It must follow the format:\nCar: RA[A-G]123A to RA[G]999Z")
            return

        if task == "Select an Operation":
            self.show_error("Selection Error", "Please select a valid operation from the dropdown.")
            return

        self.tasks.add_task(task, plate_id)
        self.update_task_listbox()
        self.plate_id_entry.delete(0, tk.END)
        self.show_success(f"Task '{task}' for Plate ID {plate_id} added successfully.")

    def remove_task(self):
        removed_node = self.tasks.remove_task()
        if removed_node:
            self.update_task_listbox()
            self.show_success(f"Task '{removed_node.task}' for Plate ID {removed_node.plate_id} removed.")
        else:
            self.show_error("No Tasks", "No tasks to remove.")

    def update_task_listbox(self):
        self.tasks_listbox.delete(2, tk.END)
        tasks = self.tasks.get_all_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, task)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_success(self, message):
        messagebox.showinfo("Success", message)

    def on_closing(self):
        """Ask the user for confirmation before closing"""
        if messagebox.askokcancel("Quit", "Are you sure you want to close the application?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
