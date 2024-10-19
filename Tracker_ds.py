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


    def minus_to_SDW(self, exe, key):
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
                application_info[key] -= 1
            else:
                application_info[key] = None
            return [key, application_info[key]]
        return [key, None]
    
    def remove_none_values(self, list_SDW_val):
        '''
        :arg list_SDW_val: (list of list)
        :fun: (RETURNS: This function removes sub lists in list_SDW_val that
            contain None in their idex of 1)
        '''
        no_nones = []
        for val in list_SDW_val:
            if val[1] is not None:
                no_nones.append(val)
        return no_nones
    
    def find_min_SDW(self, list_SDW_val):
        '''
        :arg list_SDW_val: (list of list)
        :fun: (RETURNS a sub list that is in list_SDW_val that has the lowest
            value in its index of 1)
        '''
        if list_SDW_val[0] is not None:
            curr_min = list_SDW_val[0]
            for val in list_SDW_val:
                if val[1] < curr_min[1]:
                    curr_min = val
            return curr_min
        else:
            return []
    
    def update_tallies(self, exe):
        '''
        :arg exe: (string) This is the exe string name
        :fun: (returns the lowest tally with tally type, for example [
            "daily_tally", 3]) (This function will also minus 1 to all the 
            tallies in the exe's dictionary of tallies unless they are None
            values.)
        '''
        tally_values = []
        for my_key in self.keys:
            updated_SDW = self.minus_to_SDW(exe, my_key)
            tally_values.append(updated_SDW)

        removed_none_tallies = self.remove_none_values(tally_values)
        min_tally = self.find_min_SDW(removed_none_tallies)
        return min_tally

