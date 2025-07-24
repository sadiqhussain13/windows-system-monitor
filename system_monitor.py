import psutil
import tkinter as tk
from tkinter import messagebox
from plyer import notification
import time
import threading

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("400x300")

        # Default thresholds
        self.cpu_threshold = 80.0
        self.memory_threshold = 80.0
        self.disk_threshold = 80.0

        # Flags to prevent repeated notifications
        self.cpu_notified = False
        self.memory_notified = False
        self.disk_notified = False

        # GUI Elements
        self.create_gui()

        # Start monitoring
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_system)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def create_gui(self):
        # Labels for displaying metrics
        tk.Label(self.root, text="CPU Usage:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.cpu_label = tk.Label(self.root, text="0.0%")
        self.cpu_label.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Memory Usage:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.memory_label = tk.Label(self.root, text="0.0%")
        self.memory_label.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Disk Usage:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.disk_label = tk.Label(self.root, text="0.0%")
        self.disk_label.grid(row=2, column=1, padx=10, pady=5)

        # Threshold input fields
        tk.Label(self.root, text="CPU Threshold (%):").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.cpu_entry = tk.Entry(self.root)
        self.cpu_entry.insert(0, str(self.cpu_threshold))
        self.cpu_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Memory Threshold (%):").grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.memory_entry = tk.Entry(self.root)
        self.memory_entry.insert(0, str(self.memory_threshold))
        self.memory_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Disk Threshold (%):").grid(row=5, column=2, padx=10, pady=5, sticky="w")
        self.disk_entry = tk.Entry(self.root)
        self.disk_entry.insert(0, str(self.disk_threshold))
        self.disk_entry.grid(row=5, column=1, padx=10, pady=5)

        # Update threshold button
        tk.Button(self.root, text="Update Thresholds", command=self.update_thresholds).grid(row=6, column=0, columnspan=2, pady=10)

        # Stop button
        tk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring).grid(row=7, column=0, columnspan=2, pady=10)

    def update_thresholds(self):
        try:
            self.cpu_threshold = float(self.cpu_entry.get())
            self.memory_threshold = float(self.memory_entry.get())
            self.disk_threshold = float(self.disk_entry.get())
            if not (0 <= self.cpu_threshold <= 100  and 0 <= self.memory_threshold <= 100 and 0 <= self.disk_threshold <= 100):
                 raise ValueError("Thresholds must be between 0 and 100.")
            self.cpu_notified = False
            self.memory_notified = False
            self.disk_notified = False
            messagebox.showinfo("Success", "Thresholds updates successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def monitor_system(self):
        while self.running:
            
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent
            disk_info = psutil.disk_usage('/')
            disk_usage = disk_info.percent

            # Update GUI
            self.cpu_label.config(text=f"{cpu_usage:.1f}%")
            self.memory_label.config(text=f"{memory_usage:.1f}%")
            self.disk_label.config(text=f"{disk_usage:.1f}%")

            # Check thresholds and send notifications
            if cpu_usage > self.cpu_threshold and not self.cpu_notified:
                notification.notify(
                    title="System Monitor Alert",
                    message=f"CPU usage exceeded threshold: {cpu_usage:.1f}%",
                    timeout=10
                )
                self.cpu_notified = True
            elif cpu_usage <= self.cpu_threshold:
                self.cpu_notified = False

            if memory_usage > self.memory_threshold and not self.memory_notified:
                notification.notify(
                    title="System Monitor Alert",
                    message=f"Memory usage exceeded threshold: {memory_usage:.1f}%",
                    timeout=10
                )
                self.memory_notified = True
            elif memory_usage <= self.memory_threshold:
                self.memory_notified = False

            if disk_usage > self.disk_threshold and not self.disk_notified:
                notification.notify(
                    title="System Monitor Alert",
                    message=f"Disk usage exceeded threshold: {disk_usage:.1f}%",
                    timeout=10
                    )
                self.disk_notified = True
            elif disk_usage <= self.disk_threshold:
                self.disk_notified = False 

            # Sleep to prevent exceesive CPU usage
            time.sleep(1)  

    def stop_monitoring(self):
        self.running = False
        self.root.quit()

def main():
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
