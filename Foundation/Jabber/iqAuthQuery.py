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

import weakref, sha
from xml.sax.saxutils import escape, quoteattr
from Foundation.WeakBind import BindCallable
from iqQuery import iqQueryBase
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqAuthQuery(iqQueryBase):
    def __init__(self, JC, username, password, resource, callback=None, BidValue=1):
        self._AuthInProgress = 1
        iqQueryBase.__init__(self, JC, callback, BidValue)

        self.JC().information.authorized = 0
        self.JC().information.jid = self.JC().BuildJID(username, None, resource)
        
        while not self.JC()._elements:
            self.JC().Process()

        digest = sha.new(self.JC()._elements[0].id + password).hexdigest()
        xmlAuthInfo = '<username>%s</username><digest>%s</digest><resource>%s</resource>' % (username, digest, resource)

        self.SendQuery('jabber:iq:auth', type='set', xml=xmlAuthInfo)
        # The last match assertion says that there is a child 
        # in the jabber:iq:auth namespace, which there won't be.  
        # So remove that match criteria.
        self.Match.pop()

    def __nonzero__(self):
        if self._AuthInProgress:
            return 1
        else: return super(iqAuthQuery, self).__nonzero__()
       
    def __call__(self, stream, iq):
        if iq.type == 'result':
            self.JC().information.authorized = 1
        self._AuthInProgress = 0
        if self:
            return super(iqAuthQuery, self).__call__(stream, iq)
