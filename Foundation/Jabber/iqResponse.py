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

"""Basis for responding to jabber:iq:* queries"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
from xml.sax.saxutils import escape, quoteattr
from Foundation.WeakBind import BindCallable
import JabberObserver as JObs
import JID
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqResponseBase(JObs.JabberObserver):
    def __init__(self, JC, callback=None, BidValue=1):
        JObs.JabberObserver.__init__(self, callback, BidValue=BidValue)
        if isinstance(JC, weakref.ReferenceType):
            self.JC = JC
        else: self.JC = weakref.ref(JC)
        self.JC().stream.AddObserver('iq', self)

    def AnswerQuery(self, ns, type='get'):
        # Lets observer the jabber stream
        if ns not in self.JC().SupportedNS:
            self.JC().SupportedNS.append(ns)

        del self.Match[:]
        self.Match.append(JObs.MatchHasChildNamespace(ns))
        self.Match.append(JObs.MatchAttributes(type=type))

        # Setup our match attributes
        return self

