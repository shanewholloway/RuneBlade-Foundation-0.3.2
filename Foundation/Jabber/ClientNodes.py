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

"""XMLBuilder compatable Jabber nodes for use in Foundation.Jabber.Client

Dependencies:
    Foundation.XMLObjectify
    weakref
    re

"""
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
import re
from Foundation import XMLObjectify

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Jabber Node Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberNode(XMLObjectify.ObjectifiedXML):
    """Default node class for a Jabber XML node."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, client, *args, **kw):
        self._client = weakref.proxy(client)
        XMLObjectify.ObjectifiedXML.__init__(self, client, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Content(self):
        """Returns all the PCData of the Node as a list of strings"""
        return self(None)

    def Elements(self, node=None, namespace=None):
        """Gets all of the child nodes of this node that match node or namespace as regular expressions."""
        elementList = self._elements
        if namespace is not None:
            match = re.compile(namespace).match
            elementList = [element for element in elementList if match(element[0][0])]

        if node is None: elementList = [element[1] for element in elementList if element[0][1]]
        elif node == '*': elementList = [element[1] for element in elementList]
        else: 
            match = re.compile(node).match
            elementList = [element[1] for element in elementList if match(element[0][1])]
        return elementList

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberStream(JabberNode):
    """Jabber node for the root Jabber tag. 
    Namely stream:stream where xmlns:stream='http://etherx.jabber.org/streams'

    Note that we do not care if there is any PCData, 
    nor does the root node keep its child nodes.  
    This allows for those nodes to be deallocated
    after they are processed. 
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _xmlInitStarted(self):
        self._client.ServerJID = self.from_
        self._client.stream.UpdateObservers(settings=self)
    def _addElement(self, node, element): pass
    def _addData(self, data): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberStreamError(JabberNode):
    """Jabber node for stream errors.  (Mostly invalid XML in my experience.)
    stream:error where xmlns:stream='http://etherx.jabber.org/streams'

    Raises JabberStreamError.JabberStreamError
    """

    class JabberStreamError(Exception): pass

    def _xmlInitComplete(self):
        self._client.stream.UpdateObserversEx({self.__node__: self})
        self._client.Shutdown()
        raise JabberStreamError.JabberStreamError, self._toXML()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberClientNode(JabberNode):
    """Jabber nodes base for jabber:client nodes.  
    When the node is completely built, the client stream 
    subject's observers are updated"""

    def _xmlInitComplete(self):
        if self.__namespace__ == 'jabber:client':
            self._client.stream.UpdateObserversEx({self.__node__: self})
         
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberClientPresence(JabberClientNode):
    """Provides jabber:client presence specific default attribute values to reduce
    the quantity of conditional code."""
    _default_attributes = {'from':'', 'type':'available', 'id':'default_presence_id'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberClientMessage(JabberClientNode):
    """Provides jabber:client presence specific default attribute values to reduce
    the quantity of conditional code."""
    _default_attributes = {'from':'', 'to':'', 'type':'message', 'id':'default_message_id'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberClientIQ(JabberClientNode):
    """Provides jabber:client presence specific default attribute values to reduce
    the quantity of conditional code."""
    _default_attributes = {'from':'', 'type':'get', 'id':'default_iq_id'}

