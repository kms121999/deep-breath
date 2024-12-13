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
        self.Tally_ds = tally_ds()

    def add_monitored_process(self,name, dictionary):
        self.monitored_processes[name] = dictionary

    def check_reset_times(self, reset_time):
        now = datetime.now()
        curr_date = now.date()
        curr_day = now.date
        curr_month = now.month
        curr_year = now.year
        file_path = 'date.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r+') as file:
                # Get the info from the file
                last_date = file.read()
                date_list = []
                for section in last_date:
                    date_list.append(section)
                last_year = date_list[0]
                last_month = date_list[1]
                last_day = date_list[2]
                # Logic
                if last_year == str(curr_year):
                    
                    if last_month == str(curr_month):
                        
                        if last_day != str(curr_day):
                            self.Tally_ds.reset_tally("daily_tally")
                            file.truncate(0)
                            file.write([curr_year, curr_month, curr_day])



        if datetime.weekday(datetime.now()) == reset_time["day"] and datetime.now().hour == reset_time["hour"] or\
            datetime.now().hour == reset_time["day"]:
            for process in self.monitored_processes.items():
                process[1]["time"] = 0
                self.monitored_processes[process[0]]["updated"] = False

    def update_monitored_processes(self, processes):
        
        for process in processes:
            exe = process.name() # the process name as a string
            if exe not in self.monitored_processes.keys():
                self.monitored_processes[exe] = {"time" : 0, "updated" : False}

            if self.monitored_processes[exe]["updated"] == False:
                self.monitored_processes[exe]["time"] += 1
                # print(f'!!!!!!!!!!!!!!!!!!!! {exe}')
                self.Tally_ds.update_tallies(exe)
                self.monitored_processes[exe]["updated"] = True
            # print(process)
        self.update_reset(self.monitored_processes)

    def check_limit_status(self, processes):
        """
        This function checks to see if the monitored processes time use exceeds certain limits.
        Here is where it is decided on how to handle the user :)
        """
        # print('WQHATAEKL SKLE JSEKJ ')
        for process in processes:
            # print('YOU NEED TO WORK')
            process_settings = self.setting_manager.get_process(process.name())

            # If the remaining limit is 0
            # print("________________________________________________________Process Settings")
            if process_settings:
                # print("________________________________________________________________________ALKJDF S")
                if process_settings.daily_limit[0].time_limit <= self.monitored_processes[process.name()]['time']:
                    self.Notification.create_notification("You've been on too long!!")
                    ...
                # Here is where the process is killed
                # os.system(f'taskkill /f /im {process[0]}')

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
            # print(len(processes))
            # Update the time of all monitored processes
            self.update_monitored_processes(psutil.process_iter())
            # Check if the user has exceeded their time limit
            self.check_limit_status(psutil.process_iter())
            # Checks to see if limits need a reset
            self.check_reset_times(self.setting_manager.get("reset_times"))

            # print(self.monitored_processes["chrome.exe"])
            # Display handy notification
            self.Notification.get_quote_api('happiness')
