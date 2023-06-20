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


from .data.swage import Swage
from .data.tension import Tension
from .data.leak import Leak
from .data.dark_current import DarkCurrent
from .data.position import Position
from .data.status import Status, UMich_Status, ErrorCodes
from .data.bent import Bent
from .data.umich import UMich_Tension
from .data.umich import UMich_DarkCurrent
from .data.umich import UMich_Bent
from .data.umich import UMich_Misc
from .data.umich import UMich_Leak
from tube import Tube

class Mini_tube(Tube):

    def __init__(self):
        self.position = Position()

    def __add__(self, other):
        ret = Tube()
        ret.chamber = self.chamber
        ret.row = self.row
        ret.column = self.column        
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
        ret_str = ""
        if self.get_ID():

            # Checks for the status from UMich
            try:
                ret_str += self.get_ID() + '-' + ((self.status()).name or '') + ' / ' + (self.status_umich().name or '') + '\n'

            except:
                ret_str += self.get_ID() + '-' + (self.status().name or '') + '\n'
         

        date_str=self.get_mfg_date()
        if date_str != None:
            ret_str += 'Manufacture date ' +str(date_str) + '\n'
        else:
            ret_str += 'No information on manufacture date\n'
        if len(self.m_comments) != 0:
            ret_str += "\nComments:\n"
        for comment, user, date, error_code in self.m_comments:
            ret_str += (comment or '') \
                       + " -" \
                       + (user or '') \
                       + " " \
                       + (date.date().isoformat() if date is not None else '') \
                       + " " \
                       + (error_code.name or '') \
                       + '\n\n'

        if any([code != 0 for (h, e, y, code) in self.m_comments]):
            ret_str = ret_str[:-1]
            ret_str += "\nMARKED AS FAIL BY COMMENT\n\n"
        ret_str += self.swage.__str__()
        ret_str += self.tension.__str__()
        ret_str += self.leak.__str__()
        ret_str += self.bent.__str__()
        ret_str += self.dark_current.__str__()
        ret_str += self.position.__str__()

        return ret_str
    
    def to_dict(self):
        #a dictionary of each station records
        #becomes a dictionary of all station records
        #becomes a dictionary for all tubes
        tube_in_dict = dict()
        swager_station = dict()
        tension_station = dict()
        leak_station = dict()
        dark_current_station = dict()
        bentness_station = dict()
        position_station = dict()


        swager_station['m_records'] = []
        tension_station['m_records'] = []
        leak_station['m_records'] = []
        dark_current_station['m_records'] = []
        bentness_station['m_records'] = []
        position_station['m_records'] = []

        for record in self.swage.get_record('all'):
            record_dict = dict()
            record_dict['raw_length'] = record.raw_length
            record_dict['swage_length'] = record.swage_length
            record_dict['clean_code'] = record.clean_code
            record_dict['date'] = record.date
            record_dict['user'] = record.user
            swager_station['m_records'].append(record_dict)

        for record in self.tension.get_record('all'):
            record_dict = dict()
            record_dict["tension"] = record.tension,
            record_dict["frequency"] = record.frequency,
            record_dict["date"] = record.date,
            record_dict["user"] = record.user
            tension_station['m_records'].append(record_dict)
            
        for record in self.leak.get_record('all'):
            record_dict = dict()
            record_dict["leak_rate"] = record.leak_rate
            record_dict["date"] = record.date
            record_dict["user"] = record.user
            leak_station['m_records'].append(record_dict)
            
        for record in self.dark_current.get_record('all'):
            record_dict = dict()
            record_dict["dark_current"] = record.dark_current
            record_dict["date"] = record.date
            record_dict["voltage"] = record.voltage
            record_dict["user"] = record.user
            dark_current_station['m_records'].append(record_dict)

        for record in self.bent.get_record('all'):
            record_dict = dict()
            record_dict["bentness"] = record.bentness
            record_dict["date"] = record.date
            record_dict["user"] = record.user
            bentness_station['m_records'].append(record_dict)

        for record in self.position.get_record('all'):
            record_dict = dict()
            record_dict["chamber"] = record.chamber
            record_dict["row"] = record.row
            record_dict["column"] = record.column
            record_dict["date"] = record.date
            record_dict["user"] = record.user
            tension_station['m_records'].append(record_dict)

        tube_data_dict = dict()

        tube_data_dict['swage_station'] = swager_station
        tube_data_dict['tension_station'] = tension_station
        tube_data_dict['leak_station'] = leak_station
        tube_data_dict['dark_current_station'] = dark_current_station
        tube_data_dict['position_station'] = position_station


        tube_in_dict[self.m_tube_id] = tube_data_dict


        return tube_in_dict

    # Small tubes are not made in MSU
    def made_at_umich(self):
        return False
        