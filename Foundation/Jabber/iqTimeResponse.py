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

"""Responds to jabber:iq:time queries"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from iqResponse import iqResponseBase
import time
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqTimeResponse(iqResponseBase):
    def __init__(self, JC, BidValue=1):
        iqResponseBase.__init__(self, JC, self.OnIQTimeRequest, BidValue)
        self.AnswerQuery("jabber:iq:time")

    def OnIQTimeRequest(self, subject, iq):
        iq.to = iq.from_
        del iq.from_
        iq.type = 'result'
        
        strResult = ''.join(iq._toXML(bHeaderOnly=1))
        strResult += '''<query xmlns='jabber:iq:time' >'''
        strResult += '''<utc>%04d%02d%02dT%02d:%02d:%02d</utc>''' % time.gmtime()[:6]
        strResult += '''<display>%s</display>''' % time.asctime()
        strResult += '''<tz>%s</tz>''' % time.tzname[-1]
        strResult += '''</query></iq>'''

        iq._client.SendXML(strResult)

