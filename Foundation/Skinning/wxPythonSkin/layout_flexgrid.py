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

from layout import wx, layout

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layout_flexgrid(layout):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = layout.default_settings.copy()
    default_settings.update({
        'orientation': 'opposite',
        'sizerAuto': '1',
        'sizerFit': '0',
        'rows': '0',
        'cols': '2',
        'vgap': '0',
        'hgap': '0',
        'expandrows': '[]',
        'expandcols': '[-1]',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        self.PushContext()
        self.winParent = self.wxGetParentObject((wx.wxWindowPtr, layout))
        if not isinstance(self.winParent, wx.wxWindowPtr): self.winParent = None

        # Create the layout sizer
        kwSettings = self.wxSettingDict(['rows', 'cols', 'vgap', 'hgap'], [])
        self.object = wx.wxFlexGridSizer(**kwSettings)

        for row in self.wxEval('expandrows'):
            if row < 0: row = kwSettings['rows'] + row
            self.object.AddGrowableRow(row)

        for col in self.wxEval('expandcols'):
            if col < 0: col = kwSettings['cols'] + col
            self.object.AddGrowableCol(col)

        self.context.layout = self.object

