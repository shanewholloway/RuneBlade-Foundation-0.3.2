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

from Foundation.XMLBuilder import XMLBuilderObjectBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IgnoreXML(XMLBuilderObjectBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _xmlChildFactory(self, owner, parent, node, attributes, namespacemap): 
        return self.__class__

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StoreXML(XMLBuilderObjectBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, owner, parent, node, attributes, namespacemap): 
        self.owner, self.parent, self.node, self.attributes, self.namespacemap = owner, parent, node, attributes, namespacemap
        self.children = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Restore(self, owner=None):
        owner = owner or self.owner

        # Emulate the namespace start calls
        for uri, prefix in self.namespacemap.iteritems():
            owner._start_namespace_decl_handler(prefix, uri)

        # Construct the joined node name
        sep = owner._seperator
        name = sep.join(self.node)

        newattributes = {}
        for attrname, attrvalue in self.attributes.iteritems():
            if isinstance(attrname, tuple): 
                if attrname[1] not in self.attributes:
                    attrname = sep.join(attrname)
                    newattributes[attrname] = attrvalue
            else:
                newattributes[attrname] = attrvalue

        # Emulate the Start of an element
        owner._start_element(name, newattributes)

        self.RestoreChildren(owner)

        # Emulate the End of an element
        owner._end_element(name)

        # Emulate the namespace end calls
        for prefix in self.namespacemap.itervalues():
            owner._end_namespace_decl_handler(prefix)

    def RestoreChildren(self, owner=None):
        owner = owner or self.owner
        # Emulate the Sub Elements
        for each in self.children:
            if each[0]: each[-1].Restore(owner)
            else: owner._char_data(each[-1])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _addElement(self, node, obj): 
        self.children.append((1, obj))

    def _addData(self, data):
        self.children.append((0, data))

    def _xmlInitStarted(self): 
        pass 

    def _xmlInitComplete(self): 
        pass

    def _xmlChildFactory(self, owner, parent, node, attributes, namespacemap): 
        return self.__class__

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RestoreStoredXMLMixin(object):
    def RestoreChildren(self, owner=None):
        owner = owner or self.owner
        for each in self.children:
            if each[0]: each[-1].Restore(owner)
            else: owner._char_data(each[-1])
