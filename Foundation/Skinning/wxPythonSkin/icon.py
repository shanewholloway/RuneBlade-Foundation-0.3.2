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
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class icon(wxSkinObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinObject.default_settings.copy()
    default_settings.update({
        'type':         'wxBITMAP_TYPE_ICO',
        'call':         None,
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        if self.settings['call'] is None:
            parentobject = self.wxGetParentObject(wx.wxWindowPtr)
            if hasattr(parentobject, 'SetIcon'):
                self.settings['call'] = 'SetIcon'
            else: self.settings['call'] = ''

        kwSettings = self.wxSettingDict(['type'], ['name'])
        kwSettings['name'] = os.path.join(self.context.__root__, kwSettings['name'])
        self.object = wx.wxIcon(kwSettings['name'], kwSettings['type'])

    def SkinFinalize(self):
        if self.settings['call']:
            parentobject = self.wxGetParentObject(wx.wxWindowPtr)
            method = getattr(parentobject, self.settings['call'])
            method(self.object)

