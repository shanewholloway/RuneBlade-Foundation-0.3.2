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

"""Simple select.select handle management.

A set of classes wrapping select.select, making the management of N handles as 
simple as managing a single handle.  In order to implement SmartSelect for your 
socket or other handle(s), simply derive from SmartSelectBase, and implement the 
abstract methods from ClientBase.

Well read pythoneers will note that is module is very similar to asyncore, and are
probably wondering why.  Well, my reason is interface.  Asyncore was great inspiration,
but I wanted to have less assumption that the objects were sockets; simply objects 
compatable with select.select.  Secondly, objects derived from SmartSelectBase should
be as easily run as if they were collected into a larger group.  Finally, I wanted the
collections to feel like just that: collections of selectable objects.  (dict, list, or single)
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import select
import socket

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClientBase(object):
    """An abstract base class for creating "Smart Sockets" or other select.select able objects"""
    #def fileno(self): return 0 ## override this, returning something that works with select.select, like socket.fileno
    def _NeedsRead(self): return 0
    #def _ProcessRead(self): pass  ## If there is no definition, then these will raise if not "overridden"
    def _NeedsWrite(self): return 0
    #def _ProcessWrite(self): pass  ## If there is no definition, then these will raise if not "overridden"
    def _NeedsError(self): return 0
    #def _ProcessError(self): pass  ## If there is no definition, then these will raise if not "overridden"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SmartSelectBase(object):
    """Base class for waiting upon a set of select.select able objects"""

    ProcessState = "Initial", None

    def Process(self, timeout=None):
        """Uses select.select to wait on several file (proxy) handles in an object-oriented way.  
        ProcessState contains the state and, if applicable, the handle being processed,
        allowing for interogation in the case of an exception."""
        if not self:
            self.ProcessState = "Idle", None
            return 0

        self.ProcessState = "Waiting", None
        ReadList, WriteList, ErrorList = self.ReadList, self.WriteList, self.ErrorList
        if ReadList or WriteList or ErrorList:
            lstSelected = select.select(ReadList, WriteList, ErrorList, timeout)

            for each in lstSelected[0]: 
                self.ProcessState = "Read", each
                each._ProcessRead()
            for each in lstSelected[1]: 
                self.ProcessState = "Write", each
                each._ProcessWrite()
            for each in lstSelected[2]: 
                self.ProcessState = "Error", each
                each._ProcessError()

            self.ProcessState = "Complete", None
            return (lstSelected[0] or lstSelected[1] or lstSelected[2]) and 1 or 0
        else:
            self.ProcessState = "Complete", None
            return 0

    def ProcessPending(self, timeout=0.0):
        """Calls Process until a timeout occurs."""
        while self.Process(timeout):
            pass
        return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SmartSelectClientBase(ClientBase, SmartSelectBase):
    """Allows base classes of a smart select to be able to run "by themselves" as if they were their own SmartSelectors"""
    def _getReadList(self): return self._NeedsRead() and [self] or []
    ReadList = property(_getReadList)

    def _getWriteList(self): return self._NeedsWrite() and [self] or []
    WriteList = property(_getWriteList)

    def _getErrorList(self): return self._NeedsError() and [self] or []
    ErrorList = property(_getErrorList)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SmartSelectList(SmartSelectBase, list):
    """A list collection of Smart Sockets to aid in pseudo "non-blocking" socket programming.  
    Note, this is very simalr to asyncore.dispatcher."""

    def __call__(self, *args, **kw):
        return self.Process(*args, **kw)
        
    def _getReadList(self): return [x for x in self if x._NeedsRead()]
    ReadList = property(_getReadList)

    def _getWriteList(self): return [x for x in self if x._NeedsWrite()]
    WriteList = property(_getWriteList)

    def _getErrorList(self): return [x for x in self if x._NeedsError()]
    ErrorList = property(_getErrorList)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SmartSelectDict(SmartSelectBase, dict):
    """A dictionary collection of Smart Sockets to aid in pseudo "non-blocking" socket programming.  
    Note, this is very simalr to asyncore.dispatcher."""

    def __call__(self, *args, **kw):
        return self.Process(*args, **kw)
        
    def _getReadList(self): return [x for x in self.itervalues() if x._NeedsRead()]
    ReadList = property(_getReadList)

    def _getWriteList(self): return [x for x in self.itervalues() if x._NeedsWrite()]
    WriteList = property(_getWriteList)

    def _getErrorList(self): return [x for x in self.itervalues() if x._NeedsError()]
    ErrorList = property(_getErrorList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SmartSelectDictList(SmartSelectBase, dict):
    """A dictionary collection of lists of Smart Sockets to aid in pseudo "non-blocking" socket programming.  
    Note, this is very simalr to asyncore.dispatcher."""

    def __call__(self, *args, **kw):
        return self.Process(*args, **kw)
        
    def _getReadList(self): return [x for y in self.itervalues() for x in y if x._NeedsRead()]
    ReadList = property(_getReadList)

    def _getWriteList(self): return [x for y in self.itervalues() for x in y if x._NeedsWrite()]
    WriteList = property(_getWriteList)

    def _getErrorList(self): return [x for y in self.itervalues() for x in y if x._NeedsError()]
    ErrorList = property(_getErrorList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SmartSelect = SmartSelectList
