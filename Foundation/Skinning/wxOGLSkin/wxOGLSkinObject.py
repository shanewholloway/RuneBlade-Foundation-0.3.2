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

from Foundation.Skinning.wxPythonSkin.wxSkinObject import wxSkinObject, wx
from wxPython import ogl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

_ctxGlobals = {}
_ctxGlobals.update(vars(ogl))
_ctxGlobals.update(vars(wx))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Initialization 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
class wxOGLSkinObject(wxSkinObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def oglEvalDefault(self, Setting, Default, ctxLocals=None, ctxGlobals=_ctxGlobals):
        if ctxLocals is None: ctxLocals = {'self':self}
        return eval(self.settings.get(Setting, Default), ctxLocals, ctxGlobals)

    def oglEval(self, Setting, ctxLocals=None, ctxGlobals=_ctxGlobals):
        if ctxLocals is None: ctxLocals = {'self':self}
        return eval(self.settings.get(Setting), ctxLocals, ctxGlobals)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def oglSettingDict(self, Eval=[], NonEval=[], kwStart=None):
        result = kwStart or {}
        for each in Eval: result[each] = self.oglEval(each)
        for each in NonEval: result[each] = self.settings[each]
        return result

