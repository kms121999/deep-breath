import pickle
import threading
from ProcessSettings import ProcessSettings

DEFAULT_SETTINGS = {
    "processSettings": {
    },
    "interactionIntensity": 1,
    "color": 'red',
    "notification_frequency_min": 5,
    "quotes": True,
    "goals": False

}

SETTINGS_FILE = 'data/user_settings.pkl'

class SettingManager:
    def __init__(self):
        # If you take both locks, you must take disk_lock first and then the other lock
        self.lock = threading.Lock()

        # Allows the in-memory lock to be released while writing to disk
        # This prevents tracker from being blocked while writing to disk
        self.disk_lock = threading.Lock()

        self.settings = {}
        with self.disk_lock:
            # Since settings is not populated, take the lock to prevent access to empty settings
            with self.lock:
                try:
                    with open(SETTINGS_FILE, 'rb') as file:
                        self.settings = pickle.load(file)
                except (FileNotFoundError):
                    self.settings = dict(DEFAULT_SETTINGS)
    
    def get_settings(self):
        with self.lock:
            return self.settings
    
    def set_settings(self, settings):
        with self.disk_lock:
            with self.lock:
                self.settings = settings

            with open(SETTINGS_FILE, 'wb') as file:
                pickle.dump(settings, file)

    def get(self, key):
        # Probably don't need this lock in practice
        with self.lock:
            return self.settings.get(key)
        
    def get_process(self, executable_name):
        with self.lock:
            return self.settings['processSettings'].get(executable_name)
        
    @staticmethod
    def addProcessSettings(settings, label, executable_name):
        process_settings = ProcessSettings(label, executable_name)
        settings['processSettings'][executable_name] = process_settings
        return settings