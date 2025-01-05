import tkinter as tk
from tkinter import messagebox, ttk
import re

class TreeNode:
    """TreeNode class for representing tasks and sub-tasks in a hierarchical structure"""
    def __init__(self, task, plate_id=None):
        self.task = task
        self.plate_id = plate_id
        self.children = []  # List of child nodes (sub-tasks)

    def add_child(self, child_node):
        """Add a sub-task (child node) to the current node"""
        self.children.append(child_node)

    def __str__(self):
        """Return a string representation of the task"""
        return f"{self.task} - {self.plate_id if self.plate_id else ''}"

class TaskTree:
    """TaskTree class to manage the tree structure of tasks"""
    def __init__(self):
        self.root = None

    def set_root(self, root_node):
        """Set the root node of the tree"""
        self.root = root_node

    def add_task(self, parent_task, task, plate_id=None):
        """Add a new task under the specified parent task"""
        parent_node = self.find_task(self.root, parent_task)
        if parent_node:
            new_task_node = TreeNode(task, plate_id)
            parent_node.add_child(new_task_node)

    def find_task(self, node, task):
        """Find a task in the tree by task name"""
        if node.task == task:
            return node
        for child in node.children:
            result = self.find_task(child, task)
            if result:
                return result
        return None

    def get_all_tasks(self, node=None, prefix=""):
        """Recursively get all tasks as a list of strings"""
        if node is None:
            node = self.root

        tasks = []
        tasks.append(f"{prefix}{node.task} - {node.plate_id if node.plate_id else ''}")
        for child in node.children:
            tasks.extend(self.get_all_tasks(child, prefix + "  "))
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

        self.task_tree = TaskTree()

        # Root task (e.g., "Maintenance")
        self.root_task = TreeNode("Maintenance")
        self.task_tree.set_root(self.root_task)

        # Add sub-tasks under the root task
        oil_change = TreeNode("Oil Change")
        self.root_task.add_child(oil_change)
        self.task_tree.add_task("Oil Change", "Engine Oil Change")

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

        self.task_tree.add_task("Maintenance", task, plate_id)  # Add task under "Maintenance"
        self.update_task_listbox()
        self.plate_id_entry.delete(0, tk.END)
        self.show_success(f"Task '{task}' for Plate ID {plate_id} added successfully.")

    def remove_task(self):
        task_to_remove = self.task_var.get()
        task_node = self.task_tree.find_task(self.root_task, task_to_remove)
        if task_node:
            self.show_remove_confirmation(task_node)
        else:
            self.show_error("No Tasks", "No tasks to remove.")

    def show_remove_confirmation(self, task_node):
        """Show confirmation popup before removing the task"""
        response = messagebox.askyesno("Remove Task", f"Are you sure you want to remove '{task_node.task}' with Plate ID '{task_node.plate_id}'?")
        if response:
            self.task_tree.remove_task(task_node)
            self.update_task_listbox()
            self.show_success(f"Task '{task_node.task}' removed successfully.")

    def update_task_listbox(self):
        self.tasks_listbox.delete(2, tk.END)
        tasks = self.task_tree.get_all_tasks(self.root_task)
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
