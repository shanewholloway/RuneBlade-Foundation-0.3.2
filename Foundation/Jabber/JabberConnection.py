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

"""Very basic Jabber client.

Dependencies:
    Foundation.SmartSelect
    Foundation.XMLBuilder
    socket

The Jabber protocol can be found at http://jabber.org, 
and at the time of writting, specifically at 
http://docs.jabber.org/general/html/protocol.html

"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Foundation.XMLBuilder import XMLBuilderObjectBase
from Foundation.XMLClassBuilder import XMLClassBuilderMixin
from Foundation import SmartSelect
from Foundation.WeakBind import BindCallable
import JID
import sys
import socket
import select

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_xmlJabberHeader = '''<?xml version="1.0" encoding="UTF-8" ?><stream:stream to="%s" xmlns="%s" xmlns:stream="http://etherx.jabber.org/streams">'''
_xmlJabberFooter = '''</stream:stream>'''


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberConnection(XMLClassBuilderMixin, SmartSelect.SmartSelectClientBase):
    """Very basic Jabber client, including:
        - Smart select socket handling, 
        - Structured XML parsing, 
        - Initializing and finalizing connection with the Jabber Server
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _socket = None
    _parser = None
    ServerJID = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        # Base code
        XMLClassBuilderMixin.__init__(self)

        if args or kw:
            self.Startup(*args, **kw)

    def __del__(self):
        if self: self.Shutdown()

    def __nonzero__(self):
        return self._socket and 1 or 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Startup(self, JabberServerURL, port=5222, ServerJID=None, namespace='jabber:client', fileIn=None, fileOut=None, **kw):
        """Creates a Socket and XML parser to handle connection to a Jabber server.

        JabberServerURL & port specify how the socket is connected to Jabber server, 
        ServerJID is to be set if the ServerJID is different than the JabberServerURL hostname, and
        fileIn and fileOut should be file-like-objects to receive the influx and outflux streams.

        """
        self._SetDebug(fileIn, fileOut)

        # Create the sendData buffer and lock
        try:
            self._sendData = ''
            import threading
            self._sendDataLock = threading.Lock()
        except ImportError:
            self._sendDataLock = None

        # Create our socket
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            params = JID.reJabberURL.split(JabberServerURL)[1:-1]
            self._socket.connect((params[0], port))
        except socket.error:
            self._SetSocketError(*sys.exc_info())
            raise
        self.fileno = self._socket.fileno
        
        self.ServerJID = JID.JID(ServerJID or params[0])

        # Create our xml parser
        self._parser = self._CreateParser()

        # Send the initial header
        self.SendXML(_xmlJabberHeader % (self.ServerJID, namespace))

    def Shutdown(self):
        """Politely disconnects the socket and parser from the jabber stream"""
        if __debug__: print 'Disconnecting %s from %s' % (self.__class__.__name__, self.ServerJID)
        if self._socket: 
            try: self._SendXMLImmediate('%s' % _xmlJabberFooter)
            except socket.error: pass
        if self._fileIn: print >> self._fileIn, _xmlJabberFooter
        self._socket = None
        self._parser = None

    def _SetDebug(self, fileIn, fileOut):
        """Sets the debug input and output files (or file-like-objects).  
        These can also be passed in when creating the Jabber Client"""
        self._fileIn = fileIn
        self._fileOut = fileOut

    def BuildJID(self, username='', server='', resource=''):
        """Returns a JID that will resolve to username@server/resource.  
        Additionally, if you simply want the corresponding JID on the current 
        Jabber Server, all you need to pass is the username."""
        return JID.JID.join(username, server or self.ServerJID, resource)
        
    def SendXML(self, xml):
        """Sends bare-bones xml data on the socket.  
        Note: the xml is not checked for validity, but the Jabber Servers get
        pretty upset when the data is invalid, and they tend to sever the socket."""
        try:
            if self._sendDataLock: self._sendDataLock.acquire()
            self._sendData += xml
        finally:
            if self._sendDataLock: self._sendDataLock.release()
        return xml

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ XMLBuilding Private Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _start_element(self, name, attributes):
        """Used internally by the XML parsing mechanism.  
        This override replaces jid-related attributes with a JID class instance."""
        if name[:7] == 'jabber:':
            for key in ('to', 'from', 'jid'):
                if key in attributes: 
                    attributes[key] = JID.JID(attributes[key])
        return self.__super._start_element(name, attributes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Smart Select Private Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _NeedsRead(self): 
        """Used by the SmartSelect mechanism to signal when reading is needed."""
        return self._socket and 1
    def _ProcessRead(self):
        """Called by the SmartSelect mechanism when the socket is ready to be read from."""
        data = self._SocketRecv()
        if self._fileIn: print >> self._fileIn, data
        self._parser.Parse(data)
         
    def _NeedsWrite(self): 
        """Used by the SmartSelect mechanism to signal when writing is needed."""
        return self._socket and self._sendData and 1 or 0
    def _ProcessWrite(self):
        """Called by the SmartSelect mechanism when the socket is ready to be written to."""
        try:
            if self._sendDataLock: self._sendDataLock.acquire()
            nSent = self._SocketSend(self._sendData)
            if self._fileOut: print >> self._fileOut, self._sendData[:nSent]
            self._sendData = self._sendData[nSent:]
        finally:
            if self._sendDataLock: self._sendDataLock.release()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Other Private Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _SendXMLImmediate(self, xml):
        """Similar to SendXML, except that _SendXMLImmediate only returns when all the pending
        XML data has been written to the socket."""
        try:
            if self._sendDataLock: self._sendDataLock.acquire()
            self._sendData += xml
            while self._sendData and select.select([], [self._socket], [], 0.5):
                nSent = self._SocketSend(self._sendData)
                if self._fileOut: print >> self._fileOut, self._sendData[:nSent]
                self._sendData = self._sendData[nSent:]
        finally:
            if self._sendDataLock: self._sendDataLock.release()

    def _SocketRecv(self, limit=8192):
        try:
            return self._socket.recv(limit)
        except socket.error:
            self._SetSocketError(*sys.exc_info())
            raise

    def _SocketSend(self, data):
        try:
            return self._socket.send(data)
        except socket.error:
            self._SetSocketError(*sys.exc_info())
            raise

    def _SetSocketError(self, exc_class, exc_info, exc_traceback):
        del exc_class
        del exc_info
        del exc_traceback

# Keep the super around for speed
JabberConnection._JabberConnection__super = super(JabberConnection)
