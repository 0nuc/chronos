import tkinter as tk
from tkinter import ttk
import time
from plyer import notification

class TimerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("250x235")
        self.root.configure(bg="black")
        self.root.resizable(False, False)
        
        # Variables du timer
        self.time_remaining = 0
        self.break_time = 0
        self.is_break = False
        self.is_running = False
        
        # Style
        self.style = ttk.Style()
        self.style.configure('Timer.TLabel', font=('Arial', 48, 'bold'))
        self.style.configure('Controls.TFrame', padding=10)
        
        self.setup_ui()
        self.toggle_always_on_top()
        
    def setup_ui(self):
        # Création des onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        # Onglet Timer
        self.timer_frame = ttk.Frame(self.notebook, style='Controls.TFrame')
        self.notebook.add(self.timer_frame, text='Timer')
        
        # Timer display
        self.time_label = ttk.Label(self.timer_frame, text="00:00", style='Timer.TLabel')
        self.time_label.pack(pady=20)
        
        # Control buttons frame
        control_frame = ttk.Frame(self.timer_frame)
        control_frame.pack(fill='x', padx=20)
        
        self.start_button = ttk.Button(control_frame, text="Démarrer", command=self.start_timer, width=15)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Arrêter", command=self.stop_timer, state='disabled', width=15)
        self.stop_button.pack(side='right', padx=5)
        
        # Onglet Paramètres
        self.settings_frame = ttk.Frame(self.notebook, style='Controls.TFrame')
        self.notebook.add(self.settings_frame, text='Paramètres')
        
        # Work time settings
        work_frame = ttk.LabelFrame(self.settings_frame, text="Temps de travail", padding=10)
        work_frame.pack(fill='x', padx=10, pady=5)
        
        self.work_time_input = ttk.Spinbox(work_frame, from_=1, to=120, width=10)
        self.work_time_input.set(25)
        ttk.Label(work_frame, text="minutes").pack(side='right', padx=5)
        self.work_time_input.pack(side='right')
        
        # Break time settings
        break_frame = ttk.LabelFrame(self.settings_frame, text="Temps de pause", padding=10)
        break_frame.pack(fill='x', padx=10, pady=5)
        
        self.break_time_input = ttk.Spinbox(break_frame, from_=1, to=30, width=10)
        self.break_time_input.set(5)
        ttk.Label(break_frame, text="minutes").pack(side='right', padx=5)
        self.break_time_input.pack(side='right')
        
        # Always on top option
        top_frame = ttk.LabelFrame(self.settings_frame, text="Options", padding=10)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        self.always_on_top_var = tk.BooleanVar(value=True)
        self.always_on_top = ttk.Checkbutton(
            top_frame, 
            text="Garder au premier plan",
            variable=self.always_on_top_var,
            command=self.toggle_always_on_top
        )
        self.always_on_top.pack()
        
    def start_timer(self):
        self.time_remaining = int(self.work_time_input.get()) * 60
        self.break_time = int(self.break_time_input.get()) * 60
        self.is_running = True
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.work_time_input.configure(state='disabled')
        self.break_time_input.configure(state='disabled')
        self.notebook.select(0)  # Retour à l'onglet Timer
        self.update_timer()
        
    def stop_timer(self):
        self.is_running = False
        self.start_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.work_time_input.configure(state='normal')
        self.break_time_input.configure(state='normal')
        self.time_label.configure(text="00:00", foreground='black')
        self.is_break = False
        
    def update_timer(self):
        if self.is_running and self.time_remaining >= 0:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            
            if self.time_remaining == 0:
                if not self.is_break:
                    notification.notify(
                        title="Work Timer",
                        message="Temps de travail terminé ! Prenez une pause.",
                        timeout=10
                    )
                    self.time_remaining = self.break_time
                    self.is_break = True
                    self.time_label.configure(foreground='green')
                else:
                    notification.notify(
                        title="Work Timer",
                        message="Pause terminée ! Reprenez le travail.",
                        timeout=10
                    )
                    self.stop_timer()
            else:
                self.time_remaining -= 1
                
            if self.is_running:
                self.root.after(1000, self.update_timer)
                
    def toggle_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = TimerWindow()
    app.run()