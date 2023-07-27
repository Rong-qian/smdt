###############################################################################
#   File: mini_tube.py
#   Author(s): Rongqian Qian
#   Date Created: 20 June, 2023
#
#   Purpose: This is the class representing a short tube for mini chamber.
#    an application will create these and store them in the database
#
#   Modifications:

###############################################################################


from .tube import Tube
from .data.position import Position

class Mini_tube(Tube):

    def __init__(self):
        super().__init__()
        self.position = Position()

    def __add__(self, other):
        ret = Mini_tube()
        #Tube.__add__(self,other)
        ret.position = self.position      
        ret.m_tube_id = self.m_tube_id
        ret.m_comments = self.m_comments + other.m_comments
        ret.swage = self.swage + other.swage
        ret.leak = self.leak + other.leak
        ret.dark_current = self.dark_current + other.dark_current
        ret.tension = self.tension + other.tension
        ret.bent = self.bent + other.bent
        ret.legacy_data = dict(self.legacy_data, **other.legacy_data)
        ret.position = self.position + other.position

        return ret

    def __str__(self):
        ret_str = Tube.__str__(self)
        ret_str += self.position.__str__()

        return ret_str
    
    def to_dict(self):
        #a dictionary of each station records
        #becomes a dictionary of all station records
        #becomes a dictionary for all tubes
        tube_in_dict = Tube.to_dict(self)
        position_station = dict()
        position_station['m_records'] = []

        for record in self.position.get_record('all'):
            record_dict = dict()
            record_dict["chamber"] = record.chamber
            record_dict["row"] = record.row
            record_dict["column"] = record.column
            record_dict["date"] = record.date
            record_dict["user"] = record.user
            position_station['m_records'].append(record_dict)

        tube_in_dict[self.m_tube_id]['position_station'] = position_station
        return tube_in_dict
        
