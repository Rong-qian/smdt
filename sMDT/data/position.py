###############################################################################
#   File: position.py
#   Author(s): Rongqian Qian
#   Date Created: 19 Jun3, 2023
#
#   Purpose: This file houses the position station class. This class stores the
#       data collected from the position station into an object.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################
from abc import ABC
from datetime import datetime
import textwrap

from .station import Station
from .status import Status
from .record import Record


class PositionRecord(Record):
    """
    Class for objects representing individual records from the Position station.
    """

    # Does this format for a long list of parameters look cleaner?
    def __init__(
        self, 
        chamber = None,
        row = None,
        column = None,
        date=datetime.now(), 
        user=None
    ):

        # Call the super class init to construct the object.
        super().__init__(user)
        self.chamber  = chamber
        self.row = row 
        self.column = column
        self.date = date

    def fail(self):
        # Tubes, at this point in time, are not going to be failed on the basis
        # of chamber position.
        return False
        
    def __str__(self):
        # Using string concatenation here.
        a = f"Tube is in Chamber: {self.chamber}\n"
        b = f"Row: {self.row}\n"
        c = f"Column: {self.column}\n"
        d = f"Recorded on: {self.date}\n"
        e = f"Recorded by: {self.user}\n\n"

        return_str = a + b + c + d + e
        return return_str


class Position(Station, ABC):
    """
    The Position station class, manages the relevant records for a particular tube.
    """
    def __init__(self): 
        Station.__init__(self)

    def __str__(self):
        a = "Position Data: " + (self.status().name or '') + "\n"
        b = ""

        # We want to print out each record.
        for record in sorted(
                self.m_records, key=lambda i: (i.date is None, i.date)
        ):
            b += record.__str__()

        b = b[:-1]

        # We want to have the return string indent each record, for 
        # viewing ease.
        return a + textwrap.indent(b, '\t') + '\n'
    
    def fail(self):
        if not self.visited():
            return False

        return self.get_record(mode='last').fail()

    def status(self):
        if not self.visited():
            return Status.INCOMPLETE
        elif self.fail():
            return Status.FAIL
        else:
            return Status.PASS
