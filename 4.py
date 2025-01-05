import tkinter as tk
from tkinter import messagebox, ttk
import re


class Node:
    """Node class for the Binary Tree"""
    def __init__(self, task, plate_id):
        self.task = task
        self.plate_id = plate_id
        self.left = None
        self.right = None


class BinaryTree:
    """Binary Tree to manage tasks with a fixed number of orders"""
    def __init__(self, max_size):
        self.root = None
        self.max_size = max_size
        self.size = 0

    def insert(self, task, plate_id):
        """Insert a task in the binary tree"""
        if self.size >= self.max_size:
            return False  # Tree is full, cannot add more tasks
        if self.root is None:
            self.root = Node(task, plate_id)
        else:
            self._insert(self.root, task, plate_id)
        self.size += 1
        return True

    def _insert(self, node, task, plate_id):
        """Recursive insertion helper"""
        if task < node.task:
            if node.left is None:
                node.left = Node(task, plate_id)
            else:
                self._insert(node.left, task, plate_id)
        else:
            if node.right is None:
                node.right = Node(task, plate_id)
            else:
                self._insert(node.right, task, plate_id)

    def remove(self, task):
        """Remove a task from the binary tree"""
        self.root = self._remove(self.root, task)
        self.size -= 1

    def _remove(self, node, task):
        """Recursive removal helper"""
        if node is None:
            return node

        if task < node.task:
            node.left = self._remove(node.left, task)
        elif task > node.task:
            node.right = self._remove(node.right, task)
        else:
            # Node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.task = temp.task
            node.plate_id = temp.plate_id
            node.right = self._remove(node.right, temp.task)
        return node

    def _min_value_node(self, node):
        """Get the node with the minimum task"""
        current = node
        while current.left:
            current = current.left
        return current

    def get_all_tasks(self):
        """Get all tasks from the binary tree in sorted order"""
        tasks = []
        self._inorder(self.root, tasks)
        return tasks

    def _inorder(self, node, tasks):
        """Inorder traversal helper to get tasks in sorted order"""
        if node:
            self._inorder(node.left, tasks)
            tasks.append(f"{node.task} - {node.plate_id}")
            self._inorder(node.right, tasks)


class MaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Maintenance Tracker")

        # Set the window to full screen, but retain the window controls (close, minimize, maximize)
        self.root.state("zoomed")

        # Set the background color for the main window
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

        # Title with more attractive font and color
        title_label = tk.Label(root, text="Car Maintenance Tracker", font=("Helvetica", 26, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=20)

        # Plate ID Input Frame
        self.plate_frame = tk.Frame(root, bg="#f7f7f7")
        self.plate_frame.pack(pady=15)

        tk.Label(self.plate_frame, text="Enter Plate ID (e.g., RAA123A for Car):", font=("Helvetica", 14), bg="#f7f7f7", fg="#333").grid(row=0, column=0, padx=10)
        self.plate_id_entry = tk.Entry(self.plate_frame, font=("Helvetica", 14), width=20, bd=2, relief="solid", highlightcolor="#4CAF50", highlightthickness=2)
        self.plate_id_entry.grid(row=0, column=1, padx=10)

        # Task Input Frame (appears after plate ID entry)
        input_frame = tk.Frame(root, bg="#f7f7f7")
        input_frame.pack(pady=10)

        self.task_var = tk.StringVar()
        self.task_var.set(self.task_options[0])  # Default selection

        self.task_dropdown = ttk.Combobox(input_frame, textvariable=self.task_var, values=self.task_options, font=("Helvetica", 14), state="readonly", width=25)
        self.task_dropdown.grid(row=0, column=0, padx=5)

        # Action Buttons (Stylized)
        add_buttons_frame = tk.Frame(input_frame, bg="#f7f7f7")
        add_buttons_frame.grid(row=0, column=1, padx=10)

        tk.Button(add_buttons_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Helvetica", 14), relief="flat", width=12, height=2).grid(row=0, column=0, padx=5, pady=5)

        # Maintenance Tasks Section with border
        tk.Label(root, text="Pending Maintenance Tasks:", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

        # Listbox to show pending tasks
        self.tasks_listbox = tk.Listbox(root, font=("Helvetica", 14), height=8, width=50, bd=2, relief="solid", selectmode=tk.SINGLE, bg="#f0f0f0", fg="#333")
        self.tasks_listbox.pack(pady=5)

        # Title for columns in Listbox
        self.tasks_listbox.insert(tk.END, "OPERATION                PLATE ID")
        self.tasks_listbox.insert(tk.END, "-" * 50)  # Separator line

        # Remove Task Button
        tk.Button(root, text="Remove Task", command=self.remove_task, bg="#FF5722", fg="white", font=("Helvetica", 14), relief="flat", width=20, height=2).pack(pady=10)

        # Initialize tasks binary tree with a max size of 5
        self.max_size = 5
        self.tasks = BinaryTree(self.max_size)

        # Bind the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def validate_plate_id(self, plate_id):
        """Validate the plate ID format for car."""
        # Regex for Car Plate ID: 'RAA123A' to 'RAG999Z' (Car format)
        car_pattern = r"^RA[A-G]\d{3}[A-Z]$"  # RA followed by A to G, 3 digits, and 1 letter

        # Check if the plate ID matches the car pattern
        if re.match(car_pattern, plate_id):
            return True
        return False

    def add_task(self):
        plate_id = self.plate_id_entry.get()
        task = self.task_var.get()

        # Error handling for Plate ID validation
        if not plate_id:
            self.show_error("Plate ID Error", "Plate ID cannot be empty. Please enter a valid Plate ID.")
            return

        if not self.validate_plate_id(plate_id):
            self.show_error("Plate ID Error", "Invalid Plate ID. It must follow the format:\n"
                                              "Car: RA[A-G]123A to RA[G]999Z")
            return

        if task == "Select an Operation":
            self.show_error("Selection Error", "Please select a valid operation from the dropdown.")
            return

        # Insert task into the binary tree
        if not self.tasks.insert(task, plate_id):
            self.show_error("Tree Full", "The task tree is full. Cannot add more tasks.")
            return

        self.update_task_listbox()
        self.plate_id_entry.delete(0, tk.END)  # Clear Plate ID after use
        self.show_success(f"Task '{task}' for Plate ID {plate_id} added successfully.")

    def remove_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected or selected[0] < 2:  # Ignore header lines
            self.show_error("Selection Error", "Please select a valid task to remove.")
            return

        task_info = self.tasks_listbox.get(selected[0])
        task, plate_id = task_info.split(" - ")

        # Show confirmation dialog to remove task
        response = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove the operation '{task}' for Plate ID {plate_id}?")
        if response:
            self.tasks.remove(task)
            self.update_task_listbox()
            self.show_success(f"Task '{task}' for Plate ID {plate_id} removed.")

    def update_task_listbox(self):
        """Update the listbox with the current tasks from the binary tree"""
        self.tasks_listbox.delete(2, tk.END)  # Remove the old tasks
        tasks = self.tasks.get_all_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, task)

    def show_error(self, title, message):
        """Display custom error pop-up with attractive styling"""
        self.show_popup(title, message, "#F44336", "#ffffff")

    def show_success(self, message):
        """Display custom success pop-up with attractive styling"""
        self.show_popup("Success", message, "#4CAF50", "#ffffff")

    def show_popup(self, title, message, bg_color, fg_color):
        """Display a custom popup window"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x150")
        popup.config(bg=bg_color)

        label = tk.Label(popup, text=message, font=("Helvetica", 14), fg=fg_color, bg=bg_color)
        label.pack(pady=30)

        close_button = tk.Button(popup, text="Close", command=popup.destroy, font=("Helvetica", 14), bg="#ffffff", fg="#333")
        close_button.pack()

    def on_close(self):
        """Handle the close window event"""
        response = messagebox.askyesno("Confirm Exit", "Do you want to close the application?")
        if response:
            self.root.destroy()


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
