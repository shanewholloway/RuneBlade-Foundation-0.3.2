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

from wxSkinObject import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSkinLayoutObject(wxSkinWindowObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinObject.default_settings.copy()
    default_settings.update({
        'sizerOption': '0',
        'sizerFlag': '0',
        'sizerBorder': '0',
        'minsize': '0',
        })
    default_settings[SkinObject.BaseSettingsInherit] += 'wxDefLayout,'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def AddToLayout(self, layoutOverride=None):
        layout = layoutOverride or self.wxGetParentObject((wx.wxSizerPtr, wx.wxWindowPtr))
        if isinstance(layout, wx.wxSizerPtr):
            sizerOption = self.wxEval('sizerOption')
            sizerFlag = self.wxEval('sizerFlag')
            sizerBorder = self.wxEval('sizerBorder')
            if isinstance(self.object, tuple):
                layout.Add(self.object[0], self.object[1], sizerOption, sizerFlag, sizerBorder)
            else:
                layout.Add(self.object, sizerOption, sizerFlag, sizerBorder)

        minsize = None
        if 'minsize' in self.source_settings: 
            minsize = self.wxEval('minsize')
        elif 'sizehints' in self.source_settings: 
            minsize = self.wxEval('sizehints')[:2]

        if minsize: 
            if isinstance(layout, wx.wxSizerPtr):
                layout.SetItemMinSize(self.object, *minsize)
            if isinstance(self.object, wx.wxSizerPtr):
                self.object.SetMinSize(minsize)

        return layout

