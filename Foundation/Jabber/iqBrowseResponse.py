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

"""Responds to jabber:iq:browse queries"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from iqResponse import iqResponseBase
from xml.sax.saxutils import escape, quoteattr
import sys
import os
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqBrowseResponse(iqResponseBase):
    def __init__(self, JC, BidValue=1):
        iqResponseBase.__init__(self, JC, self.OnIQBrowseRequest, BidValue=BidValue)
        self.AnswerQuery("jabber:iq:browse")

    def OnIQBrowseRequest(self, subject, iq):
        iq.to = iq.from_
        del iq.from_
        iq.type = 'result'
        
        strResult = ''.join(iq._toXML(bHeaderOnly=1))
        strResult += '''<user xmlns='jabber:iq:browse' jid=%s name=%s >''' % (quoteattr(self.JC().information.jid), quoteattr(self.JC().information.username))
        strResult += ''.join(['<ns>%s</ns>' % escape(ns) for ns in self.JC().SupportedNS])
        strResult += '''</user></iq>'''

        iq._client.SendXML(strResult)
