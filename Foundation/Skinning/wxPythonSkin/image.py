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

class image(wxSkinObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinObject.default_settings.copy()
    default_settings.update({
        'type':         'wxBITMAP_TYPE_ANY',
        'call':         None,
        'autosize':     '1',
        'rescale':      'None'
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        if self.settings['call'] is None:
            parentobject = self.wxGetParentObject(wx.wxWindowPtr)
            if hasattr(parentobject, 'SetBitmap'):
                self.settings['call'] = 'SetBitmap'
            elif hasattr(parentobject, 'SetBitmapLabel'):
                self.settings['call'] = 'SetBitmapLabel'
            elif isinstance(parentobject, wx.wxImageListPtr):
                self.settings['call'] = 'Add'
            else: self.settings['call'] = ''

        kwSettings = self.wxSettingDict(['type'], ['name'])
        kwSettings['name'] = os.path.join(self.context.__root__, kwSettings['name'])
        self.object = wx.wxImage(**kwSettings)
        rescale = self.wxEval('rescale')
        if rescale:
            if rescale[0] < 0:
                rescale = self.object.GetWidth(), rescale[1]
            if rescale[1] < 0:
                rescale = rescale[0], self.object.GetHeight()
            self.object.Rescale(*rescale)
 
    def SkinFinalize(self):
        if self.settings['call']:
            parentobject = self.wxGetParentObject(wx.wxWindowPtr)
            if self.wxEval('autosize'):
                newsize = (self.object.GetWidth(), self.object.GetHeight())
            elif hasattr(parentobject, 'GetSize'):
                newsize = parentobject.GetSize()
                
            method = getattr(parentobject, 'SetBitmap' + self.settings['call'], None)
            if not method: method = getattr(parentobject, self.settings['call'])
            method(self.object.ConvertToBitmap())

            if hasattr(parentobject, 'SetSize'):
                parentobject.SetSize(newsize)

wx.wxInitAllImageHandlers()
