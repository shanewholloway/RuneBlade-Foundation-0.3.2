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

"""Abstract base classes for building Python object trees from an XML stream.

Classes:

    XMLBuilderObjectBase
    XMLBuilderMixin
    XMLBuilder

History:

    Please see XMLObjectify's history.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from xml.parsers.expat import ParserCreate as _ParserCreate
from WeakBind import BindCallable as _BindCallable
from Foundation.ChainedDict import ChainedDict

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLBuilderObjectBase(object):
    """Base class for objects created by XMLBuilderMixin derived classes."""
    def __init__(self, owner, parent, node, attributes, namespacemap): pass
    def _addElement(self, node, obj): pass
    def _addData(self, data): pass
    def _xmlInitStarted(self): pass 
    def _xmlInitComplete(self): pass 
    def _xmlChildFactory(self, owner, parent, node, attributes, namespacemap): return None
    def _toXML(self, strSplit='', *args, **kw):
        if strSplit is not None: return strSplit.join([])
        else: return []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
class XMLBuilderMixin(object): 
    """Abstract base class that guides the building of python objects from XML.  
    Depends upon the interface defined by XMLBuilderObjectBase."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _encoding = 'ASCII'
    _seperator = '.'
    _ParserFactory = _ParserCreate
    NamespaceSynonyms = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self._elements = []
        self._current_namespacemap = ChainedDict()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetElementFactory(self, owner, element, node, attributes, namespacemap):
        """Allows a derived class to return an instance factory (a class, since python is so awesome) for 
        this particular data.  The template method makes no restrictions, except that the instance factory
        must be able to accept the same arguments as this method."""
        raise KeyError, 'No Class Registered: %s %s' % node

    def _GetOwner(self):
        """Used by _start_element to point to the owner of the node.  Derived classes should
        override this method the owner is different than the XMLBuilder"""
        return self

    def _start_namespace_decl_handler(self, prefix, uri):
        """Part of the tree-style template method, called at the before the beginning of an XML node parse 
        to manage namespaces."""
        self._current_namespacemap [uri] = prefix

    def _end_namespace_decl_handler(self, prefix):
        """Part of the tree-style template method, called at the after the end of an XML node parse 
        to manage namespaces."""
        pass

    def _start_element(self, name, attributes):
        """Part of the tree-style template method, called at the beginning of an XML node parse.
        Instantiates the element returned by _GetElementFactory."""

        node = self._SplitQualifiedName(name)

        newattributes = {}
        for attrname, attrvalue in attributes.iteritems():
            attrnamespace, attrname = self._SplitQualifiedName(attrname)
            if not attrnamespace or attrnamespace == node[0]: 
                newattributes[node[0], attrname] = attrvalue
                newattributes[attrname] = attrvalue
            else: newattributes[attrnamespace, attrname] = attrvalue

        self._current_namespacemap = ChainedDict({}, self._current_namespacemap)

        args = (self._GetOwner(), self._elements and self._elements[-1] or None, node, newattributes, self._current_namespacemap.chained)
        build_factory = self._GetElementFactory(*args)
        newelement = build_factory(*args)
        if self._elements:
            self._elements[-1]._addElement(node, newelement)
        self._elements.append(newelement)
        self._elements[-1]._xmlInitStarted()

    def _end_element(self, name):
        """Part of the tree-style template method, called at the closing of an XML node parse.
        Simply notifies the element that it is complete."""
        self._current_namespacemap = ChainedDict({}, self._current_namespacemap.chained)

        if self._elements:
            result = self._elements.pop()
            result._xmlInitComplete()
        else: result = None

        return result

    def _char_data(self, data):
        """Part of the tree-style template method, called when PCData is found."""
        self._elements[-1]._addData(data)

    def SetParserFactory(self, ParserFactory):
        self._ParserFactory = ParserFactory

    def _SplitQualifiedName(self, combined):
        idx = combined.rfind(self._seperator)
        if idx < 0: 
            namespace = None
            name = combined
        else: 
            namespace = combined[0:idx]
            name = combined[idx + len(self._seperator):]
        namespace = self.NamespaceSynonyms.get(namespace, namespace)
        return namespace, name

    def _CreateParser(self):
        """Creates the Expat parser in a python-OO way."""
        parser = self._ParserFactory(self._encoding, self._seperator)
        parser.returns_unicode = self._encoding != 'ASCII' and 1 or 0
        parser.StartElementHandler = _BindCallable(self._start_element)
        parser.EndElementHandler = _BindCallable(self._end_element)
        parser.CharacterDataHandler = _BindCallable(self._char_data)
        parser.StartNamespaceDeclHandler = _BindCallable(self._start_namespace_decl_handler)
        parser.EndNamespaceDeclHandler = _BindCallable(self._end_namespace_decl_handler)
        return parser

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLBuilder(XMLBuilderMixin):
    """Abstract base class closer to actualizing python object building.  
    See XMLObjectify, or XMLClassBuilder for more concrete builders."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __call__(self, *args, **kw):
        """Calls ParseFile if the first argument is an open file, and Parse otherwise."""
        if isinstance(args[0], file):
            return self.ParseFile(*args, **kw)
        else: return self.Parse(*args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Parse(self, *args, **kw):
        """Starts the building of python objects using the XML parser.  Assumes first argument is string-like object."""
        parser= self._PreParse()
        parser.Parse(*args, **kw)
        return self._PostParse(parser)

    def ParseFile(self, *args, **kw):
        """Starts the building of python objects using the XML parser.  Assumes first argument is a file-like object."""
        parser= self._PreParse()
        parser.ParseFile(*args, **kw)
        return self._PostParse(parser)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _end_element(self, name):
        """Manages the _LastCompleteElement variable."""
        self._LastCompleteElement = XMLBuilderMixin._end_element(self, name)

    def _PreParse(self):
        """Few initialization things to be done at the beginning of a parse session."""
        self._elements, self._LastCompleteElement  = [], None
        return self._CreateParser()

    def _PostParse(self, parser):
        """Few cleanup things to be done at the end of a parse session."""
        result, self._LastCompleteElement = self._LastCompleteElement, None
        return result

