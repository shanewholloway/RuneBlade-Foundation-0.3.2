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
from Foundation.wxTools.wxFrameMover import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class frame_mover(wxSkinObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinObject.default_settings.copy()
    default_settings.update({
        'dragbutton':'left',
        'sizeframe':'0,0',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        sizeframe = self.wxEval('sizeframe')
        if self.settings['dragbutton'] == 'left':
            self.object = wxFrameMoverLeftButton(self.context.frame, sizeframe)
        elif self.settings['dragbutton'] == 'right':
            self.object = wxFrameMoverRightButton(self.context.frame, sizeframe)
        elif self.settings['dragbutton'] == 'middle':
            self.object = wxFrameMoverMiddleButton(self.context.frame, sizeframe)
        else:
            self.object = wxFrameMoverLeftButton(self.context.frame, sizeframe)
 
    def SkinFinalize(self):
        parentobject = self.wxGetParentObject(wx.wxWindowPtr)
        parentobject.SetNextHandler(self.object)
        self.object.SetPreviousHandler(parentobject)
