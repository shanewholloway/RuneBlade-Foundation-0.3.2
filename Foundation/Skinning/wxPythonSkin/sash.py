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

from wxSkinLayoutObject import wx, wxSkinLayoutObject, wxSkinObjectNoData

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class sash(wxSkinLayoutObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinLayoutObject.default_settings.copy()
    default_settings.update({
        'name':     __name__,
        'style':    'wxCLIP_CHILDREN | wxSW_3D',
        'xrange':   '0,-1',
        'yrange':   '0,-1',
        'edges':    '[]',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        winParent = self.wxGetParentObject(wx.wxWindowPtr)
        kwSettings = self.wxSettingDict(['wxid', 'style', 'pos', 'size'], ['name'])
        self.object = self.wxSashWindow(winParent, **kwSettings)
        self.AddToLayout()
        self.wxInitialStandardOptions()

    def SkinFinalize(self):
        self.SetSashSettings()
        self.wxFinalStandardOptions()

    def SetSashSettings(self):
        xrange = self.wxEval('xrange')
        if xrange[0] >= 0: self.object.SetMinimumSizeX(xrange[0])
        if xrange[1] >= 0: self.object.SetMaximumSizeX(xrange[1])

        yrange = self.wxEval('yrange')
        if yrange[0] >= 0: self.object.SetMinimumSizeY(xrange[0])
        if yrange[1] >= 0: self.object.SetMaximumSizeY(xrange[1])

        edges = self.wxEval('edges')
        for edge in edges:
            self.object.SetSashVisible(edge, 1)
