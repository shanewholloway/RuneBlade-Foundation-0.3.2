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

"""Subject/Observer wrapping of wxEvents, allowing 0 to n recipients for any given event. 

Avoids having to deal with evt.Skip, or PushEventHandler for every needed layer by building
upon Bidable and Category subjects from Foundation.SubjectObserver.

To use:
    EvtSubject = wxEvtSubject()
    EvtSubject.PushEventHandler(window_or_evthandler)
    EvtSubject.AddObserver(wxEVT_SIZE, callback_one)
    EvtSubject.AddObserver(wxEVT_SIZE, callback_n)
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from wxPython import wx
from Foundation.SubjectObserver import BidableCategorySubject
from Foundation.WeakBind import BindCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxEvtHandlerBidableCategorySubject(BidableCategorySubject):
    EventCallbackName = 'event'

    def __init__(self, EventHandler=None):
        self.EvtHandler = wx.wxEvtHandler()
        BidableCategorySubject.__init__(self)
        if EventHandler: self.PushEventHandler(EventHandler)

    def _OnEvent(self, evt):
        if not self.UpdateObserversEx({(self.EventCallbackName, evt.GetEventType()):evt}):
            evt.Skip()
    
    def PushEventHandler(self, EventHandler):
        self.EvtHandler.SetNextHandler(EventHandler)
        EventHandler.SetPreviousHandler(self.EvtHandler)

    def AddObserver(self, category, *args, **kw):
        self.EvtHandler.Connect(-1, -1, category, BindCallable(self._OnEvent))
        BidableCategorySubject.AddObserver(self, (self.EventCallbackName, category), *args, **kw)

wxEvtSubject = wxEvtHandlerBidableCategorySubject
