import pickle

DEFAULT_SETTINGS = {
    'processSettings': {
    },
    'interactionIntensity': 1,
}

class SettingManager:
    def __init__(self):
        self.settings = {}
        try:
            with open('user_settings.pkl', 'rb') as file:
                self.settings = pickle.load(file)
        except (FileNotFoundError):
            self.settings = dict(DEFAULT_SETTINGS)
            

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value