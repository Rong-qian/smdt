###############################################################################
#   File: tension.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 06 April, 2021
#
#   Purpose: This file houses the tension station class. This class stores the
#       data collected from the tension station into an object.
#
#   Known Issues:
#
#   Workarounds:
#   12-2021, RS: Update logic for first tension and second tension
#
###############################################################################
import datetime
import textwrap
from abc import ABC

from .record import Record
from .station import Station
from .status import Status


class TensionRecord(Record):
    """
    Class for objects representing individual records from the Tension station.
    """

    # Here are the project defined limits.
    max_tension = 350 + 15
    min_tension = 350 - 15

    def __init__(
            self,
            tension = None,
            frequency = None,
            date = datetime.datetime.now(),
            user = None
    ):
        super().__init__(user)
        self.tension = tension
        self.frequency = frequency
        self.date = date

    def fail(self):
        if self.tension is None:
            return True
        elif self.tension < TensionRecord.min_tension \
                or self.tension > TensionRecord.max_tension:
            return True
        else:
            return False

    def __str__(self):
        a = f"Tension: {self.tension}\n"
        b = f"Frequency: {self.frequency}\n"
        c = f"Recorded on: {self.date}\n"
        d = f"Recorded by: {self.user}\n\n"
        return a + b + c + d


class Tension(Station, ABC):
    """
    Class for objects representing individual records from the Tension station.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "Tension Data: " + self.status().name + "\n"
        b = ""

        # We want to print out each record.
        for record in sorted(
                self.m_records, key = lambda i: (i.date is None, i.date)
        ):
            b += record.__str__()

        b = b[:-1]

        # We want to have the return string indent each record, 
        # for viewing ease.
        return a + textwrap.indent(b, '\t') + '\n'

    def passed_first_tension(self):
        return any([not i.fail() for i in self.m_records if i is not None])

    # return the date on which the first first-tension test passed
    def first_tension_date(self):
        record = self.first_tension_record()
        if record is None:
            return None
        return record.date


    # return the complete tension record for the first first-tension test passed
    def first_tension_record(self):
        for record in sorted(
                self.m_records, key = lambda i: (i.date is None, i.date)
        ):
            if record is None:
                return None
            if not record.fail():
                return record
        return None

    # check if the second tension test (two weeks after the first one) passed
    def passed_second_tension(self):
        record = self.second_tension_record()
        if record is None:
            return False
        return not record.fail()

    
    # return the complete tension record for the second tension test passed
    def second_tension_record(self):
        if not self.passed_first_tension():
            return None
        first_date = self.first_tension_date()
        two_weeks = datetime.timedelta(days = 14)
        for record in sorted(
                self.m_records, key = lambda i: (i.date is None, i.date)
        ):
            if record is None:
                return None
            delta = record.date.date() - first_date.date()
            if not record.fail() and delta >= two_weeks:
                return record
        return None

    
    def status(self):
        if not self.visited():
            return Status.INCOMPLETE
        # if self.passed_second_tension():
        #    return Status.PASS
        # else:
        #    for record in sorted(self.m_records, key=lambda i: i.date):
        #        if not record.fail():
        #            three_weeks = datetime.timedelta(days=21)
        #            delta = datetime.datetime.now() - record.date
        #            if delta < three_weeks:
        #                return Status.INCOMPLETE
        #            else:
        #                break
        #    return Status.FAIL
        elif self.passed_first_tension():
            return Status.PASS
        else:
            return Status.FAIL

    def fail(self):
        return self.status() == Status.FAIL
