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

class splitter(wxSkinLayoutObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinLayoutObject.default_settings.copy()
    default_settings.update({
        'name':         __name__,
        'style':        'wxSP_3D | wxCLIP_CHILDREN',
        'orientation':  'vertical',
        'splitterPos':      '300',
        'splitterMinSize':  '50',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        winParent = self.wxGetParentObject(wx.wxWindowPtr)
        kwSettings = self.wxSettingDict(['wxid', 'style', 'pos', 'size'], ['name'])
        kwSettings['point'] = kwSettings['pos']
        del kwSettings['pos']
        self.object = wx.wxSplitterWindow(winParent, **kwSettings)
        self.SplitWindows = []
        self.AddToLayout()

    def AddWindowChild(self, ChildNode):
        if len(self.SplitWindows) > 2:
            self.SplitWindows[:] = self.SplitWindows[-1:]
        self.SplitWindows.append(ChildNode.object)
        if len(self.SplitWindows) >= 2:
            if self.settings['orientation'] == 'vertical':
                self.object.SplitVertically(self.SplitWindows[0], self.SplitWindows[1])
            elif self.settings['orientation'] == 'horizontal':
                self.object.SplitHorizontally(self.SplitWindows[0], self.SplitWindows[1])
        self.wxInitialStandardOptions()

    def SkinFinalize(self):
        self.wxFinalStandardOptions()
        self.object.SetSashPosition(self.wxEval('splitterPos'))
        self.object.SetMinimumPaneSize(self.wxEval('splitterMinSize'))
        
