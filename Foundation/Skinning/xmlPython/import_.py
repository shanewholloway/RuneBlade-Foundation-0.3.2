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
import inline

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class import_(inline.inline):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = inline.inline.default_settings.copy()
    default_settings['module'] = None
    default_settings['from'] = None
    default_settings['attr'] = None
    default_settings['reload'] = '0'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def ExecuteXML(self, **Variables):
        SysPathIdx = len(sys.path)
        sys.path.insert(SysPathIdx, self.context.__root__)

        if 'from' in self.source_settings:
            # Import the module, and then grab the attribute out of it
            AttrName = self.settings['attr']
            module = __import__(self.settings['from'], {}, {}, AttrName)
            module = getattr(module, AttrName)
            self.AddNamespace({AttrName: module})
        elif 'module' in self.source_settings:
            # Import the module in a direct fassion
            ModuleName = self.settings['module']
            module = __import__(ModuleName, {}, {})
            self.AddNamespace({ModuleName: module})
        else:
            # Just run the contents!
            module = None
            # Run the code
            localvars = Variables.copy()
            code = compile(self.GetCode(), name, 'exec')
            exec code in localvars
            self.AddNamespace(localvars)

        if module and int(self.settings['reload']):
            reload(module)

        sys.path.pop(SysPathIdx)
        return module

