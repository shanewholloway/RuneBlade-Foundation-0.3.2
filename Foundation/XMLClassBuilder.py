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

from Foundation import XMLBuilder
import keyword

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementFactory(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class Static(object):
        def __init__(self, result):
            self.result = result
        def __call__(self, *args, **kw):
            return self.result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class InheritFromNextFactory(Exception):
        def __call__(self, *args, **kw):
            raise InheritFromNextFactory, (args, kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class BaseImport(object):
        def __init__(self, PyPathRoot=''):
            self.PyPathRoot = PyPathRoot
            self._CachedElementFactories = {}

        def _DoImport(self, PyPath, Name):
            if self.PyPathRoot and PyPath:
                PyPath = '.'.join((self.PyPathRoot, PyPath))
            elif not PyPath:
                PyPath = self.PyPathRoot
            module = __import__(PyPath, globals(), {}, Name)
            result = getattr(module, Name)
            return result

        def __call__(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if not result: 
                ns, name = node
                if keyword.iskeyword(name): name = name + '_'
                result = self._DoImport('', name)

                ## The following works for another scheme
                ##result = self.DoImport(*node)

                self._CachedElementFactories[node] = result
            return result
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class StaticImport(BaseImport):
        def __init__(self, PyPath, Name, *args, **kw):
            ElementFactory.BaseImport.__init__(self, *args, **kw)
            self.ImportArgs = PyPath, Name
            self.result = None

        def __call__(self, *args, **kw):
            if not self.result:
                self.result = self._DoImport(*self.ImportArgs)
            return self.result
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class NodeImport(BaseImport):
        def __call__(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if not result: 
                ns, name = node
                if keyword.iskeyword(name): name = name + '_'
                result = self._DoImport(name, name)

                ## The following works for another scheme
                ##result = self.DoImport(*node)

                self._CachedElementFactories[node] = result
            return result
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class NamespaceImport(BaseImport):
        def __call__(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if not result: 
                ns, name = node
                if keyword.iskeyword(name): name = name + '_'
                result = self._DoImport('%s.%s' % (ns, name), name)

                ## The following works for another scheme
                ##result = self.DoImport(*node)

                self._CachedElementFactories[node] = result
            return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class TryList(object):
        def __init__(self, trylist, ignoreExceptions=[ImportError, AttributeError, KeyError]):
            self._trylist = trylist
            self._ignoreExceptions = tuple(ignoreExceptions)

        def __call__(self, *args, **kw):
            for each in self._trylist:
                try:
                    return each(*args, **kw)
                except self._ignoreExceptions:
                    pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class CachedTryList(TryList):
        def __init__(self, *args, **kw):
            ElementFactory.TryList.__init__(self, *args, **kw)
            self._CachedElementFactories = {}

        def __call__(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if result: 
                return result
            for each in self._trylist:
                try:
                    result = each(owner, parent, node, attributes, namespacemap)
                    self._CachedElementFactories[node] = result
                    return result
                except self._ignoreExceptions:
                    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementFactorySet(dict):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    NextFactorySet = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def PushFactorySet(self, FactorySet):
        self.NextFactorySet = FactorySet
        return self

    def PopFactorySet(self):
        result = self.NextFactorySet
        self.NextFactorySet = None
        return result

    def copy(self):
        return ElementFactorySet(dict.copy(self))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetElementFactory(self, owner, parent, node, attributes, namespacemap):
        try:
            idx = node
            while idx:
                FactoryFactory = self.get(idx, None)
                if FactoryFactory:
                    result = FactoryFactory(owner, parent, node, attributes, namespacemap)
                    if result: 
                        return result
                idx = idx[:-1]

            # Resort to the default
            FactoryFactory = self.get(None, None)
            if FactoryFactory:
                result = FactoryFactory(owner, parent, node, attributes, namespacemap)
                if result: 
                    return result
            
        except ElementFactory.InheritFromNextFactory, (args, kw):
            if self.NextFactorySet:
                return self.NextFactorySet._GetElementFactory(*args, **kw)

        raise KeyError, "Could not find a class to build for node %r" % (node,)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLClassBuilderMixin(XMLBuilder.XMLBuilderMixin):
    """Mixin that forms the python import indirectly from a dictionary lookup of the namespace, 
    and then combines the result with the node name."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ElementFactories = ElementFactorySet()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def AddElementFactory(self, idx, Factory):
        self.ElementFactorySet[idx] = Factory

    def RemoveElementFactory(self, idx):
        del self.ElementFactorySet[idx]

    def AddElementFactories(self, Factories):
        """Registeres a new mapping between xmlns and python import strings."""
        # Did they send us a real change?
        if Factories:
            # And now update with what they gave us
            self.ElementFactorySet.update(Factories)

    def PushElementFactorySet(self, FactorySet):
        result = self.ElementFactories
        self.ElementFactories = FactorySet.PushFactorySet(result)
        return result

    def PopElementFactorySet(self):
        result = self.ElementFactories
        self.ElementFactories = result.PopFactorySet()
        return result
 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetModifableElementFactoryDict(self):
        # Are we working on the class dictionary?
        if self.ElementFactories is self.__class__.ElementFactories:
            # If so, lets get an instance copy
            self.ElementFactories = self.ElementFactories.copy()
        return self.ElementFactories
    ElementFactorySet = property(_GetModifableElementFactoryDict) 

    def _GetElementFactory(self, owner, parent, node, attributes, namespacemap):
        if self._elements:
            result = self._elements[-1]._xmlChildFactory(owner, parent, node, attributes, namespacemap)
            if result: return result
        return self.ElementFactorySet._GetElementFactory(owner, parent, node, attributes, namespacemap)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLClassBuilder(XMLClassBuilderMixin, XMLBuilder.XMLBuilder):
    pass
