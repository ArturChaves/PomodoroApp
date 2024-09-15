import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import sys
import os


def resource_path(relative_path):
    
    try:
        
        base_path = sys._MEIPASS
    except AttributeError:
        
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PomodoroTimer:


    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.title("Pomodoro Timer")
        
        
        icon_path = resource_path("tomato.png")
        self.root.call('wm', 'iconphoto', self.root._w, PhotoImage(file=icon_path))

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))
        self.s.configure("TButton", font=("Ubuntu", 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab4 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoroTime = 25
        self.shortBreakTime = 5
        self.longBreakTime = 15

        self.pomodoroTimerLabel = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoroTimerLabel.pack(pady=20)

        self.shortBreakTimerLabel = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.shortBreakTimerLabel.pack(pady=20)

        self.longBreakTimerLabel = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.longBreakTimerLabel.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")
        self.tabs.add(self.tab4, text="Configs")

        self.gridLayout = ttk.Frame(self.root)
        self.gridLayout.pack(pady=10)

        self.startButton = ttk.Button(self.gridLayout, text="Start", command=self.startTimerThreads)
        self.startButton.grid(row=0, column=0)

        self.skipButton = ttk.Button(self.gridLayout, text="Skip", command=self.skipClock)
        self.skipButton.grid(row=0, column=1)

        self.resetButton = ttk.Button(self.gridLayout, text="Reset", command=self.resetClock)
        self.resetButton.grid(row=0, column=2)

        self.pomodoroCounterLabel = ttk.Label(self.gridLayout, text="Pomodoros: 0", font=("Ubuntu", 16))
        self.pomodoroCounterLabel.grid(row=1, column=0, columnspan=3, pady=10)


        self.configLayout = ttk.Frame(self.tab4)
        self.configLayout.pack(pady=20)

        ttk.Label(self.configLayout, text="Pomodoro Time (minutes):", font=("Ubuntu", 14)).grid(row=0, column=0, pady=5, padx=5)
        self.pomodoroTimeEntry = ttk.Entry(self.configLayout, width=5)
        self.pomodoroTimeEntry.insert(0, "25")
        self.pomodoroTimeEntry.grid(row=0, column=1)

        ttk.Label(self.configLayout, text="Short Break Time (minutes):", font=("Ubuntu", 14)).grid(row=1, column=0, pady=5, padx=5)
        self.shortBreakTimeEntry = ttk.Entry(self.configLayout, width=5)
        self.shortBreakTimeEntry.insert(0, "5")
        self.shortBreakTimeEntry.grid(row=1, column=1)

        ttk.Label(self.configLayout, text="Long Break Time (minutes):", font=("Ubuntu", 14)).grid(row=2, column=0, pady=5, padx=5)
        self.longBreakTimeEntry = ttk.Entry(self.configLayout, width=5)
        self.longBreakTimeEntry.insert(0, "15")
        self.longBreakTimeEntry.grid(row=2, column=1)

        self.saveConfigButton = ttk.Button(self.configLayout, text="Save", command=self.saveConfig)
        self.saveConfigButton.grid(row=3, column=0, columnspan=2, pady=10)

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.root.mainloop()


    def saveConfig(self):
        
        try:
            self.pomodoroTime = int(self.pomodoroTimeEntry.get())
            self.shortBreakTime = int(self.shortBreakTimeEntry.get())
            self.longBreakTime = int(self.longBreakTimeEntry.get())

            
            self.pomodoroTimerLabel.config(text=f"{self.pomodoroTime:02d}:00")
            self.shortBreakTimerLabel.config(text=f"{self.shortBreakTime:02d}:00")
            self.longBreakTimerLabel.config(text=f"{self.longBreakTime:02d}:00")
        except ValueError:
            print("Please enter valid integer values.")

    def force_window_to_top(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        position_x = int(screen_width / 2 - window_width / 2)
        position_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"+{position_x}+{position_y}")

        
    def on_tab_change(self, event):
        selected_tab = self.tabs.index(self.tabs.select())
        

        if selected_tab == 3:
            self.startButton.grid_remove()
            self.skipButton.grid_remove()
            self.resetButton.grid_remove()
            self.pomodoroCounterLabel.grid_remove()
        else:

            self.startButton.grid()
            self.skipButton.grid()
            self.resetButton.grid()
            self.pomodoroCounterLabel.grid()

    def startTimer(self):
        pomodoroTimer = self.pomodoroTime * 60
        shortBreakTimer = self.shortBreakTime * 60
        longBreakTimer = self.longBreakTime * 60

        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        self.running = True

        if timer_id == 1:

            while pomodoroTimer > 0 and not self.stopped:
                minutes, seconds = divmod(pomodoroTimer, 60)
                self.pomodoroTimerLabel.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                pomodoroTimer -= 1
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoroCounterLabel.configure(text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.force_window_to_top()
                self.startTimer()
        elif timer_id == 2:


            while shortBreakTimer > 0 and not self.stopped:
                minutes, seconds = divmod(shortBreakTimer, 60)
                self.shortBreakTimerLabel.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                shortBreakTimer -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.force_window_to_top()
                self.startTimer()
        elif timer_id == 3:            
            while longBreakTimer > 0 and not self.stopped:
                minutes, seconds = divmod(longBreakTimer, 60)
                self.longBreakTimerLabel.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                longBreakTimer -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.force_window_to_top()
                self.startTimer()
        else:
            print("Invalid timer id")      

    def startTimerThreads(self):
        if not self.running:
            t = threading.Thread(target=self.startTimer)
            t.start()
            self.running = True

    def resetClock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoroTimerLabel.config(text=f"{self.pomodoroTime:02d}:00")
        self.shortBreakTimerLabel.config(text=f"{self.shortBreakTime:02d}:00")
        self.longBreakTimerLabel.config(text=f"{self.longBreakTime:02d}:00")
        self.pomodoroCounterLabel.config(text="Pomodoros: 0")
        self.running = False
        self.tabs.select(0)
        

    def skipClock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomodoroTimerLabel.config(text=f"{self.pomodoroTime:02d}:00")
        elif current_tab == 1:
            self.shortBreakTimerLabel.config(text=f"{self.shortBreakTime:02d}:00")
        elif current_tab == 2:
            self.longBreakTimerLabel.config(text=f"{self.longBreakTime:02d}:00")

        self.stopped = True
        self.skipped = True

PomodoroTimer()
