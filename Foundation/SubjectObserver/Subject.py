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

"""Maintains a list of montioring observers that get updated when 
UpdateObservers or UpdateObserversEx get called, unless the subject is Locked.
A lock can be obtained by calling Lock, and it maintained until the lock object 
no longer exisits or is explicitly released.

WeakBind module is used extensively to prevent reference chains keeping objects in
memory unnecessarily."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Foundation import WeakBind
import bisect

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Subject(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self._observers = []
        self._cachedUpdates = {}
        self._locked = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Management 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def AddObserver(self, observer, priority=0):
        """Adds observer to the internal collection monitoring this subject
        Observer is assumed to be a callable object."""
        result = WeakBind.BindCallable(observer)
        bisect.insort(self._observers, (-priority, result))
        return self

    def RemoveObserver(self, observer):
        """Removes observer from the internal collection monitoring this subject.  
        Observer should be the same object that was passed to AddObserver."""
        result = WeakBind.BindCallable(observer)
        self._observers[:] = [x for x in self._observers if x[-1] != result]
        return self

    def ClearObservers(self):
        """Removes all observers from the internal collection"""
        self._observers[:] = []
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Update Callbacks
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    def _ObserverList(self):
        """Returns the internal observer collection pruned of invalid weakref objects as a list"""
        self._observers[:] = [x for x in self._observers if x[-1]]
        return [x[-1] for x in self._observers]
    Observers = property(_ObserverList)

    def UpdateObservers(self, **kw):
        """Updates all observers of this subject with data in **kw.  See also UpdateObserversEx."""
        return self.UpdateObserversEx(kw)

    def UpdateObserversEx(self, kw):
        """Updates all observers of this subject with data in kw.  (kw is assumed to be a dictonary.)  See also UpdateObservers."""
        self._cachedUpdates.update(kw)
        if self._cachedUpdates and not self.Locked():
            _cachedUpdates, self._cachedUpdates = self._cachedUpdates, {}
            lock = self.Lock()
            for each in self.Observers:
                self.UpdateObserver(each, _cachedUpdates)
            lock.SetLock(None)
            return 1
        else: return 0

    def UpdateObserver(self, observer, UpdateDict):
        """Updates observer with UpdateDict.  (UpdateDict is assumed to be a dictonary.)"""
        if observer: observer(self, **UpdateDict)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Subject Locking
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class _SubjectLock:
        """Maintains a lock on subject while instance exists"""
        subject = None
        def __init__(self, lockedsubject):
            self.SetLock(lockedsubject)
        def __del__(self):
            try: 
                self.SetLock(None)
            except:
                # XXX: Is there a good way to pass the exception along, and not have it 
                # be absorbed by the python __del__ exception condition?
                import traceback
                traceback.print_exc()
        def SetLock(self, lockedsubject):
            """Obtains a  lock on lockedsubject.  If lockedsubject is different than the 
            current subject, then the current subject is unlocked as well."""
            if self.subject and id(self) in self.subject._locked:
                self.subject._locked.remove(id(self))
                if self.subject._cachedUpdates:
                    self.subject.UpdateObservers()
            self.subject = lockedsubject
            if self.subject:
                self.subject._locked.append(id(self))

    def Lock(self):
        """Prevents observers of subject from being updated while a lock is held on the subject."""
        return self._SubjectLock(self)

    def Locked(self):
        """Returns 1 if the subject is locked, and 0 otherwise"""
        return self._locked and 1 or 0
