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

"""State machine implementation using the Subject/Observer design pattern.

By defining each state as a subject, the state can "call you back" in order to
compute complext firing semantics, or when the state is reached.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from CategorySubject import CategorySubject 
from operator import and_, or_

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OrStateList(list):
    def __int__(self):
        for each in self:
            if each.GetState(): 
                return 1
        return 0

    def SetHandled(self):
        for each in self:
            if each.GetState(): 
                each.SetHandled()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AndStateList(list):
    def __int__(self):
        for each in self:
            if not each.GetState(): 
                return 0
        if self: return 1
        else: return 0

    def SetHandled(self):
        for each in self:
            if each.GetState(): 
                each.SetHandled()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StateSubject(CategorySubject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    value = 0
    incvalue = 1
    precondition = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def __init__(self, InfluxsClass=AndStateList, **kw):
        self.__dict__.update(kw)
        CategorySubject.__init__(self)
        self._Influxs = InfluxsClass()

    def __int__(self):
        return self.GetState()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GetState(self):
        return self.value

    def SetState(self, value=None):
        if value is None: value = self.incvalue
        if self.value != value:
            self.value = value 

            result = self.PushState()

            return result

    def PushState(self):
        if self.value and not self._Influxs:
            self.UpdateObservers(precondition=self.value)

        self.UpdateObservers(state=self)

        return self.GetState()

    def SetHandled(self, handled=1):
        self.SetState(max(self.value-handled, 0))

    def CheckInfluxs(self, subject, state):
        if state and not self.value and not self.precondition:
            self.precondition = int(self._Influxs)
            if self.precondition:
                self.__publishing = 0
                self.preconditionlock = self.Lock()
                self.UpdateObservers(precondition=self.precondition)

    __publishing = 0
    def PublishSet(self, subject, state):
        if self.precondition and not self.__publishing:
            self.__publishing = 1
            self._Influxs.SetHandled()
            self.preconditionlock.SetLock(None)
            del self.preconditionlock
            self.precondition = None
        
    def AddInflux(self, Influx):
        self._Influxs.append(Influx)
        Influx.AddObserver('state', self.CheckInfluxs, priority=-1)
        Influx.AddObserver('state', self.PublishSet, priority=-2)

    def AddOutflux(self, Outflux):
        Outflux.AddInflux(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class State(StateSubject):
    """NOTE: This class is for backward compatability!!!  Please use StateSubject instead."""

    def SetHandled(self, handled=1):
        pass 

    def AddInflux(self, Influx):
        self._Influxs.append(Influx)
        # Reverse the order of callable and category for legacy support
        Influx.AddObserver(self.CheckInfluxs, 'state', priority=-1)
        Influx.AddObserver(self.PublishSet, 'state', priority=-2)

    def AddObserver(self, callable, category='', **kw):
        # Reverse the order of callable and category for legacy support
        category = category or 'precondition'
        return CategorySubject.AddObserver(self, category, callable, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_StateMachine():
    from Foundation.ContextApply import ContextApply_s_p,ContextApply_0
    def PrintDescription(State, precondition):
        print State.__doc__
        #State.SetState()

    a = State(__doc__="A")
    a.AddObserver(ContextApply_0(a.SetState))
    a.AddObserver(PrintDescription)
    b = State(__doc__="B")
    b.AddObserver(ContextApply_0(b.SetState))
    b.AddObserver(PrintDescription)
    c = State(__doc__="C")
    c.AddObserver(ContextApply_0(c.SetState))
    c.AddObserver(PrintDescription)
    d = State(__doc__="D")
    d.AddObserver(ContextApply_0(d.SetState))
    d.AddObserver(PrintDescription)

    b.AddInflux(a)
    c.AddInflux(b)
    d.AddInflux(b)
    d.AddInflux(c)

    a.SetState()
    assert d.GetState()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    _Test_StateMachine() 

