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

import weakref
from types import ModuleType
from Foundation.Skinning.SkinObject import SkinObject 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PySkinObject(SkinObject):
    default_settings = SkinObject.default_settings.copy()
    default_settings['phase'] = 'initialize'
    
    def SkinInitialize(self):
        if self.settings['phase'] == 'initialize':
            self.object = self.ExecuteXML()

    def SkinFinalize(self):
        if self.settings['phase'] == 'finalize':
            self.object = self.ExecuteXML()

    def ExecuteXML(self, **Variables):
        return None

    def AddNamespace(self, namespace):
        if isinstance(namespace, ModuleType):
            self.globalnamespace.update(vars(namespace))
        else:
            self.globalnamespace.update(namespace)
