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

from Foundation.SubjectObserver.Subject import Subject
from Foundation.SubjectObserver.Observer import Observer
from Foundation.SubjectObserver.BidableSubject import BidableSubject
from JabberSubject import FromJIDSubject
import JID

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Classes 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PresenceMapMixin(object):
    def __init__(self, JC):
        JC.stream.AddObserver('presence', self.OnPresence)
        self.ByJID = {}
        self.ByResource = {}

    def OnPresence(self, subject, presence):
        self.ByJID[presence.from_] = presence
        self.ByResource.setdefault(presence.from_.nominal(), {})[presence.from_.resource()] = presence

    def __getitem__(self, name): 
        return self.ByJID.get(JID.JID(name))
    def __setitem__(self, name, value): 
        self.ByJID[JID.JID(name)] = value
    def __delitem__(self, name): 
        del self.ByJID[JID.JID(name)]
    def __contains__(self, name): 
        return JID.JID(name) in self.ByJID

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PresenceMap(PresenceMapMixin, BidableSubject):
    def __init__(self, JC):
        PresenceMapMixin.__init__(self, JC)
        BidableSubject.__init__(self)

    def OnPresence(self, subject, presence):
        self.__super.OnPresence(subject, presence)
        self.UpdateObservers(PresenceFrom=presence.from_)

PresenceMap._PresenceMap__super = super(PresenceMap)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PresenceUpdate(FromJIDSubject):
    def __init__(self, JC):
        FromJIDSubject.__init__(self)
        JC.stream.AddObserver('presence', self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PresenceUpdateMap(PresenceUpdate, PresenceMapMixin):
    def __init__(self, JC):
        PresenceUpdate.__init__(self, JC)
        PresenceMapMixin.__init__(self, JC)

