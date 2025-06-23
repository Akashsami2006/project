import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, date
import sqlite3
from typing import List, Dict, Optional, Tuple

class CalendarApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Monthly Calendar with Reminders")
        
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        self.db_conn = sqlite3.connect("reminders.db")
        self.create_db_table()
        
        self.create_widgets()
        self.update_calendar()
    
    def create_db_table(self) -> None:
        """Create the reminders table if it doesn't exist"""
        cursor = self.db_conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS reminders ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "year INTEGER, "
            "month INTEGER, "
            "day INTEGER, "
            "time TEXT, "
            "title TEXT, "
            "description TEXT, "
            "is_completed INTEGER DEFAULT 0"
            ")"
        )
        self.db_conn.commit()
    
    def create_widgets(self) -> None:
        """Create all the UI widgets"""
        
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=10)
        
        self.prev_btn = ttk.Button(nav_frame, text="<", command=self.prev_month)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.month_year_label = ttk.Label(nav_frame, text="", font=('Arial', 12, 'bold'))
        self.month_year_label.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = ttk.Button(nav_frame, text=">", command=self.next_month)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.today_btn = ttk.Button(nav_frame, text="Today", command=self.go_to_today)
        self.today_btn.pack(side=tk.LEFT, padx=10)
        
        self.cal_frame = ttk.Frame(self.root)
        self.cal_frame.pack(pady=10)
        
        reminder_frame = ttk.LabelFrame(self.root, text="Reminders")
        reminder_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        
        self.reminder_tree = ttk.Treeview(
            reminder_frame, 
            columns=("id", "date", "time", "title", "description", "status"), 
            show="headings"
        )
        
        self.reminder_tree.heading("id", text="ID")
        self.reminder_tree.heading("date", text="Date")
        self.reminder_tree.heading("time", text="Time")
        self.reminder_tree.heading("title", text="Title")
        self.reminder_tree.heading("description", text="Description")
        self.reminder_tree.heading("status", text="Status")
        
        self.reminder_tree.column("id", width=30, anchor=tk.CENTER)
        self.reminder_tree.column("date", width=80, anchor=tk.CENTER)
        self.reminder_tree.column("time", width=60, anchor=tk.CENTER)
        self.reminder_tree.column("title", width=120)
        self.reminder_tree.column("description", width=200)
        self.reminder_tree.column("status", width=80, anchor=tk.CENTER)
        
        self.reminder_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(reminder_frame)
        btn_frame.pack(pady=5)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Reminder", command=self.add_reminder)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ttk.Button(btn_frame, text="Edit Reminder", command=self.edit_reminder)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete Reminder", command=self.delete_reminder)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.complete_btn = ttk.Button(btn_frame, text="Mark Complete", command=self.toggle_complete)
        self.complete_btn.pack(side=tk.LEFT, padx=5)
        
        self.reminder_tree.bind("<Double-1>", self.view_reminder)
    
    def update_calendar(self) -> None:
        """Update the calendar display"""
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
        
        
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")
        
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekdays):
            ttk.Label(self.cal_frame, text=day, width=10, relief=tk.RIDGE).grid(row=0, column=i)
        
        
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day != 0:
                    btn = ttk.Button(
                        self.cal_frame, 
                        text=str(day), 
                        width=10,
                        command=lambda d=day: self.show_day_reminders(d)
                    )
                    
                    
                    today = datetime.now()
                    if (self.current_year == today.year and 
                        self.current_month == today.month and 
                        day == today.day):
                        btn.config(style="Bold.TButton")
                    
                    btn.grid(row=week_num, column=day_num)
        
        
        self.update_reminders_list()
    
    def update_reminders_list(self, day: Optional[int] = None) -> None:
        """Update the reminders list for a specific day or the whole month"""
        self.reminder_tree.delete(*self.reminder_tree.get_children())
        
        cursor = self.db_conn.cursor()
        if day:
            cursor.execute(
                "SELECT id, day, time, title, description, is_completed "
                "FROM reminders "
                "WHERE year=? AND month=? AND day=? "
                "ORDER BY time",
                (self.current_year, self.current_month, day)
            )
        else:
            cursor.execute(
                "SELECT id, day, time, title, description, is_completed "
                "FROM reminders "
                "WHERE year=? AND month=? "
                "ORDER BY day, time",
                (self.current_year, self.current_month)
            )
        
        reminders = cursor.fetchall()
        
        for reminder in reminders:
            id_, day, time, title, desc, completed = reminder
            date_str = f"{day}/{self.current_month}/{self.current_year}"
            status = "Completed" if completed else "Pending"
            self.reminder_tree.insert("", tk.END, values=(id_, date_str, time, title, desc, status))
    
    def show_day_reminders(self, day: int) -> None:
        """Show reminders for a specific day"""
        self.update_reminders_list(day)
    
    def prev_month(self) -> None:
        """Navigate to previous month"""
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()
    
    def next_month(self) -> None:
        """Navigate to next month"""
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()
    
    def go_to_today(self) -> None:
        """Navigate to current month and day"""
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.update_calendar()
        self.update_reminders_list(today.day)
    
    def add_reminder(self) -> None:
        """Open dialog to add a new reminder"""
        self.reminder_dialog("Add Reminder")
    
    def edit_reminder(self) -> None:
        """Edit selected reminder"""
        selected = self.reminder_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reminder to edit")
            return
        
        item = self.reminder_tree.item(selected[0])
        reminder_id = item['values'][0]
        self.reminder_dialog("Edit Reminder", reminder_id)
    
    def delete_reminder(self) -> None:
        """Delete selected reminder"""
        selected = self.reminder_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reminder to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reminder?"):
            item = self.reminder_tree.item(selected[0])
            reminder_id = item['values'][0]
            
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
            self.db_conn.commit()
            
            self.update_reminders_list()
    
    def toggle_complete(self) -> None:
        """Toggle completion status of selected reminder"""
        selected = self.reminder_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reminder to mark complete/incomplete")
            return
        
        item = self.reminder_tree.item(selected[0])
        reminder_id = item['values'][0]
        current_status = 1 if item['values'][5] == "Completed" else 0
        
        cursor = self.db_conn.cursor()
        cursor.execute(
            "UPDATE reminders "
            "SET is_completed=? "
            "WHERE id=?",
            (1 - current_status, reminder_id)
        )
        self.db_conn.commit()
        
        self.update_reminders_list()
    
    def view_reminder(self, event) -> None:
        """View reminder details"""
        selected = self.reminder_tree.selection()
        if not selected:
            return
        
        item = self.reminder_tree.item(selected[0])
        reminder_id = item['values'][0]
        
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT year, month, day, time, title, description, is_completed "
            "FROM reminders "
            "WHERE id=?",
            (reminder_id,)
        )
        
        year, month, day, time, title, desc, completed = cursor.fetchone()
        
        details = (
            f"Date: {day}/{month}/{year}\n"
            f"Time: {time}\n"
            f"Title: {title}\n"
            f"Description: {desc}\n"
            f"Status: {'Completed' if completed else 'Pending'}"
        )
        
        messagebox.showinfo("Reminder Details", details)
    
    def reminder_dialog(self, title: str, reminder_id: Optional[int] = None) -> None:
        """Create a dialog for adding/editing reminders"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        
        
        default_day = datetime.now().day if not reminder_id else None
        default_time = "12:00"
        default_title = ""
        default_desc = ""
        
        
        if reminder_id:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "SELECT year, month, day, time, title, description "
                "FROM reminders "
                "WHERE id=?",
                (reminder_id,)
            )
            
            year, month, day, time, title, desc = cursor.fetchone()
            default_day = day
            default_time = time
            default_title = title
            default_desc = desc
        
        
        ttk.Label(dialog, text="Day:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        day_var = tk.IntVar(value=default_day)
        day_spin = ttk.Spinbox(dialog, from_=1, to=31, textvariable=day_var, width=5)
        day_spin.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        
        ttk.Label(dialog, text="Time (HH:MM):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        time_var = tk.StringVar(value=default_time)
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=10)
        time_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        
        ttk.Label(dialog, text="Title:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        title_var = tk.StringVar(value=default_title)
        title_entry = ttk.Entry(dialog, textvariable=title_var, width=30)
        title_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        
        ttk.Label(dialog, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.NE)
        desc_var = tk.StringVar(value=default_desc)
        desc_entry = tk.Text(dialog, width=30, height=5)
        desc_entry.insert(tk.END, default_desc)
        desc_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        
        def save_reminder() -> None:
            day = day_var.get()
            time_str = time_var.get()
            title = title_var.get()
            desc = desc_entry.get("1.0", tk.END).strip()
            
            
            try:
                
                last_day = calendar.monthrange(self.current_year, self.current_month)[1]
                if day < 1 or day > last_day:
                    raise ValueError(f"Day must be between 1 and {last_day}")
                
                
                try:
                    datetime.strptime(time_str, "%H:%M")
                except ValueError:
                    raise ValueError("Time must be in HH:MM format")
                
                if not title:
                    raise ValueError("Title cannot be empty")
                
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
                return
            
            # Save to database
            cursor = self.db_conn.cursor()
            if reminder_id:
                
                cursor.execute(
                    "UPDATE reminders "
                    "SET day=?, time=?, title=?, description=? "
                    "WHERE id=?",
                    (day, time_str, title, desc, reminder_id)
                )
            else:
                
                cursor.execute(
                    "INSERT INTO reminders (year, month, day, time, title, description) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (self.current_year, self.current_month, day, time_str, title, desc)
                )
            
            self.db_conn.commit()
            dialog.destroy()
            self.update_reminders_list()
        
        ttk.Button(dialog, text="Save", command=save_reminder).grid(row=4, column=1, padx=5, pady=10, sticky=tk.E)
    
    def __del__(self) -> None:
        """Clean up when the app is closed"""
        self.db_conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    
    
    style = ttk.Style()
    style.configure("Bold.TButton", font=('Arial', 10, 'bold'))
    
    root.mainloop()