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

class layout(wxSkinLayoutObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinLayoutObject.default_settings.copy()
    default_settings.update({
        'orientation': 'opposite',
        'sizerAuto': '1',
        'sizerFit': '0',
        'args': 'tuple()',
        })

    orientation_map = {
        # Opposite is default vertical
        'opposite': (wx.wxBoxSizer, (wx.wxVERTICAL,)),
        'vertical': (wx.wxBoxSizer, (wx.wxVERTICAL,)),
        'vert': (wx.wxBoxSizer, (wx.wxVERTICAL,)),

        'horizontal': (wx.wxBoxSizer, (wx.wxHORIZONTAL,)),
        'horiz': (wx.wxBoxSizer, (wx.wxHORIZONTAL,)),

        'staticVert': (wx.wxStaticBoxSizer, (wx.wxVERTICAL,)),
        'staticVertical': (wx.wxStaticBoxSizer, (wx.wxVERTICAL,)),
        'staticHoriz': (wx.wxStaticBoxSizer, (wx.wxHORIZONTAL,)),
        'staticHorizontal': (wx.wxStaticBoxSizer, (wx.wxHORIZONTAL,)),

        'box': (wx.wxBoxSizer, tuple()),
        'staticBox': (wx.wxBoxSizer, tuple()),
        'grid': (wx.wxGridSizer, tuple()),
        'flexGrid': (wx.wxFlexGridSizer, tuple()),
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        self.PushContext()
        self.winParent = self.wxGetParentObject((wx.wxWindowPtr, layout))
        if not isinstance(self.winParent, wx.wxWindowPtr): self.winParent = None
        orientation = self.settings['orientation']
        if not self.winParent and orientation == 'opposite':
            orientation = 'vertical' # New Default
            # Calculate the "real" opposite
            parentLayout = getattr(self.context, 'layout', None)
            if parentLayout and isinstance(parentLayout, wx.wxBoxSizerPtr):
                if parentLayout.GetOrientation() == wx.wxVERTICAL:
                    orientation = 'horizontal' # We should toggle it here

        # Create the layout sizer
        sizerClass, preArgs = self.orientation_map[orientation]
        postArgs = self.wxEval('args')
        self.object = sizerClass(*(preArgs + postArgs))

        self.context.layout = self.object

    def SkinFinalize(self):
        parent = self.AddToLayout()
        if parent is self.winParent: 
            parentLayout = getattr(self.parent().context, 'layout', None)
            if parentLayout: 
                sizew, sizeh = self.object.GetMinSize().asTuple()
                parentLayout.SetItemMinSize(self.winParent, sizew, sizeh)

            self.winParent.SetSizer(self.object)
            self.object.SetSizeHints(self.winParent) # Be sure to set size hints after setting sizer!

            if self.wxEval('sizerAuto'): 
                self.winParent.SetAutoLayout(1)
            if self.wxEval('sizerFit'): 
                self.object.Fit(self.winParent)
        del self.winParent

