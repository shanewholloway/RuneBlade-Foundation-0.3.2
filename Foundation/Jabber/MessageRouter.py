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

from JabberSubject import FromJIDSubjectMixin, JabberSubjectBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MessageRouterByFrom(FromJIDSubjectMixin):
    def __init__(self, JC):
        JC.stream.AddObserver('message', self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MessageRouterByType(JabberSubjectBase):
    def __init__(self, JC):
        JC.stream.AddObserver('message', self)

    def _ProxyObserverList(self, category):
        result = []
        result.extend(self._ObserverList(category[1].type))
        result.extend(super(MessageRouterByType, self)._ProxyObserverList(category))
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MessageRouterByID(JabberSubjectBase):
    def __init__(self, JC):
        JC.stream.AddObserver('message', self)

    def _ProxyObserverList(self, category):
        result = []
        result.extend(self._ObserverList(category[1].id))
        result.extend(super(MessageRouterByType, self)._ProxyObserverList(category))
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MessageRouter(MessageRouterByFrom, MessageRouterByType, MessageRouterByID):
    pass
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MessageRouterByThread(JabberSubjectBase):
    def __init__(self, JC):
        JC.stream.AddObserver('message', self)

    def _ProxyObserverList(self, category):
        result = []
        thread = ':'.join(map(str, category[1].Elements(value='thread')))
        result.extend(self._ObserverList(thread))
        result.extend(super(MessageRouterByThread, self)._ProxyObserverList(category))
        return result

