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

"""Create wxWindow's derived controls to support an ActiveX controls.

This code is heavily borrowed from Robin Dunn's wxPython.lib.activexwrapper,
but reorganized in order to:
    - Support imported objects without a default_source (Adobe.SVGCtl.3)
    - Use the pythonic mixin idiom to simplify and clarify what is happening
    - Move to python2.2's types.ClassType(...) factory method instead of the new module
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import win32ui
import pywin.mfc.activex
import win32con
from wxPython import wx
import types

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxActiveXMixins(wx.wxWindow, pywin.mfc.activex.Control):
    """pyWin and wxPython mixin to supply the envrionment for ActiveX controls"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        # init base classes
        pywin.mfc.activex.Control.__init__(self)
        wx.wxWindow.__init__(self, *args, **kw)

        win32ui.EnableControlContainer()
        self._eventObj = self._eventObj  # move from class to instance

        # create a pythonwin wrapper around this wx.wxWindow
        handle = self.GetHandle()
        self._wnd = win32ui.CreateWindowFromHandle(handle)

        # create the control
        sz = self.GetSize()
        self.CreateControl(self.__class__.__name__, win32con.WS_TABSTOP | win32con.WS_VISIBLE, 
            (0, 0, sz.width, sz.height), self._wnd, self.GetId())

        # init the ax events part of the object
        self._eventBase.__init__(self, self._dispobj_)

        # hook some wx events
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

    def __getattr__(self, attr):
        try:
            return pywin.mfc.activex.Control.__getattr__(self, attr)
        except AttributeError:
            if self._eventObj:
                return getattr(self._eventObj, attr)
            else: raise

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Cleanup(self):
        del self._wnd
        self.close()

    def OnSize(self, evt):
        # get wx.wxWindow size
        sz = self.GetClientSize()
        # move the AXControl
        self.MoveWindow((0, 0, sz.width, sz.height), 1)

    def OnEraseBackground(self, evt):
        pass
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _EmptyEvents:
    """Mixin for CoClasses that do not have a "default_source" attributes, such as Adobe.SVGCtl.3"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _public_methods_ = []
    _dispid_to_func_ = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw): 
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Function Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def wxActiveXControlFactory(CoClass, eventClasses=tuple(), eventObj=None):
    """Creates a wxWindow's derived control to support an ActiveX control given the control's CoClass.
    
    Parameters:
        - CoClases: COM CoClass from win32com.client gencache or makepy or similar

        - eventClasses: a tuple of classes that the component should also derive from,
            specifically to support event overrides

        - eventObj: an instance to be searched for event callbacks (and other things...).
            Think acquisition.  ;)  

    See also -- wxPython.lib.activexwrapper.MakeActiveXClass
    """
    # This would be better with Python2.2's Metaclasses... but wxPython 
    # derives from classic classes which are not quite as nice; but workable ;)
    AXEventClass = getattr(CoClass, 'default_source', _EmptyEvents)
    if not isinstance(eventClasses, (tuple, list)): eventClasses = (eventClasses,)
    name = 'AXControl_' + CoClass.__name__
    bases = (wxActiveXMixins, CoClass, AXEventClass) + filter(None, eventClasses)
    data = {'_eventObj':eventObj, '_eventBase': AXEventClass, 'default_source': AXEventClass}
    return types.ClassType(name, bases, data)

