#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ License 
##~ 
##- The RuneBlade Foundation library is intended to ease some 
##- aspects of writing intricate Jabber, XML, and User Interface (wxPython, etc.) 
##- applications, while providing the flexibility to modularly change the 
##- architecture. Enjoy.
##~ 
##~ Copyright (C) 2002  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~ 
##~ TechGame Networks, LLC can be reached at:
##~ 3578 E. Hartsel Drive #211
##~ Colorado Springs, Colorado, USA, 80920
##~
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Subject/Observer like implementation of sched"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import bisect, time
from Foundation import WeakBind

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SchedulerSubject(object):
    def __init__(self, TimeFn=time.time):
        self._TimeFn = WeakBind.BindCallable(TimeFn)
        self._LastTime = 0
        self._events = []
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Management 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def AddRelativeEvent(self, Time, observer):
        return self.AddEvent(Time + self._TimeFn(), observer)

    def AddEvent(self, Time, observer):
        result = Time, WeakBind.BindCallable(observer)
        bisect.insort(self._events, result)
        return self

    def RemoveEvent(self, observer):
        result = WeakBind.BindCallable(observer)
        self._events[:] = [x for x in self._events if x[-1] != result]
        return self

    def ClearEvents(self):
        self._events[:] = []
        return self

    def Process(self, Time=None, LastTime=None):
        if Time is None: Time = self._TimeFn()
        LastTime, self._LastTime = self._LastTime, Time
        return self.ProcessTimeWindow(LastTime, Time)

    def ProcessTimeWindow(self, StartTime, StopTime):
        result = []
        for each in self._events:
            if each[0] < StartTime: pass
            elif each[0] <= StopTime:
                if each[1]: each[1](self, StopTime, each[0])
            else: result.append(each)

        self._events = result
        return self._events and (self._events[-1][0] > StopTime)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RecuringSchedulerSubject(SchedulerSubject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Update Callbacks
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    def Reset(self, LastTime=0):
        self._LastTime = LastTime

    def ProcessTimeWindow(self, StartTime, StopTime):
        result = []
        for each in self._events:
            if each[0] < StartTime: continue
            elif each[0] <= StopTime:
                if each[1]: each[1](self, StopTime, each[0])
            else: break

        return self._events and (self._events[-1][0] > StopTime)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_SchedulerSubject():
    def printTime(scheduler, Time, EventTime):
        print
        print 'The time is now', time.ctime(Time), 
        if Time - EventTime  > 0.01: 
            print 'but was late by', Time - EventTime
        else: print
        
    print
    print "Testing time.time scheduler"
    print
    printTime(None, time.time(), time.time())

    TimeSch = RecuringSchedulerSubject()
    TimeSch.AddRelativeEvent(1.0, printTime)
    TimeSch.AddRelativeEvent(2.0, printTime)
    TimeSch.AddRelativeEvent(4.0, printTime)
    TimeSch.AddRelativeEvent(8.0, printTime)

    while TimeSch.Process():
        time.sleep(0.2)
        print '.',
        
    print "Do it Again?"
    TimeSch.Reset()

    while TimeSch.Process():
        time.sleep(0.2)
        print '.',
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print
    print "Testing tick scheduler"
    print

    def printTime(scheduler, tick, EventTime):
        print 'The tick is now', tick,
        if tick - EventTime > 0: 
            print 'but was scheduled for', EventTime
        else: print
        
    global nTime
    nTime = 0
    def gettime(): return nTime
    
    TickSch = RecuringSchedulerSubject(gettime)
    TickSch.AddRelativeEvent(5, printTime)
    TickSch.AddRelativeEvent(20, printTime)
    TickSch.AddRelativeEvent(40, printTime)

    while TickSch.Process():
        nTime += 1
        print '.',
    print "Doubletime!"
    nTime = 0
    TickSch.Reset()
    while TickSch.Process():
        nTime += 2
        print '.',

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    _Test_SchedulerSubject() 
    print "Test complete."

