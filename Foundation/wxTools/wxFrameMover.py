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

"""EventHandlers that allow any window to act as a drag bar.

Primarily fills the need of having a "move handle" somewhere else than the
titlebar of the window."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
from wxPython import wx
from Foundation.wxTools.wxWeakBind import wxBindCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxFrameMoverLeftButton(wx.wxEvtHandler):
    def __init__(self, Frame, SizeFrame=(0,0)):
        wx.wxEvtHandler.__init__(self)
        if Frame: self.SetFrame(Frame)
        self._CaptrueEvents()
        self.SizeFrame = SizeFrame

    def _CaptrueEvents(self):
        wx.EVT_MOTION(self, wxBindCallable(self.OnMouseMotion))
        wx.EVT_LEFT_DOWN(self, wxBindCallable(self.OnMouseDown))
        wx.EVT_LEFT_UP(self, wxBindCallable(self.OnMouseUp))

    def SetFrame(self, Frame):
        self.Frame = weakref.proxy(Frame)

    def OnMouseDown(self, evt):
        EO = evt.GetEventObject()
        EO.CaptureMouse()
        self._DoSavePosition(evt, EO)

    def OnMouseUp(self, evt):
        evt.GetEventObject().ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self._DoMove(evt)

    def _DoSavePosition(self, evt, EO):
        self.OffsetPos = EO.ClientToScreen(evt.GetPosition())
        self.FrameRect = self.Frame.GetRect().asTuple()

    def _DoMove(self, evt):
        DeltaPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        DeltaRect = [0,0,0,0]
        for idx in xrange(2):
            alpha = self.SizeFrame[idx]
            if alpha < 0:
                DeltaRect[0 + idx] = alpha * (self.OffsetPos[idx] - DeltaPos[idx])
                DeltaRect[2 + idx] = alpha * (DeltaPos[idx] - self.OffsetPos[idx])
            elif alpha > 0:
                DeltaRect[0 + idx] = 0
                DeltaRect[2 + idx] = alpha * (DeltaPos[idx] - self.OffsetPos[idx])
            elif self.SizeFrame == (0,0):
                DeltaRect[2 + idx] = 0
                DeltaRect[0 + idx] = DeltaPos[idx] - self.OffsetPos[idx]

        newrect = [x+y for x,y in zip(self.FrameRect, DeltaRect)]
        self.Frame.SetDimensions(*newrect)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxFrameMoverRightButton(wxFrameMoverLeftButton):
    def _CaptrueEvents(self):
        wx.EVT_MOTION(self, wxBindCallable(self.OnMouseMotion))
        wx.EVT_RIGHT_DOWN(self, wxBindCallable(self.OnMouseDown))
        wx.EVT_RIGHT_UP(self, wxBindCallable(self.OnMouseUp))

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.RightIsDown():
            self._DoMove(evt)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxFrameMoverMiddleButton(wxFrameMoverLeftButton):
    def _CaptrueEvents(self):
        wx.EVT_MOTION(self, wxBindCallable(self.OnMouseMotion))
        wx.EVT_MIDDLE_DOWN(self, wxBindCallable(self.OnMouseDown))
        wx.EVT_MIDDLE_UP(self, wxBindCallable(self.OnMouseUp))

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():
            self._DoMove(evt)

