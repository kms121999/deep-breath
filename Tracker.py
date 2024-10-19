import psutil
from datetime import datetime
import time
import os

class Tracker():
    def __init__(self):
        self.monitored_processes = {}
        self.running = True
        self.single_tick = 5.0

    def add_monitored_process(self,name, dictionary):
        self.monitored_processes[name] = dictionary

    def edit_monitored_process():
        ...

    def update_monitored_processes(self, processes):
        
        for process in processes:
            # If the process is in our list of monitored processes, we will update it's time
            if process.name() in self.monitored_processes.keys() and self.monitored_processes[process.name()]["updated"] == False:
                self.monitored_processes[process.name()]["time"] += 1
                self.monitored_processes[process.name()]["updated"] = True
                print(self.monitored_processes[process.name()]["time"])

        self.update_reset(self.monitored_processes)

    def check_limit_status(self):
        for process in self.monitored_processes.items():
            if process[1]['time'] == process[1]['session_limit']:
                os.system(f'taskkill /f /im {process[0]}')
                print("User notification of session expiration")

    def update_reset(self, monitored_processes):
        """
        the 'updated' key in monitored_process makes sure that a monitored process isn't tallied multiple times due to
        multiple processes running on the task manager. 'update_reset' resets all values to false
        before the next iteration :).
        """
        for process in monitored_processes.items():
            process[1]["updated"] = False

    def tick(self):
        """
        A tick is a single iteration of a loop within a set time.
        """
        while self.running:
            # Wait a minute
            time.sleep(self.single_tick)
            # Get list of active processes
            processes = psutil.process_iter()
            # Update the time of all monitored processes
            self.update_monitored_processes(processes)
            # Check if the user has exceeded their time limit
            self.check_limit_status()


tracker = Tracker()
tracker.add_monitored_process("chrome.exe", {"time" : 0, "start_time" : 0, "session_limit" : 1, "updated" : False})
# tracker.add_monitored_process("league.exe", {"time" : 0, "start_time" : 0, "session_limit" : 5, "updated" : False})

tracker.tick()

# print(monitored_processes["chrome.exe"]["time"])
# # Get list of active processes
# for process in psutil.process_iter():
#     if process.name() in and monitored_processes[process.name()]["updated"] == False:
#         monitored_processes[process.name()]["time"] += 1
#         monitored_processes[process.name()]["updated"] = True

# update_reset()

# print(monitored_processes["chrome.exe"]["time"])


