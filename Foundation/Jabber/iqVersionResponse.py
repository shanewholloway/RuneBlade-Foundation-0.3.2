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

"""Responds to jabber:iq:version queries"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from iqResponse import iqResponseBase
import sys
import os
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqVersionResponse(iqResponseBase):
    def __init__(self, JC, Name, Version, BidValue=1):
        iqResponseBase.__init__(self, JC, self.OnIQVersionRequest, BidValue)
        self.AnswerQuery("jabber:iq:version")
        self.Name = Name
        self.Version = Version

    def OnIQVersionRequest(self, subject, iq):
        iq.to = iq.from_
        del iq.from_
        iq.type = 'result'
        
        strResult = ''.join(iq._toXML(bHeaderOnly=1))
        strResult += '''<query xmlns='jabber:iq:version' >'''
        strOS = '%s (%s) running Python %s' % (os.name, sys.platform, sys.version)
        strResult += '''<name>%s</name><version>%s</version><os>%s</os>''' % (self.Name, self.Version, strOS)
        strResult += '''</query></iq>'''

        iq._client.SendXML(strResult)
