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

class wxStaticBitmapWithRollover(wx.wxStaticBitmap):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _rollover_events = None
    _rollover_bitmap = None
    _nonrollover_bitmap = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetBitmapRollover(self, rollover):
        if not self._rollover_events:
            from Foundation.wxTools.wxWeakBind import wxBindCallable
            from Foundation.wxTools.wxRolloverEvents import wxRolloverEvents
            self._rollover_events = wxRolloverEvents()
            self._rollover_events.OnMouseEnter = wxBindCallable(self._SetRolloverBitmap)
            self._rollover_events.OnMouseLeave = wxBindCallable(self._SetNonRolloverBitmap)
            self.PushEventHandler(self._rollover_events)
        self._rollover_bitmap = rollover

    def GetBitmapRollover(self):
        return self._rollover_bitmap 

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _SetRolloverBitmap(self, evt):
        self._nonrollover_bitmap = self.GetBitmap()
        self.SetBitmap(self._rollover_bitmap)
        #self.Refresh()
        evt.Skip()

    def _SetNonRolloverBitmap(self, evt):
        if self._nonrollover_bitmap:
            self.SetBitmap(self._nonrollover_bitmap)
            self._nonrollover_bitmap = None
            #self.Refresh()
        evt.Skip()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class bitmap(wxSkinLayoutObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinLayoutObject.default_settings.copy()
    default_settings.update({
        'name':     __name__,
        'wxid':       'wx.wxNewId()',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        winParent = self.wxGetParentObject(wx.wxWindowPtr)
        kwSettings = self.wxSettingDict(['wxid', 'style', 'pos', 'size'], ['name'])
        kwSettings['bitmap'] = wx.wxEmptyBitmap(*kwSettings['size'])
        #self.object = wx.wxStaticBitmap(winParent, **kwSettings)
        self.object = wxStaticBitmapWithRollover(winParent, **kwSettings)
        self.wxInitialStandardOptions()

    def SkinFinalize(self):
        self.AddToLayout()
        self.wxFinalStandardOptions()

