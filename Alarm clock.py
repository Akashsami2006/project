import os
import time
import datetime
from threading import Thread
from tkinter import *
from tkinter import filedialog, messagebox
from playsound import playsound
import pygame.mixer

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Alarm Clock")
        self.root.geometry("500x400")
        
        pygame.mixer.init()
        self.alarms = []
        self.snooze_duration = 5  # default snooze duration in minutes
        self.current_alarm_tone = "default.mp3"  # default tone
        self.custom_tone_path = None
        
        self.create_widgets()

        self.check_alarms_thread = Thread(target=self.check_alarms, daemon=True)
        self.check_alarms_thread.start()
    
    def create_widgets(self):
        settings_frame = LabelFrame(self.root, text="Set New Alarm", padx=10, pady=10)
        settings_frame.pack(pady=10, padx=10, fill="x")
        
        time_frame = Frame(settings_frame)
        time_frame.pack(fill="x", pady=5)
        
        Label(time_frame, text="Time (HH:MM):").pack(side=LEFT)
        self.hour_var = StringVar(value="12")
        self.minute_var = StringVar(value="00")
        self.ampm_var = StringVar(value="PM")
        
        Spinbox(time_frame, from_=1, to=12, textvariable=self.hour_var, width=3).pack(side=LEFT, padx=5)
        Spinbox(time_frame, from_=0, to=59, textvariable=self.minute_var, width=3, format="%02.0f").pack(side=LEFT, padx=5)
        OptionMenu(time_frame, self.ampm_var, "AM", "PM").pack(side=LEFT, padx=5)
        
        date_frame = Frame(settings_frame)
        date_frame.pack(fill="x", pady=5)
        Label(date_frame, text="Date (YYYY-MM-DD):").pack(side=LEFT)
        self.date_var = StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        Entry(date_frame, textvariable=self.date_var).pack(side=LEFT, padx=5, expand=True, fill="x")
        
        tone_frame = Frame(settings_frame)
        tone_frame.pack(fill="x", pady=5)
        
        Label(tone_frame, text="Alarm Tone:").pack(side=LEFT)
        self.tone_var = StringVar(value="Default Tone")
        tone_options = ["Default Tone", "Custom Tone"]
        OptionMenu(tone_frame, self.tone_var, *tone_options, command=self.tone_selected).pack(side=LEFT, padx=5)
        Button(tone_frame, text="Browse", command=self.browse_tone).pack(side=LEFT, padx=5)
        
        snooze_frame = Frame(settings_frame)
        snooze_frame.pack(fill="x", pady=5)
        
        Label(snooze_frame, text="Snooze Duration (min):").pack(side=LEFT)
        self.snooze_var = IntVar(value=self.snooze_duration)
        Spinbox(snooze_frame, from_=1, to=30, textvariable=self.snooze_var, width=3).pack(side=LEFT, padx=5)
        
        Button(settings_frame, text="Set Alarm", command=self.set_alarm).pack(pady=10)
        
        alarms_frame = LabelFrame(self.root, text="Active Alarms", padx=10, pady=10)
        alarms_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.alarms_listbox = Listbox(alarms_frame)
        self.alarms_listbox.pack(fill="both", expand=True)
        
        control_frame = Frame(alarms_frame)
        control_frame.pack(fill="x", pady=5)
        
        Button(control_frame, text="Delete Alarm", command=self.delete_alarm).pack(side=LEFT, padx=5)
        Button(control_frame, text="Snooze Alarm", command=self.snooze_alarm).pack(side=LEFT, padx=5)
    
    def tone_selected(self, value):
        if value == "Default Tone":
            self.custom_tone_path = None
    
    def browse_tone(self):
        file_path = filedialog.askopenfilename(
            title="Select Alarm Tone",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if file_path:
            self.custom_tone_path = file_path
            self.tone_var.set("Custom Tone")
    
    def set_alarm(self):
        try:    
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            ampm = self.ampm_var.get()
            
            if ampm == "PM" and hour != 12:
                hour += 12
            elif ampm == "AM" and hour == 12:
                hour = 0
            
            year, month, day = map(int, self.date_var.get().split("-"))
            alarm_time = datetime.datetime(year, month, day, hour, minute)
            
            if alarm_time < datetime.datetime.now():
                messagebox.showerror("Error", "Cannot set alarm for past time!")
                return

            self.snooze_duration = self.snooze_var.get()
            
            alarm = {
                "time": alarm_time,
                "tone": self.custom_tone_path if self.custom_tone_path else "default",
                "snooze_duration": self.snooze_duration,
                "active": True
            }
            self.alarms.append(alarm)
            self.update_alarms_list()
            
            messagebox.showinfo("Success", f"Alarm set for {alarm_time.strftime('%Y-%m-%d %I:%M %p')}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def update_alarms_list(self):
        self.alarms_listbox.delete(0, END)
        for i, alarm in enumerate(self.alarms):
            status = "Active" if alarm["active"] else "Inactive"
            tone = "Custom" if alarm["tone"] != "default" else "Default"
            self.alarms_listbox.insert(
                END,
                f"{i+1}. {alarm['time'].strftime('%Y-%m-%d %I:%M %p')} | {tone} tone | Snooze: {alarm['snooze_duration']} min | {status}"
            )
    
    def delete_alarm(self):
        try:
            selection = self.alarms_listbox.curselection()
            if selection:
                index = selection[0]
                del self.alarms[index]
                self.update_alarms_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete alarm: {str(e)}")
    
    def snooze_alarm(self):
        try:
            selection = self.alarms_listbox.curselection()
            if selection:
                index = selection[0]
                alarm = self.alarms[index]
                
                snooze_minutes = alarm["snooze_duration"]
                new_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze_minutes)
                
                new_alarm = {
                    "time": new_time,
                    "tone": alarm["tone"],
                    "snooze_duration": alarm["snooze_duration"],
                    "active": True
                }
                
                self.alarms.append(new_alarm)
                self.update_alarms_list()
                
                pygame.mixer.music.stop()
                
                messagebox.showinfo("Snooze", f"Alarm snoozed for {snooze_minutes} minutes")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to snooze alarm: {str(e)}")
    
    def check_alarms(self):
        while True:
            now = datetime.datetime.now()
            
            for alarm in self.alarms:
                if alarm["active"] and now >= alarm["time"]:
                   
                    self.trigger_alarm(alarm)
                    
                    alarm["active"] = False
                    self.update_alarms_list()
            
            time.sleep(1)
    
    def trigger_alarm(self, alarm):
        
        def play_alarm_tone():
            try:
                tone_path = alarm["tone"]
                if tone_path == "default":
                    
                    for _ in range(5):
                        pygame.mixer.music.load(self.get_default_tone())
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                        time.sleep(0.5)
                else:
                    pygame.mixer.music.load(tone_path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
            except Exception as e:
                print(f"Error playing alarm tone: {e}")

        self.root.after(0, lambda: messagebox.showinfo(
            "Alarm",
            f"Alarm! It's {alarm['time'].strftime('%I:%M %p')}\n\nClick OK to stop the alarm."
        ))
        
        tone_thread = Thread(target=play_alarm_tone)
        tone_thread.start()
        
        self.root.wait_window(self.root.focus_get())
        
        pygame.mixer.music.stop()
    
    def get_default_tone(self):
        
        
        try:
            import winsound
            winsound.Beep(1000, 500)  
            return None
        except:
           
            return None

if __name__ == "__main__":
    root = Tk()
    app = AlarmClock(root)
    root.mainloop()