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
from Foundation.Skinning.UtilitySkinElements import IgnoreXML, StoreXML, RestoreStoredXMLMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PyConditionalSkinObject(PySkinObject, RestoreStoredXMLMixin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _ChildFactory = IgnoreXML
    _bStoreChildren = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ XMLBuilderObjectBase Overrides
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, owner, parent, node, attributes, namespacemap): 
        PySkinObject.__init__(self, owner, parent, node, attributes, namespacemap)
        self.owner = owner

    def _xmlChildFactory(self, owner, parent, node, attributes, namespacemap): 
        return self._ChildFactory 

    def _addData(self, data): 
        if self._bStoreChildren:
            return PySkinObject._addData(self, data)
        else: return None

    def _addElement(self, node, obj): 
        if self._bStoreChildren:
            return PySkinObject._addElement(self, node, obj)
        else: return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def StoreChildren(self, flag=1):
        self._bStoreChildren = flag
        if flag: self._ChildFactory = StoreXML
        else: self._ChildFactory = IgnoreXML

    def SkinInitialize(self):
        pass

    def SkinFinalize(self):
        pass

