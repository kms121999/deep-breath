import psutil
from datetime import datetime

class Tracker():
    def __init__(self):
        self.monitored_processes = {}

    def add_monitored_process(self,name, dictionary):
        self.monitored_processes[name] = dictionary
        ...

    def edit_monitored_process():
        ...

    def update_time_spent():
        ...

    def check_limit_status_of_monitored_procecsses(self):
        for process in self.monitored_processes.items():
            if process[1]['time'] > process[1]['session_limit'] or \
                process[1]['time'] > process[1]['daily_limit']:
                print("User notification of session expiration")
        ...

    def update_reset(self):
        for process in self.monitored_processes.items():
            process[1]["updated"] = False

    def minute_loop():

    ...


tracker = Tracker()
tracker.add_monitored_process("chrome.exe", {"time" : 0, "start_time" : 0, "updated" : False})
tracker.add_monitored_process("chrome.exe", {"time" : 0, "start_time" : 0, "updated" : False})


print(monitored_processes["chrome.exe"]["time"])
# Get list of active processes
for process in psutil.process_iter():
    if process.name() in and monitored_processes[process.name()]["updated"] == False:
        monitored_processes[process.name()]["time"] += 1
        monitored_processes[process.name()]["updated"] = True

update_reset()

print(monitored_processes["chrome.exe"]["time"])


