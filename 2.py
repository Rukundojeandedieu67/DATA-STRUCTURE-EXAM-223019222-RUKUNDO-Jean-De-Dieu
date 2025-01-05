import tkinter as tk
from tkinter import messagebox, ttk
import re

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

        tk.Button(add_buttons_frame, text="Add to Front", command=self.add_task_to_front, bg="#4CAF50", fg="white", font=("Helvetica", 14), relief="flat", width=12, height=2).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(add_buttons_frame, text="Add to Rear", command=self.add_task_to_rear, bg="#2196F3", fg="white", font=("Helvetica", 14), relief="flat", width=12, height=2).grid(row=0, column=1, padx=5, pady=5)

        # Maintenance Tasks Section with border
        tk.Label(root, text="Pending Maintenance Tasks:", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)
        self.tasks_listbox = tk.Listbox(root, font=("Helvetica", 14), height=8, width=50, bd=2, relief="solid", selectmode=tk.SINGLE, bg="#f0f0f0", fg="#333")
        self.tasks_listbox.pack(pady=5)

        # Action Buttons for removing tasks with enhanced design
        action_frame = tk.Frame(root, bg="#f7f7f7")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Remove from Front", command=self.remove_task_from_front, bg="#f44336", fg="white", font=("Helvetica", 14), relief="flat", width=16, height=2).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(action_frame, text="Remove from Rear", command=self.remove_task_from_rear, bg="#FF9800", fg="white", font=("Helvetica", 14), relief="flat", width=16, height=2).grid(row=0, column=1, padx=5, pady=5)

        # Initialize tasks list (deque)
        self.tasks = []

        # Bind the close window event to show confirmation message
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def validate_plate_id(self, plate_id):
        """Validate the plate ID format for car."""
        # Regex for Car Plate ID: 'RAA123A' to 'RAG999Z' (Car format)
        car_pattern = r"^RA[A-G]\d{3}[A-Z]$"  # RA followed by A to G, 3 digits, and 1 letter

        # Check if the plate ID matches the car pattern
        if re.match(car_pattern, plate_id):
            return True
        return False

    def show_custom_popup(self, title, message, is_error=False):
        """Create a custom pop-up window for messages with attractive design."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        popup.configure(bg="#FFEB3B" if not is_error else "#F44336")

        # Label with customized font and background
        label = tk.Label(popup, text=message, font=("Helvetica", 12, "bold"), fg="white", bg="#FFEB3B" if not is_error else "#F44336", wraplength=350)
        label.pack(pady=20)

        # Close Button with a positive/negative color
        close_button_color = "#4CAF50" if not is_error else "#FF5722"
        close_button = tk.Button(popup, text="Close", command=popup.destroy, font=("Helvetica", 14, "bold"), fg="white", bg=close_button_color, width=10, height=2, relief="flat")
        close_button.pack(pady=10)

    def show_confirmation_popup(self, title, message, on_confirm, on_cancel):
        """Create a confirmation dialog box with custom design and buttons."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        popup.configure(bg="#2196F3")

        label = tk.Label(popup, text=message, font=("Helvetica", 14, "bold"), fg="white", bg="#2196F3", wraplength=350)
        label.pack(pady=20)

        # Yes and No Buttons for confirmation
        yes_button = tk.Button(popup, text="Yes", command=lambda: [on_confirm(), popup.destroy()], font=("Helvetica", 14, "bold"), fg="white", bg="#4CAF50", width=10, height=2, relief="flat")
        yes_button.pack(side=tk.LEFT, padx=10, pady=10)

        no_button = tk.Button(popup, text="No", command=lambda: [on_cancel(), popup.destroy()], font=("Helvetica", 14, "bold"), fg="white", bg="#FF5722", width=10, height=2, relief="flat")
        no_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def add_task_to_front(self):
        plate_id = self.plate_id_entry.get()
        task = self.task_var.get()

        if not self.validate_plate_id(plate_id):
            self.show_custom_popup("Plate ID Error", "Invalid Plate ID. It must follow the format:\n"
                                                    "Car: RA[A-G]123A to RA[G]999Z", is_error=True)
            return

        if task == "Select an Operation":
            self.show_custom_popup("Selection Error", "Please select a valid operation.", is_error=True)
        else:
            # Show confirmation dialog for adding to front
            self.show_confirmation_popup(
                "Confirm Action", 
                f"Are you sure you want to add task '{task}' for Plate ID {plate_id} to the front?", 
                lambda: self.confirm_add_to_front(plate_id, task), 
                lambda: None
            )

    def confirm_add_to_front(self, plate_id, task):
        # Add to the front of the task list
        self.tasks.insert(0, f"{task} - {plate_id}")
        self.update_task_listbox()
        self.plate_id_entry.delete(0, tk.END)  # Clear Plate ID after use
        messagebox.showinfo("Task Added", f"Task '{task}' for Plate ID {plate_id} added to the front.")

    def add_task_to_rear(self):
        plate_id = self.plate_id_entry.get()
        task = self.task_var.get()

        if not self.validate_plate_id(plate_id):
            self.show_custom_popup("Plate ID Error", "Invalid Plate ID. It must follow the format:\n"
                                                    "Car: RA[A-G]123A to RA[G]999Z", is_error=True)
            return

        if task == "Select an Operation":
            self.show_custom_popup("Selection Error", "Please select a valid operation.", is_error=True)
        else:
            # Show confirmation dialog for adding to rear
            self.show_confirmation_popup(
                "Confirm Action", 
                f"Are you sure you want to add task '{task}' for Plate ID {plate_id} to the rear?", 
                lambda: self.confirm_add_to_rear(plate_id, task), 
                lambda: None
            )

    def confirm_add_to_rear(self, plate_id, task):
        # Add to the rear of the task list
        self.tasks.append(f"{task} - {plate_id}")
        self.update_task_listbox()
        self.plate_id_entry.delete(0, tk.END)  # Clear Plate ID after use
        messagebox.showinfo("Task Added", f"Task '{task}' for Plate ID {plate_id} added to the rear.")

    def remove_task_from_front(self):
        if self.tasks:
            # Show confirmation dialog for removing from front
            self.show_confirmation_popup(
                "Confirm Removal", 
                "Are you sure you want to remove the task from the front?", 
                lambda: self.confirm_remove_from_front(), 
                lambda: None
            )
        else:
            messagebox.showwarning("No Tasks", "No tasks to remove from the front.")

    def confirm_remove_from_front(self):
        # Remove the task from the front
        self.tasks.pop(0)
        self.update_task_listbox()
        messagebox.showinfo("Task Removed", "The task was successfully removed from the front.")

    def remove_task_from_rear(self):
        if self.tasks:
            # Show confirmation dialog for removing from rear
            self.show_confirmation_popup(
                "Confirm Removal", 
                "Are you sure you want to remove the task from the rear?", 
                lambda: self.confirm_remove_from_rear(), 
                lambda: None
            )
        else:
            messagebox.showwarning("No Tasks", "No tasks to remove from the rear.")

    def confirm_remove_from_rear(self):
        # Remove the task from the rear
        self.tasks.pop()
        self.update_task_listbox()
        messagebox.showinfo("Task Removed", "The task was successfully removed from the rear.")

    def update_task_listbox(self):
        # Update the listbox with the current tasks
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)

    def on_closing(self):
        """Prompt the user with a confirmation message before quitting."""
        self.show_confirmation_popup(
            "Quit Confirmation", 
            "Are you sure you want to quit?", 
            lambda: self.root.quit(), 
            lambda: None
        )


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
