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

"""Adds 'categories' to subjects to allow for prefiltering of subject
notifications.  Simply put, you have to add an observer for a specific
category, and that observer will only be called when that category is 
updated."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Subject import Subject
from Foundation import WeakBind
import bisect

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CategorySubjectBaseMixin(object):
    def __init__(self):
        super(CategorySubjectBaseMixin, self).__init__()
        self._observers = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Management 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def AddObserver(self, category, observer, priority=0):
        result = WeakBind.BindCallable(observer)
        bisect.insort(self._observers.setdefault(category,[]), (-priority, result))
        return self

    def RemoveObserver(self, observer):
        result = WeakBind.BindCallable(observer)
        for observers in self._observers.itervalues():
            observers[:] = [x for x in observers if x[-1] != result]
        return self

    def ClearObservers(self):
        self._observers[:] = []
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Update Callbacks
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    def _ObserverList(self, category):
        observers = self._observers.setdefault(category, [])
        observers[:] = [x for x in observers if x[-1]]
        return [x[-1] for x in observers]
    def _AllObserversList(self):
        return [x[-1] for y in self._observers.values() for x in y]
    Observers = property(_AllObserversList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CategorySubjectMixin(CategorySubjectBaseMixin):
    def UpdateObserversEx(self, kw):
        self._cachedUpdates.update(kw)
        if self._cachedUpdates and not self._locked:
            _cachedUpdates, self._cachedUpdates = self._cachedUpdates, {}
            lock = self.Lock()
            for category, value in _cachedUpdates.iteritems():
                for each in self._ObserverList(category):
                    if isinstance(category, tuple):
                        self.UpdateObserver(each, {category[0]: value})
                    else: self.UpdateObserver(each, {category: value})
            return 1
        else: return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CategorySubject(CategorySubjectMixin, Subject):
    pass
