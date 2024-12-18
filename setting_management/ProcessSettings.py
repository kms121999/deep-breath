

class ProcessSettings:
    def __init__(self, label, executable_name):
        self.label = label
        self.executable_name = executable_name

        # 0 is Monday, 6 is Sunday
        self.daily_limit = {
            0: TimeLimit(),
            1: TimeLimit(),
            2: TimeLimit(),
            3: TimeLimit(),
            4: TimeLimit(),
            5: TimeLimit(),
            6: TimeLimit()
        }

        # -1 means no limit
        self.session_limit = -1
        self.session_sliding_window = 5

        self.weekly_limit = WeekLimit()

        self.warning_time = -1

    def check_time_limit(self, state):
        pass


    
    def get_remaining_limit(self, trackedProcess, day):
        limits = []
        
        # Session
        if self.session_limit != -1:
            limits.append({
                "limitType": "session",
                "remaining": self.session_limit - trackedProcess.get_session_total()
                })

        # Day
        if self.daily_limit[day].time_limit != -1:
            limits.append({
                "limitType": "daily",
                "remaining": self.daily_limit[day].time_limit - trackedProcess.get_day_total()
                })
        
        # Week
        if self.weekly_limit.time_limit != -1:
            limits.append({
                "limitType": "weekly",
                "remaining": self.weekly_limit.time_limit - trackedProcess.get_week_total()
                })

        return min(limits, key = lambda x: x['remaining'])
    
    def bridge_session(self, sessionAEnd, sessionBStart):
        if sessionBStart - sessionAEnd <= self.session_sliding_window:
            return True
        else:
            return False

    def get_warning_time(self):
        return self.warning_time        
    
class TimeLimit:
    def __init__(self):
        # -1 means no limit
        self.time_limit = 2
        self.active = False

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

class WeekLimit(TimeLimit):
    def __init__(self):
        super().__init__()
        self.reset_day_time = {
            'day': 'monday',
            'time': '02:00'
        }