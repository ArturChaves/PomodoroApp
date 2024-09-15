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
        self.root.geometry("600x300")
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

        self.pomodoroTimerLabel = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoroTimerLabel.pack(pady=20)

        self.shortBreakTimerLabel = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.shortBreakTimerLabel.pack(pady=20)

        self.longBreakTimerLabel = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.longBreakTimerLabel.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

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

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.root.mainloop()

    def startTimer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        self.running = True

        if timer_id == 1:
            fullSeconds = 60 * 25

            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                self.pomodoroTimerLabel.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullSeconds -= 1
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoroCounterLabel.configure(text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.startTimer()
        elif timer_id == 2:
            fullSeconds = 60 * 5

            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                self.shortBreakTimerLabel.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullSeconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.startTimer()
        elif timer_id == 3:
            fullSeconds = 60 * 15

            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                self.longBreakTimerLabel.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullSeconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
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
        self.pomodoroTimerLabel.config(text="25:00")
        self.shortBreakTimerLabel.config(text="05:00")
        self.longBreakTimerLabel.config(text="15:00")
        self.pomodoroCounterLabel.config(text="Pomodoros: 0")
        self.running = False
        self.tabs.select(0)
        

    def skipClock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomodoroTimerLabel.config(text="25:00")
        elif current_tab == 1:
            self.shortBreakTimerLabel.config(text="05:00")
        elif current_tab == 2:
            self.longBreakTimerLabel.config(text="15:00")
        
        self.stopped = True
        self.skipped = True

PomodoroTimer()
