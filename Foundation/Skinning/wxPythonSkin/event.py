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

from wxSkinObject import wx, wxSkinObject, wxSkinObjectNoData

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class event(wxSkinObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinObject.default_settings.copy()
    #default_settings['type'] = ''
    #default_settings['call'] = ''
    default_settings['wxid'] = '-1'
    default_settings['towxid'] = '-1'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        eventtypes = self.wxEval('type')
        startid, endid = self.wxEval('wxid'), self.wxEval('towxid')
        call = self.wxEval('call')
        if not isinstance(eventtypes, (tuple, list)):
            eventtypes = (eventtypes,)

        self.object = []
        for eventtype in eventtypes:
            self.object.append((startid, endid, eventtype, call))
 
    def SkinFinalize(self):
        parentobject = self.wxGetParentObject(wx.wxEvtHandlerPtr)
        for ConnectParams in self.object:
            parentobject.Connect(*ConnectParams)
