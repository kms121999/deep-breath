import psutil
from datetime import datetime
import time
import os
from notifications.Notification import Notification
from setting_management.SettingManager import SettingManager
from Tracker_ds import tally_ds

class Tracker():
    """
    Tracker is a data structure that sets the pace for our program. Tracker holds the loop that keeps
    the program looping a single minute at a time.
    """
    def __init__(self):
        self.tally = tally_ds()
        self.setting_manager = SettingManager()
        self.monitored_processes = {}
        self.running = True
        self.single_tick = 5.0
        self.Notification = Notification()

    def add_monitored_process(self,name, dictionary):
        self.monitored_processes[name] = dictionary

    def check_reset_times(self, reset_time):
        if datetime.weekday(datetime.now()) == reset_time["day"] and datetime.now().hour == reset_time["hour"] or\
            datetime.now().hour == reset_time["day"]:
            for process in self.monitored_processes.items():
                process[1]["time"] = 0
                self.monitored_processes[process[0]]["updated"] = False

    def update_monitored_processes(self, processes):
        
        for process in processes:
            if process.name() not in self.monitored_processes.keys():
                self.monitored_processes[process.name()] = {"time" : 0, "updated" : False}

            if self.monitored_processes[process.name()]["updated"] == False:

                self.monitored_processes[process.name()]["time"] += 1
                self.monitored_processes[process.name()]["updated"] = True

        self.update_reset(self.monitored_processes)

    def check_limit_status(self, processes):
        """
        This function checks to see if the monitored processes time use exceeds certain limits.
        Here is where it is decided on how to handle the user :)
        """
        for process in processes:
            process_settings = self.setting_manager.get_process(process.name())

            # If the remaining limit is 0
            if process_settings.get_remaining_limit(process.name(), datetime.weekday(datetime.now())) == 0:
                # Here is where the process is killed
                # os.system(f'taskkill /f /im {process[0]}')
                ...

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
            self.check_limit_status(processes)
            # Checks to see if limits need a reset
            self.check_reset_times(self.setting_manager.get("reset_times"))

            print(self.monitored_processes["chrome.exe"])
            # Display handy notification
            self.Notification.get_quote_api('happiness')



tracker = Tracker()
tracker.add_monitored_process("chrome.exe", {"time" : 0, "updated" : False})

tracker.tick()

# print(monitored_processes["chrome.exe"]["time"])
# # Get list of active processes
# for process in psutil.process_iter():
#     if process.name() in and monitored_processes[process.name()]["updated"] == False:
#         monitored_processes[process.name()]["time"] += 1
#         monitored_processes[process.name()]["updated"] = True

# update_reset()

# print(monitored_processes["chrome.exe"]["time"])


