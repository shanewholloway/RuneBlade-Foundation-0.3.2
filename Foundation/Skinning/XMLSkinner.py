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

from Foundation.XMLClassBuilder import XMLClassBuilder
from Foundation.WeakBind import BindCallable
import SkinContext
import SkinObject
import weakref
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLSkinner(XMLClassBuilder):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, mapSupportedSkinNamespaces={}, rootPath=''):
        self.rootPath = rootPath
        XMLClassBuilder.__init__(self)
        self.AddElementFactories(mapSupportedSkinNamespaces)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinXML(self, xml, contextIn=None, **kwAddedContext):
        rootPath = self.rootPath or os.getcwd()
        self._elements, self._LastCompleteElement  = [], None
        parser = self._CreateParser()
        self.context = SkinContext.SkinContext(contextIn, kwAddedContext)
        self.context.__skinner__ = weakref.ref(self)
        self.context.__root__ = rootPath
        
        parser.Parse(xml)

        self.context = None
        result, self._LastCompleteElement = self._LastCompleteElement, None
        del self._elements
        del self._LastCompleteElement
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinFile(self, file, contextIn=None, **kwAddedContext):
        if isinstance(file, str):
            rootPath = os.path.dirname(os.path.abspath(file))
            file = os.path.abspath(file)
            file = open(file, 'r')
        else: rootPath = kwAddedContext.get('__root__', None) or self.rootPath or os.getcwd()

        self._elements, self._LastCompleteElement  = [], None
        parser = self._CreateParser()
        self.context = SkinContext.SkinContext(contextIn, kwAddedContext)
        self.context.__skinner__ = weakref.ref(self)
        self.context.__root__ = rootPath

        parser.ParseFile(file)

        self.context = None
        result, self._LastCompleteElement = self._LastCompleteElement, None
        del self._elements
        del self._LastCompleteElement
        return result
 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GraftXML(self, GraftElements, xml, **kwAddedContext):
        rootPath = self.rootPath or os.getcwd()
        self._elements, self._LastCompleteElement = GraftElements, GraftElements[-1]

        parser = self._CreateParser()

        parentContext = GraftElements[-1].context
        self.context = SkinContext.SkinContext(parentContext, kwAddedContext)
        self.context.__skinner__ = weakref.ref(self)
        self.context.__root__ = rootPath
        self._LastCompleteElement.context = self.context

        parser.Parse(file)

        self.context = None
        GraftElements[-1].context = parentContext
        result, self._LastCompleteElement = self._LastCompleteElement, None
        del self._elements
        del self._LastCompleteElement
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GraftFile(self, GraftElements, file, **kwAddedContext):
        if isinstance(file, str):
            rootPath = os.path.dirname(os.path.abspath(file))
            file = os.path.abspath(file)
            file = open(file, 'r')
        else: rootPath = kwAddedContext.get('__root__', None) or self.rootPath or os.getcwd()

        self._elements, self._LastCompleteElement = GraftElements, GraftElements[-1]

        parser = self._CreateParser()

        parentContext = GraftElements[-1].context
        self.context = SkinContext.SkinContext(parentContext, kwAddedContext)
        self.context.__skinner__ = weakref.ref(self)
        self.context.__root__ = rootPath
        self._LastCompleteElement.context = self.context

        parser.ParseFile(file)

        self.context = None
        GraftElements[-1].context = parentContext
        result, self._LastCompleteElement = self._LastCompleteElement, None
        del self._elements
        del self._LastCompleteElement
        return result
 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _SkinXMLFromTopElement(self, xml, kwAddedContext):
        element = self._elements[-1]
        parser = self._CreateParser()
        element.context.__skinner__ = weakref.ref(self)
        element.context._update(kwAddedContext)

        parser.Parse(xml)

        return self._LastCompleteElement
  
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _SkinFileFromTopElement(self, file, kwAddedContext):
        element = self._elements[-1]
        if isinstance(file, str):
            rootPath = os.path.dirname(os.path.abspath(file))
            file = os.path.join(element.context.__root__, file)
            file = os.path.abspath(file)
            file = open(file, 'r')
        else: rootPath = ''

        parser = self._CreateParser()
        element.context.__skinner__ = weakref.ref(self)
        if rootPath: element.context.__root__ = rootPath
        element.context._update(kwAddedContext)

        parser.ParseFile(file)

        return self._LastCompleteElement
