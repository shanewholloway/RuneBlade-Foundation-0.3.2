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

from Foundation.Skinning.xmlPython import evaluate

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class substitute(evaluate.evaluate):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = evaluate.evaluate.default_settings.copy()
    default_settings['attr'] = None
    default_settings['nsprefix'] = None
    default_settings['namespace'] = None
    default_settings['node'] = None

    _ObjectAsXML = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinFinalize(self):
        result = evaluate.evaluate.SkinFinalize(self)

        if 'node' in self.source_settings:
            self.parent().__node__ = self.object
        elif 'ns' in self.source_settings:
            self.parent().__namespace__ = self.object
        elif 'namespace' in self.source_settings:
            self.parent().__namespace__ = self.object
        elif 'nsprefix' in self.source_settings:
            self.parent().__namespace_map__[self.settings['nsprefix'] or None] = self.object
        elif 'attr' in self.source_settings:
            self.parent().settings[self.settings['attr']] = self.object
        elif 'contextvar' in self.source_settings: pass
        elif 'parentvar' in self.source_settings: pass
        elif 'contextnode' in self.source_settings: pass
        elif 'parentnode' in self.source_settings: pass
        else:
            self._ObjectAsXML = 1

        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _toXML(self, strSplit='', *args, **kw):
        if self._ObjectAsXML:
            result = [str(self.object)]
        else: result = []

        if strSplit is not None: return strSplit.join(result)
        else: return result
