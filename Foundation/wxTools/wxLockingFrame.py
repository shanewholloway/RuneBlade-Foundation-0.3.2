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

"""Frame locking (docking) code.

Frame locking (docking) is most useful when there are a LOT of windows about
and our human instincts plead for us to align them."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from wxWeakBind import wxBindCallable
from wxPython import wx
import weakref

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxLockSide:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _DeltaWing = 10
    _DeltaAttract = 10
    _DeltaResist = 10

    _LockingSides = [
        ({}, 2), # Left - outer
        ({}, 3), # Top - outer
        ({}, 0), # Right - outer
        ({}, 1), # Bottom - outer

        ({}, 0), # Left - inner
        ({}, 1), # Top - inner
        ({}, 2), # Right - inner
        ({}, 3), # Bottom - inner
        ]

    Left = 0
    Top = 1
    Right = 2
    Bottom = 3

    LeftInner = 4
    TopInner = 5
    RightInner = 6
    BottomInner = 7

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Class Methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetupScreenLockingSides(Class):
        l,t,w,h = wx.wxGetClientDisplayRect().asTuple()
        Class._LockingSides[Class.LeftInner][0][None] = [(l-Class._DeltaResist, t, l+Class._DeltaAttract, t+h, l)]
        Class._LockingSides[Class.RightInner][0][None] = [(l+w-Class._DeltaAttract, t, l+w+Class._DeltaResist, t+h, l+w)]
        Class._LockingSides[Class.BottomInner][0][None] = [(l, t+h-Class._DeltaAttract, l+w, t+h+Class._DeltaResist, t+h)]
        Class._LockingSides[Class.TopInner][0][None] = [(l, t-Class._DeltaResist, l+w, t+Class._DeltaAttract, t)]
    SetupScreenLockingSides = classmethod(SetupScreenLockingSides)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxLockingFrameBase(wx.wxFrame, wxLockSide):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _weakself = None
    __bLocking = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        wx.wxFrame.__init__(self, *args, **kw)

        wx.EVT_SIZE(self, wxBindCallable(self._OnSizeFrame))
        wx.EVT_MOVE(self, wxBindCallable(self._OnMoveFrame))
        self.PushEventHandler(wx.wxEvtHandler())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Show(self, bShow=1):
        result = wx.wxFrame.Show(self, bShow)
        self._SaveSidePositions()
        return result

    def Move(self, pos):
        self.__bLocking = 1
        if isinstance(pos, (tuple, list)): newpos = pos
        else: newpos = pos.x, pos.y

        newpos, newsize = self._OnLockingMove(newpos, self.GetSizeTuple()) or newpos
        result = wx.wxFrame.Move(self, newpos)

        self.__bLocking = 0
        return result

    def SetDimensions(self, x, y, w, h, *args, **kw):
        self.__bLocking= 1
        newpos, newsize = self._OnLockingMove((x,y), (w,h))
        newpos, newsize = self._OnLockingSize(newpos, newsize)
        result = self._DoSetDimensions(*(newpos + newsize + args), **kw)
        self.__bLocking= 0
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def LockFrameToSelf(self, frame, LockSideIndicies=(wxLockSide.Bottom,wxLockSide.LeftInner), LockSizeIndicies=tuple()):
        Positions = self._GetIntersectionPositions(*(self.GetRect().asTuple() + frame.GetSizeTuple()))
        return self._DoLockFrameToPositon(frame, Positions, LockSideIndicies, LockSizeIndicies)

    def LockToFrame(self, frame, LockSideIndicies=(wxLockSide.Bottom,wxLockSide.LeftInner), LockSizeIndicies=tuple()):
        Positions = self._GetIntersectionPositions(*(frame.GetRect().asTuple() + self.GetSizeTuple()))
        return self._DoLockFrameToPositon(self, Positions, LockSideIndicies, LockSizeIndicies)

    def LockToDesktop(self, LockSideIndicies=(wxLockSide.TopInner,wxLockSide.LeftInner), LockSizeIndicies=tuple()):
        Positions = self._GetIntersectionPositions(*(wx.wxGetClientDisplayRect().asTuple() + self.GetSizeTuple()))
        return self._DoLockFrameToPositon(self, Positions, LockSideIndicies, LockSizeIndicies)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Event Handlers
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _OnSizeFrame(self, evt):
        if not self.__bLocking:
            self.__bLocking = 1
            pos, size = self.GetPositionTuple(), self.GetSizeTuple()
            newpos, newsize = self._OnLockingSize(pos, size)
            self._DoSetDimensions(*(newpos + newsize))
            self.__bLocking = 0
        self._SaveSidePositions()
        evt.Skip()

    def _OnMoveFrame(self, evt):
        if not self.__bLocking:
            self.__bLocking= 1
            pos, size = self.GetPositionTuple(), self.GetSizeTuple()
            newpos, newsize = self._OnLockingMove(pos, size)
            self._DoSetDimensions(*(newpos + newsize))
            self.__bLocking= 0
        self._SaveSidePositions()
        evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _DoSetDimensions(self, *args, **kw):
        wx.wxFrame.SetDimensions(self, *args, **kw)

    def _RemoveSidePositions(self):
        if self._weakself:
            for each in self._LockingSides:
                del each[0][self._weakself]
            self._weakself = None

    def _SaveSidePositions(self):
        if not self.IsShown() or self.IsIconized():
            return self._RemoveSidePositions()
        self._weakself = weakref.ref(self)
        l,t,w,h = self.GetRect().asTuple()

        self._LockingSides[self.Left][0][self._weakself] = [(l-self._DeltaAttract, t, l+self._DeltaResist, t+h, l)]
        self._LockingSides[self.Right][0][self._weakself] = [(l+w-self._DeltaResist, t, l+w+self._DeltaAttract, t+h, l+w)]
        self._LockingSides[self.Bottom][0][self._weakself] = [(l, t+h-self._DeltaResist, l+w, t+h+self._DeltaAttract, t+h)]
        self._LockingSides[self.Top][0][self._weakself] = [(l, t-self._DeltaAttract, l+w, t+self._DeltaResist, t)]

        self._LockingSides[self.LeftInner][0][self._weakself] = [(l-self._DeltaResist, t-self._DeltaWing, l+self._DeltaAttract, t, l), (l-self._DeltaResist, t+h, l+self._DeltaAttract, t+h+self._DeltaWing, l)]
        self._LockingSides[self.RightInner][0][self._weakself] = [(l+w-self._DeltaAttract, t-self._DeltaWing, l+w+self._DeltaResist, t, l+w), (l+w-self._DeltaAttract, t+h, l+w+self._DeltaResist, t+h+self._DeltaWing, l+w)]
        self._LockingSides[self.BottomInner][0][self._weakself] = [(l-self._DeltaWing, t+h-self._DeltaAttract, l, t+h+self._DeltaResist, t+h), (l+w, t+h-self._DeltaAttract, l+w+self._DeltaWing, t+h+self._DeltaResist, t+h)]
        self._LockingSides[self.TopInner][0][self._weakself] = [(l-self._DeltaWing, t-self._DeltaResist, l, t+self._DeltaAttract, t), (l+w, t-self._DeltaResist, l+w+self._DeltaWing, t+self._DeltaAttract, t)]

    def _DoLockFrameToPositon(self, frame, Positions, LockSideIndicies, LockSizeIndicies):
        pos, size = frame.GetPositionTuple(), frame.GetSizeTuple()
        for LockIndex in LockSideIndicies:
            if LockIndex & 1: pos = pos[0], Positions[LockIndex] 
            else: pos = Positions[LockIndex], pos[1]

        newpos, pos = pos, (pos[0] + size[0], pos[1] + size[1])
        for LockIndex in LockSizeIndicies:
            if LockIndex & 1: pos = pos[0], Positions[LockIndex] 
            else: pos = Positions[LockIndex], pos[1]

        newsize = abs(pos[0] - newpos[0]), abs(pos[1] - newpos[1])
        newpos = tuple(map(min, zip(pos, newpos)))

        return frame.SetDimensions(*(newpos + newsize))

    def _OnLockingMove(self, pos, size):
        (l,t),(w,h) = pos, size
        IntersectionSides = self._GetIntersectionSides(l,t,w,h)
        for (LockingSides, WidthIdx), FrameSide in zip(self._LockingSides, IntersectionSides):
            for weakframe, SideList in LockingSides.iteritems():
                if weakframe is self._weakself: continue
                for Side in SideList:
                    if self._Intersects(FrameSide, Side):
                        if WidthIdx == 0: pos = Side[-1], pos[1], 
                        elif WidthIdx == 1: pos = pos[0], Side[-1], 
                        elif WidthIdx == 2: pos = Side[-1]-w, pos[1], 
                        elif WidthIdx == 3: pos = pos[0], Side[-1]-h, 
                        break
        return pos, size

    def _OnLockingSize(self, pos, size):
        (l,t),(w,h) = pos, size
        IntersectionSides = self._GetIntersectionSides(l,t,w,h)
        for (LockingSides, WidthIdx), FrameSide in zip(self._LockingSides, IntersectionSides):
            for weakframe, SideList in LockingSides.iteritems():
                if weakframe is self._weakself: continue
                for Side in SideList:
                    if self._Intersects(FrameSide, Side):
                        if WidthIdx == 0: pos = Side[-1], pos[1], 
                        elif WidthIdx == 1: pos = pos[0], Side[-1], 
                        elif WidthIdx == 2: size = Side[-1]-pos[0], size[1], 
                        elif WidthIdx == 3: size = size[0], Side[-1]-pos[1], 
                        break
        return pos, size

    #~ Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetIntersectionPositions(self, l, t, w, h, wP=0, hP=0):
        return [
            l-wP, #LeftSide
            t-hP, #TopSide
            l+w, #RightSide
            t+h, #BottomSide

            l, #LeftInnerSide
            t, #TopInnerSide
            l+w-wP, #RightInnerSide
            t+h-hP, #BottomInnerSide
            ]

    def _GetIntersectionSides(self, l, t, w, h):
        return [
            (l+w, t, l+w, t+h), # Right - Outter
            (l, t+h, l+w, t+h), # Bottom - Outter
            (l, t, l, t+h), # Left - Outter
            (l, t, l+w, t), # Top - Outter

            (l, t, l, t+h), # Left - Inner
            (l, t, l+w, t), # Top - Inner
            (l+w, t, l+w, t+h), # Right - Inner
            (l, t+h, l+w, t+h), # Bottom - Inner
            ]

    def _Intersects(self, A, B):
        if A[0] > B[2]: return 0
        if B[0] > A[2]: return 0
        if A[1] > B[3]: return 0
        if B[1] > A[3]: return 0
        return 1


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wxLockingFrameBase.SetupScreenLockingSides()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxAttractiveLockingFrame(wxLockingFrameBase):
    _DeltaAttract = 20
    _DeltaResist = 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxResistiveLockingFrame(wxLockingFrameBase):
    _DeltaAttract = 0
    _DeltaResist = 20

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxLockingFrame(wxLockingFrameBase):
    _DeltaAttract = 10
    _DeltaResist = 10

