import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        
        # Task list
        self.tasks = []
        self.load_tasks()
        
        # UI Elements
        self.create_widgets()
        self.update_task_list()
    
    def create_widgets(self):
        # Task entry frame
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.grid(row=0, column=0, sticky="ew")
        
        ttk.Label(entry_frame, text="New Task:").grid(row=0, column=0, sticky="w")
        self.task_entry = ttk.Entry(entry_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(entry_frame, text="Category:").grid(row=1, column=0, sticky="w")
        self.category_entry = ttk.Entry(entry_frame, width=40)
        self.category_entry.grid(row=1, column=1, padx=5)
        
        ttk.Button(entry_frame, text="Add Task", command=self.add_task).grid(row=2, column=1, pady=5, sticky="e")
        
        # Task list frame
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.grid(row=1, column=0, sticky="nsew")
        
        self.task_tree = ttk.Treeview(list_frame, columns=("ID", "Description", "Category", "Status"), show="headings")
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.pack(fill="both", expand=True)
        
        # Action buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=2, column=0, sticky="ew")
        
        ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
    
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self):
        description = self.task_entry.get()
        category = self.category_entry.get() or "General"
        
        if description:
            task = {
                "id": len(self.tasks) + 1,
                "description": description,
                "category": category,
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.tasks.append(task)
            self.save_tasks()
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty!")
    
    def update_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        for task in self.tasks:
            status = "Completed" if task["completed"] else "Pending"
            self.task_tree.insert("", "end", values=(task["id"], task["description"], task["category"], status))
    
    def mark_complete(self):
        selected = self.task_tree.selection()
        if selected:
            task_id = int(self.task_tree.item(selected[0])["values"][0])
            for task in self.tasks:
                if task["id"] == task_id:
                    task["completed"] = True
                    self.save_tasks()
                    self.update_task_list()
                    break
    
    def delete_task(self):
        selected = self.task_tree.selection()
        if selected:
            task_id = int(self.task_tree.item(selected[0])["values"][0])
            self.tasks = [task for task in self.tasks if task["id"] != task_id]
            self.save_tasks()
            self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()