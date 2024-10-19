class tally_ds():
    def __init__(self):
        self.my_df = {}
        self.keys = ["session_tally", "daily_tally", "weekly_tally"]

    def add_exe(self, exe, session_amount = None, daily_amount = None, weekly_amount = None):
        '''
        :arg exe: (string) (This is the exe name)
        :arg session_amount: (int)
        :arg daily_amount: (int)
        :arg weekly_amount: (int)
        :fun: (Adds a dictionary of the values above into the self.my_df dict)
        '''
        self.my_df[exe] = {
            "session_tally": session_amount,
            "daily_tally": daily_amount,
            "weekly_tally": weekly_amount 
        }


    def add_to_SDW(self, exe, key):
        '''
        :arg exe: (string) This is the exe of a file.
        :arg key: (string) This is either "session_tally", "daily_tally"
            or "weekly_tally".
        :fun: Finds the daily, weekly, or session for the specified exe, and
        it deletes 1 to the values.
        '''
        application_info = self.my_df[exe]
        if application_info[key] is not None :
            if application_info[key] != 0:
                application_info[key] += 1
            else:
                application_info[key] = None
            return [key, application_info[key]]
        return [key, None]
    
    def update_tallies(self, exe):
        '''
        :arg exe: (string) This is the exe string name
        :fun: (This function will also add 1 to all the 
            tallies in the exe's dictionary of tallies unless they are None
            values.)
        '''
        if exe in self.my_df:
            for my_key in self.keys:
                self.add_to_SDW(exe, my_key)
        else:
            self.add_exe(exe, 0, 0, 0, 0)

    def get_exe_SDW(self, exe):
        '''
        Given the exe name this returns all the tallies for it.
        '''
        return self.my_df[exe]
    
    def get_session_value(self, exe):
        '''
        Given the exe name this returns the session tally.
        '''
        return self.my_df[exe]["session_tally"]
    
    def get_daily_value(self, exe):
        '''
        Given the exe name this returns the daily tally.
        '''
        return self.my_df[exe]["daily_tally"]

    def get_weekly_value(self, exe):
        '''
        Given the exe name this returns the weekly tally.
        '''
        return self.my_df[exe]["weekly_tally"]
    

