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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
from xml.sax.saxutils import escape, quoteattr
from Foundation.WeakBind import BindCallable
from Foundation.SubjectObserver.CategorySubject import CategorySubject
from iqQuery import iqQueryBase
import JID 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqRosterQuery(iqQueryBase, CategorySubject):
    def __init__(self, JC, callback=None, BidValue=1):
        self.OnRosterCallback = BindCallable(callback)
        iqQueryBase.__init__(self, JC, self.OnRosterInfo, BidValue)
        CategorySubject.__init__(self)
        self.SendQuery('jabber:iq:roster')
        self.ByJID = {}

    def OnRosterInfo(self, stream, iq):
        RosterItems = getattr(iq.query[0], 'item', [])
        for each in RosterItems:
            self.ByJID[each.jid] = each
            self.UpdateObserversEx({('rosteritem', each.jid):each})
        if RosterItems:
            self.UpdateObservers(roster=self.ByJID)
        if self.OnRosterCallback:
            self.OnRosterCallback(stream, iq)

    def Get(self, jid, default=None):
        return self.ByJID.get(JID.JID(jid), default)

