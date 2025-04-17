import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

# Scheduling Algorithms
class CPUScheduler:
    def __init__(self, processes):
        self.processes = processes
    
    def fcfs(self):
        self.processes.sort(key=lambda x: x[1])  # Sort by Arrival Time
        start_time, waiting_time, turnaround_time = 0, [], []
        gantt_chart = []
        for pid, at, bt, _ in self.processes:
            start_time = max(start_time, at)
            wt = start_time - at
            tat = wt + bt
            waiting_time.append(wt)
            turnaround_time.append(tat)
            gantt_chart.append((pid, start_time, start_time + bt))
            start_time += bt
        return waiting_time, turnaround_time, gantt_chart

    def sjf(self):
        self.processes.sort(key=lambda x: (x[1], x[2]))  # Sort by Arrival Time, then Burst Time
        start_time, waiting_time, turnaround_time = 0, [], []
        gantt_chart = []
        for pid, at, bt, _ in self.processes:
            start_time = max(start_time, at)
            wt = start_time - at
            tat = wt + bt
            waiting_time.append(wt)
            turnaround_time.append(tat)
            gantt_chart.append((pid, start_time, start_time + bt))
            start_time += bt
        return waiting_time, turnaround_time, gantt_chart

    def round_robin(self, quantum=2):
        queue = self.processes[:]
        start_time, waiting_time, turnaround_time = 0, {}, {}
        gantt_chart = []
        remaining_time = {pid: bt for pid, at, bt, _ in self.processes}
        
        while queue:
            pid, at, bt, _ = queue.pop(0)
            if remaining_time[pid] > quantum:
                gantt_chart.append((pid, start_time, start_time + quantum))
                remaining_time[pid] -= quantum
                start_time += quantum
                queue.append((pid, at, bt, _))
            else:
                gantt_chart.append((pid, start_time, start_time + remaining_time[pid]))
                start_time += remaining_time[pid]
                waiting_time[pid] = start_time - at - bt
                turnaround_time[pid] = waiting_time[pid] + bt
                remaining_time[pid] = 0
        return waiting_time, turnaround_time, gantt_chart

# GUI Setup
class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler Simulator")
        
        # Input Table
        self.process_list = []
        self.tree = ttk.Treeview(root, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
        for col in ["PID", "Arrival", "Burst", "Priority"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        self.tree.pack()
        
        # Controls
        self.add_process_button = tk.Button(root, text="Add Process", command=self.add_process)
        self.run_fcfs_button = tk.Button(root, text="Run FCFS", command=self.run_fcfs)
        self.run_sjf_button = tk.Button(root, text="Run SJF", command=self.run_sjf)
        self.run_rr_button = tk.Button(root, text="Run Round Robin", command=self.run_rr)
        self.add_process_button.pack()
        self.run_fcfs_button.pack()
        self.run_sjf_button.pack()
        self.run_rr_button.pack()
        
    def add_process(self):
        new_window = tk.Toplevel(self.root)
        tk.Label(new_window, text="PID").grid(row=0, column=0)
        tk.Label(new_window, text="Arrival Time").grid(row=1, column=0)
        tk.Label(new_window, text="Burst Time").grid(row=2, column=0)
        tk.Label(new_window, text="Priority").grid(row=3, column=0)
        
        pid = tk.Entry(new_window)
        arrival = tk.Entry(new_window)
        burst = tk.Entry(new_window)
        priority = tk.Entry(new_window)
        pid.grid(row=0, column=1)
        arrival.grid(row=1, column=1)
        burst.grid(row=2, column=1)
        priority.grid(row=3, column=1)
        
        def save_process():
            self.process_list.append((pid.get(), int(arrival.get()), int(burst.get()), int(priority.get())))
            self.tree.insert("", "end", values=(pid.get(), arrival.get(), burst.get(), priority.get()))
            new_window.destroy()
        
        tk.Button(new_window, text="Add", command=save_process).grid(row=4, column=1)
    
    def run_fcfs(self):
        self.run_algorithm("FCFS")
    
    def run_sjf(self):
        self.run_algorithm("SJF")
    
    def run_rr(self):
        self.run_algorithm("Round Robin")
    
    def run_algorithm(self, algo):
        if not self.process_list:
            messagebox.showerror("Error", "No processes added!")
            return
        
        scheduler = CPUScheduler(self.process_list)
        if algo == "FCFS":
            _, _, gantt_chart = scheduler.fcfs()
        elif algo == "SJF":
            _, _, gantt_chart = scheduler.sjf()
        elif algo == "Round Robin":
            _, _, gantt_chart = scheduler.round_robin()
        
        # Display Gantt Chart
        fig, ax = plt.subplots()
        for pid, start, end in gantt_chart:
            ax.broken_barh([(start, end - start)], (10, 5), facecolors=('blue'))
            ax.text((start + end) / 2, 12, f"P{pid}", ha='center', va='center', color='white')
        ax.set_xlabel("Time")
        ax.set_yticks([])
        plt.show()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
