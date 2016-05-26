#!/usr/bin/env python
from deepdive import *
from datetime import datetime, tzinfo, timedelta

#code below from:
#http://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
        return self.name

PST = Zone(-8, False, 'PST')

@tsv_extractor
@returns(lambda
        time = "int",
    :[])
def extract(
        created_utc = "text",
    ):

    time = datetime.strptime(created_utc, '%H')
    time = time.replace(tzinfo=PST)
    yield time
