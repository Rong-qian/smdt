Swage Module Documentation
==========================

[sMDT](sMDT.md).[data](data.md).position is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Position Station. 

This module has two main classes, the Position object, and the PositionRecord object. The Position object is a [Station](station.md) that holds a list of PositionRecords.

Position Station Object
--------------------

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|None|None|Constructs the swage station object
status()|None|[Status](status.md)|Returns Status.INCOMPLETE if there is no records. If there are records, the last one is checked. If it is a failure based of it's fail() function, then this returns Status.FAIL. Otherwise, returns Status.PASS
\_\_str\_\_()|None|string|Returns a string representation of the station, includes printing each of it's records.

PositionRecord Object
------------------
position.PositionRecord is the [Record](record.md) object that stores a single instance of data from the swage station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Member variables|Units|Description
---|---|---
chamber | None| The index of the mini chamber which the tube will be installed in. 
row | None | The number of the row in the mini chamber of the tube (start from 1 for the leftmost tube)
column | None | The number of the column in the mini chamber of the tube (start from 1 for the uppermost tube)
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|chamber : int, row : int, column: int, date : datetime, user : string| SwageRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for the failure condition. 

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import position
position_station = position.Position()                                                #instantiate swage station object
position_station.add_record(position.PositionRecord(chamber=1, row=1, column=1))
print(position_station.get_record("first"))                                     #print the first Position Reocrd
print(position_station.fail("last"))                                            #print wether the tube fails based on the last record.
