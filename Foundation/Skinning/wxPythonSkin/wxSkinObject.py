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

from Foundation.Skinning.SkinObject import SkinObject
from wxPython import wx
import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

reColorHex = re.compile('(?:0x|#)([0-9a-fA-F]{6})')

# vv NOTE: DEBUG vvvvvvvvvvvvv

__debug_window_counts__ = 0
if __debug_window_counts__:
    _WindowCount = 0
    def _DEBUG_OnCreate(evt):
        global _WindowCount 
        _WindowCount += 1

    def _DEBUG_OnDestroy(evt):
        global _WindowCount 
        _WindowCount -= 1
        print '~~ -', _WindowCount 

# ^^ NOTE: DEBUG ^^^^^^^^^^^^^

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSkinObject(SkinObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = SkinObject.default_settings.copy()
    default_settings.update({ 
        'wxid':         '-1',
        'style':        '0',
        'size':         'wxDefaultSize',
        'pos':          'wxDefaultPosition',
        'name':         'wxSkinObject',

        ## Standard wx Options
        'enable':       '1',
        'tooltip':      '',
        'fgcolor':      None,
        'bgcolor':      None,
        'sizehints':    '-1,-1,-1,-1,-1,-1',

        })
    default_settings[SkinObject.BaseSettingsInherit] += 'wxDef,'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def wxGetWindowCollectorParent(self, CollectorTypes=None):
        if not CollectorTypes:
            return self.FindParent(wxSkinWindowCollectorObject)
        elif isinstance(CollectorTypes, (tuple, list)):
            return self.FindParent(*CollectorTypes)
        else: return self.FindParent(CollectorTypes)

    def wxGetParentObject(self, types):
        if isinstance(types, (tuple, list)):
            return self.FindParentOrObject(*types)
        else: return self.FindParentOrObject(types)

    def wxInitialStandardOptions(self):
        if isinstance(self.object, wx.wxWindowPtr):
            #assert isinstance(self, wxSkinWindowObject), "%r is not derived from wxSkinWindowObject" % self.__class__.__name__
            Parent = self.wxGetWindowCollectorParent()
            if Parent: Parent.AddWindowChild(self)

        # vv NOTE: DEBUG vvvvvvvvvvvvv
        
        if __debug_window_counts__ and hasattr(self.object, 'PushEventHandler'):
            eh = wx.wxEvtHandler()
            self.object.PushEventHandler(eh)
            _DEBUG_OnCreate(None)
            eh.Connect(-1, -1, wx.wxEVT_DESTROY, _DEBUG_OnDestroy)
        
        # ^^ NOTE: DEBUG ^^^^^^^^^^^^^

    def wxFinalStandardOptions(self):
        if 'fgcolor' in self.source_settings:
            self.object.SetForegroundColour(wxColorEval(self.settings['fgcolor']))
        if 'bgcolor' in self.source_settings:
            self.object.SetBackgroundColour(wxColorEval(self.settings['bgcolor']))
        if 'enable' in self.source_settings:
            self.object.Enable(self.wxEval('enable'))
        if 'tooltip' in self.source_settings:
            self.object.SetToolTipString(self.settings['tooltip'])
        if 'sizehints' in self.source_settings:
            self.object.SetSizeHints(*self.wxEval('sizehints'))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def wxEvalDefault(self, Setting, Default, ctxLocals=None, ctxGlobals=wx.__dict__):
        assert ctxLocals is None # I don't think that ctxLocals was ever used...
        assert ctxGlobals is wx.__dict__
        return self.EvalLocalEx(self.settings.get(Setting, Default), ctxGlobals)

    def wxEval(self, Setting, ctxLocals=None, ctxGlobals=wx.__dict__):
        assert ctxLocals is None # I don't think that ctxLocals was ever used...
        assert ctxGlobals is wx.__dict__
        return self.EvalLocalEx(self.settings.get(Setting), ctxGlobals)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def wxSettingDict(self, Eval=[], NonEval=[], kwStart=None):
        result = kwStart or {}
        for each in Eval: result[each] = self.wxEval(each)
        for each in NonEval: result[each] = self.settings[each]
        if 'wxid' in result:
            result['id'] = result['wxid']
            del result['wxid']
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSkinWindowCollectorObject(object):
    def AddWindowChild(self, ChildNode):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSkinWindowObject(wxSkinObject, wxSkinWindowCollectorObject):
    pass
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSkinObjectNoData(object):
    def Content(self):
        return ''

    def _addData(self, data):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Helper Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from wxPython.lib import colourdb as _colourdb
_NamedColours = {}
for each in _colourdb.getColourList(): _NamedColours[each] = 1

def wxColorEval(strColor):
    lst = reColorHex.split(strColor)[1:-1]
    if lst:
        color = int(lst[0], 16)
        return wx.wxColor( (color >> 16) & 0xff, (color >> 8) & 0xff, (color) & 0xff)
    elif strColor in _NamedColours:
        return wx.wxNamedColor(strColor)
    else: 
        return wx.wxColor(*eval(strColor, {}, {}))
