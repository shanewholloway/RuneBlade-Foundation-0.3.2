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

from PySkinObject import PySkinObject
import sys
import weakref

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class script(PySkinObject):
    default_settings = PySkinObject.default_settings.copy()
    #default_settings['module'] = None
    default_settings['reload'] = '0'
    default_settings['args'] = '(self,)'
    default_settings['kw'] = '{}'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def ExecuteXML(self, **Variables):
        bAddToSysPath = self.context.__root__ not in sys.path
        if bAddToSysPath: sys.path.append(self.context.__root__)
        module = __import__(self.settings['module'], {}, {}, self.settings['call'])
        if int(self.settings['reload']):
            reload(module)
        call = getattr(module, self.settings['call'])
        args = self.EvalLocal(self.settings['args'])
        kw = self.EvalLocal(self.settings['kw'])
        if bAddToSysPath: sys.path.remove(self.context.__root__)
        return call(*args, **kw)

    def _addData(self, data):
        pass

