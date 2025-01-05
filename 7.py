import tkinter as tk
from tkinter import messagebox, ttk
import re

class Node:
    """Node class for the Doubly Linked List"""
    def __init__(self, task, plate_id, priority):
        self.task = task
        self.plate_id = plate_id
        self.priority = priority
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """Doubly Linked List to manage tasks"""
    def __init__(self):
        self.head = None
        self.tail = None

    def add_task(self, task, plate_id, priority):
        new_node = Node(task, plate_id, priority)
        if not self.head:  # If the list is empty
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def insertion_sort(self):
        """Sort tasks in the linked list by priority using Insertion Sort"""
        if not self.head or not self.head.next:
            return  # List is empty or has only one element

        current = self.head.next
        while current:
            key = current
            prev = current.prev

            while prev and key.priority < prev.priority:
                # Swap data between nodes
                prev.task, key.task = key.task, prev.task
                prev.plate_id, key.plate_id = key.plate_id, prev.plate_id
                prev.priority, key.priority = key.priority, prev.priority

                key = prev
                prev = prev.prev

            current = current.next

    def get_all_tasks(self):
        """Get all tasks as a list of strings"""
        tasks = []
        current = self.head
        while current:
            tasks.append(f"{current.task} - {current.plate_id} (Priority: {current.priority})")
            current = current.next
        return tasks

    def remove_task(self):
        """Remove task from the front"""
        if not self.head:  # List is empty
            return None
        removed_node = self.head
        self.head = self.head.next
        if self.head:  # If there is a new head, update its prev pointer
            self.head.prev = None
        if not self.head:  # If the list becomes empty, set tail to None
            self.tail = None
        return removed_node

class MaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Maintenance Tracker")

        # Set the window to full screen
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

        # Title Label
        title_label = tk.Label(root, text="Car Maintenance Tracker", font=("Helvetica", 26, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=20)

        # Plate ID Input Frame
        self.plate_frame = tk.Frame(root, bg="#f7f7f7")
        self.plate_frame.pack(pady=15)

        tk.Label(self.plate_frame, text="Enter Plate ID (e.g., RAA123A):", font=("Helvetica", 14), bg="#f7f7f7", fg="#333").grid(row=0, column=0, padx=10)
        self.plate_id_entry = tk.Entry(self.plate_frame, font=("Helvetica", 14), width=20, bd=2, relief="solid", highlightcolor="#4CAF50", highlightthickness=2)
        self.plate_id_entry.grid(row=0, column=1, padx=10)

        # Task Input Frame
        input_frame = tk.Frame(root, bg="#f7f7f7")
        input_frame.pack(pady=10)

        # Dropdown for Task Selection
        self.task_var = tk.StringVar()
        self.task_var.set(self.task_options[0])
        self.task_dropdown = ttk.Combobox(input_frame, textvariable=self.task_var, values=self.task_options, font=("Helvetica", 14), state="readonly", width=25)
        self.task_dropdown.grid(row=0, column=0, padx=5)

        # Priority Input
        self.priority_var = tk.IntVar()
        self.priority_var.set(1)
        tk.Label(input_frame, text="Priority (1-5):", font=("Helvetica", 14), bg="#f7f7f7", fg="#333").grid(row=0, column=1, padx=5)
        priority_dropdown = ttk.Combobox(input_frame, textvariable=self.priority_var, values=[1, 2, 3, 4, 5], font=("Helvetica", 14), state="readonly", width=5)
        priority_dropdown.grid(row=0, column=2, padx=5)

        # Add Task Button
        tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Helvetica", 14), relief="flat", width=12, height=2).grid(row=0, column=3, padx=10)

        # Maintenance Tasks Section
        tk.Label(root, text="Pending Maintenance Tasks:", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

        # Listbox to show tasks
        self.tasks_listbox = tk.Listbox(root, font=("Helvetica", 14), height=10, width=50, bd=2, relief="solid", selectmode=tk.SINGLE, bg="#f0f0f0", fg="#333")
        self.tasks_listbox.pack(pady=5)

        # Add Columns
        self.tasks_listbox.insert(tk.END, "OPERATION                PLATE ID                PRIORITY")
        self.tasks_listbox.insert(tk.END, "-" * 50)

        # Remove Task Button
        tk.Button(root, text="Remove Task", command=self.remove_task, bg="#FF5722", fg="white", font=("Helvetica", 14), relief="flat", width=20, height=2).pack(pady=10)

        # Initialize Doubly Linked List
        self.tasks = DoublyLinkedList()

    def validate_plate_id(self, plate_id):
        """Validate Plate ID format"""
        car_pattern = r"^RA[A-G]\d{3}[A-Z]$"
        return bool(re.match(car_pattern, plate_id))

    def add_task(self):
        plate_id = self.plate_id_entry.get()
        task = self.task_var.get()
        priority = self.priority_var.get()

        if not plate_id:
            self.show_message("Plate ID Error", "Plate ID cannot be empty.", "error")
            return

        if not self.validate_plate_id(plate_id):
            self.show_message("Plate ID Error", "Invalid Plate ID format.", "error")
            return

        if task == "Select an Operation":
            self.show_message("Selection Error", "Please select a valid operation.", "error")
            return

        self.tasks.add_task(task, plate_id, priority)
        self.tasks.insertion_sort()
        self.update_task_listbox()
        self.show_message("Success", f"Task '{task}' added successfully.", "success")
        self.plate_id_entry.delete(0, tk.END)

    def remove_task(self):
        removed_node = self.tasks.remove_task()
        if removed_node:
            self.update_task_listbox()
            self.show_message("Success", f"Task '{removed_node.task}' removed.", "success")
        else:
            self.show_message("No Tasks", "No tasks to remove.", "error")

    def update_task_listbox(self):
        """Update the listbox with sorted tasks"""
        self.tasks_listbox.delete(2, tk.END)
        tasks = self.tasks.get_all_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, task)

    def show_message(self, title, message, msg_type):
        """Custom message popup"""
        color = {"error": "#FF5733", "success": "#4CAF50", "info": "#2196F3"}
        messagebox.showinfo(title, message)

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
