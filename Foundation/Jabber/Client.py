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

"""Modular Jabber client

Dependencies:
    Foundation.SubjectObserver
    Foundation.Jabber

The Jabber protocol can be found at http://jabber.org, 
and at the time of writting, specifically at 
http://docs.jabber.org/general/html/protocol.html

"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from xml.sax.saxutils import escape, quoteattr
from Foundation.Jabber import ClientNodes
from Foundation.Jabber import JID
from Foundation.Jabber.JabberConnection import JabberConnection
from Foundation import SubjectObserver
from Foundation.XMLClassBuilder import ElementFactory as EF

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Jabber Client Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Client(JabberConnection):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ElementFactories = JabberConnection.ElementFactories.copy()
    ElementFactories.update({
        # http://etherx.jabber.org/streams nodes
        ('http://etherx.jabber.org/streams', 'stream'): EF.Static(ClientNodes.JabberStream),
        ('http://etherx.jabber.org/streams', 'error'): EF.Static(ClientNodes.JabberStreamError),

        # jabber:client nodes
        ('jabber:client', 'presence'): EF.Static(ClientNodes.JabberClientPresence),
        ('jabber:client', 'message'): EF.Static(ClientNodes.JabberClientMessage),
        ('jabber:client', 'iq'): EF.Static(ClientNodes.JabberClientIQ),

        None: EF.Static(ClientNodes.JabberNode), # Default if no match with a defined (namespace, node)
        })

    stream = None
    information = None
    SupportedNS = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        self.stream = SubjectObserver.BidableCategorySubject()
        self.stream.IncludeSend = kw.get('xmlsend', 0)
        self.stream.IncludeRecv = kw.get('xmlrecv', 0)
        self.stream.IncludeTick = kw.get('processtick', 0)
        self.information = SubjectObserver.AttributedSubject.AttributedSubject()
        self.information.jid = JID.JID()
        self.information.authorized = 0
        self.__super.__init__(*args, **kw)
        
        self.SupportedNS = []
        self.__NextID = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetNextID(self):
        """Used by various methods to obtain a "new id" for a message."""
        self.__NextID += 1
        return str(self.__NextID)

    def _SetSocketError(self, exc_class, exc_info, exc_traceback):
        self.stream.UpdateObservers(socket_error=(exc_class, exc_info))
        del exc_class
        del exc_info
        del exc_traceback

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Shutdown(self):
        """Politely disconnects the socket and parser from the jabber stream"""
        self.__super.Shutdown()
        self.information.jid = JID.JID()
        self.information.authorized = 0

    def Authenticate(self, username, password, resource, callback=None):
        """Authenticates with the Jabber server.  
        Assumes basic authentication protocol.

        Returns the iqAuthQuery instance that is sent.

        See also: iqAuthQuery"""
        import iqAuthQuery
        query = iqAuthQuery.iqAuthQuery(self, username, password, resource, callback)
        return query

    def Register(self, username, password, callback=None):
        """Registers a new account with the Jabber server.  
        Assumes basic registration protocol.

        Returns the iqQuery instance that is sent.

        See also: iqQuery"""
        import iqQuery
        strXML = '<username>%s</username><password>%s</password>' % (username, password)
        query = iqQuery.iqQuery(self, callback)
        query.SendQuery("jabber:iq:register", self.ServerJID, 'set', strXML)
        return query

    def SetPassword(self, password, callback=None):
        """Registers a new password with the Jabber server.  
        Assumes user is already authenticated and a basic registration protocol.

        Returns the iqQuery instance that is sent.

        See also: iqQuery"""
        import iqQuery
        strXML = '<password>%s</password>' % password
        query = iqQuery.iqQuery(self, callback)
        query.SendQuery("jabber:iq:register", self.ServerJID, 'set', strXML)
        return query

    def QueryRoster(self, callback=None):
        """Requests the jabber:iq:roster for the currently authenticated JID.

        Returns the iqRosterQuery instance that is sent.

        See also: iqRosterQuery"""
        import iqRosterQuery
        return iqRosterQuery.iqRosterQuery(self, callback)

    def BrowseJID(self, toJID, callback):
        """Requests the jabber:iq:browse data for the currently authenticated JID.

        Returns the iqQuery instance that is sent.

        See also: iqQuery"""
        import iqQuery
        query = iqQuery.iqQuery(self, callback)
        query.SendQuery("jabber:iq:browse", toJID) 
        return query

    def SetPublicData(self, namespace, xml):
        """Saves xml data into namespace.

        Returns the sent XML."""
        return self.SendXML('''<iq id='%s' type='set'><query xmlns='%s'>%s</query></iq> ''' % (self._GetNextID(), namespace, xml))
    SetData = SetPublicData # Alias
 
    def SetPrivateData(self, xml):
        """Saves xml data into the jabber:iq:private.

        Returns the sent XML."""
        return self.SetData('jabber:iq:private', xml)

    def GetPublicData(self, namespace, callback=None, xml=''):
        """Requests the data stored in namespace.

        Returns the iqQuery instance that is sent.

        See also: iqQuery"""
        return self.Query(namespace, '', type='get', callback=callback, xml=xml)
    GetData = GetPublicData # Alias

    def GetPrivateData(self, callback=None, xml=''):
        """Requests the data stored in jabber:iq:private.

        Returns the iqQuery instance that is sent.

        See also: iqQuery"""
        return self.GetData('jabber:iq:private', callback=callback, xml=xml)

    def Query(self, namespace, toJID='', type='get', callback=None, xml=''):
        """Sends a jabber:client iq query to toJID.

        Returns the iqQuery instance that is sent.

        See also: iqQuery"""
        import iqQuery
        query = iqQuery.iqQuery(self, callback)
        query.SendQuery(namespace, toJID, type=type, xml=xml)
        return query

    def Message(self, toJID, body='', subject='', type='message', id=None, xml=''):
        """Sends a jabber:client message to toJID.

        Returns the sent XML."""
        idMessage = id or self._GetNextID()
        strXML = '<message id=%s to=%s type=%s>' % (quoteattr(idMessage), quoteattr(toJID), quoteattr(type))
        strXML += xml
        if subject: 
            strXML += '<subject>%s</subject>' % escape(subject)
        if body:
            strXML += '<body>%s</body>'  % escape(body) 
        strXML += '</message>'
        return self.SendXML(strXML)

    def Presence(self, toJID='', status='', show='', type='available', priority=None, xml=''):
        """Sends a jabber:client presence to toJID or everyone if not toJID.

        Returns the sent XML."""
        idPresence = self._GetNextID()
        strXML = '<presence id=%s ' % quoteattr(idPresence)
        if type: strXML += 'type=%s ' % quoteattr(type)
        if toJID: strXML += 'to=%s ' % quoteattr(toJID)
        strXML += '>'

        if priority is not None: strXML += '<priority>%s</priority>'  % escape(str(priority))
        if show: strXML += '<show>%s</show>'  % escape(show) 
        if status: strXML += '<status>%s</status>' % escape(status)
        if xml: strXML += xml
        strXML += '</presence>'
        return self.SendXML(strXML)

    def Subscribe(self, toJID, type='subscribe'):
        """Sends a jabber:client presence subscribe request to toJID.

        Returns the sent XML."""
        return self.Presence(toJID=toJID, type=type)

    def Unsubscribe(self, toJID, type='unsubscribe'):
        """Sends a jabber:client presence unsubscribe request to toJID.

        Returns the sent XML."""
        return self.Presence(toJID=toJID, type=type)

#~ Make a super ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Client._Client__super = super(Client)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExtendedClient(Client):
    def __init__(self, *args, **kw):
        self.__super.__init__(*args, **kw)
        self.stream.IncludeSend = kw.get('xmlsend', 0)
        self.stream.IncludeRecv = kw.get('xmlrecv', 0)
        self.stream.IncludeTick = kw.get('processtick', 0)

    def _SocketRecv(self, limit=8192):
        """Overrides socket access so that stream events can be created."""
        result = self.__super._SocketRecv(limit)
        if self.stream.IncludeRecv and result: self.stream.UpdateObservers(xmlrecv=result)
        return result

    def _SocketSend(self, data):
        """Overrides socket access so that stream events can be created."""
        if self.stream.IncludeSend and data: self.stream.UpdateObservers(xmlsend=data)
        return self.__super._SocketSend(data)

    def _NeedsRead(self, *args, **kw):
        """Overrides SmartSelect mechanism to signal stream processtick events."""
        result = self.__super._NeedsRead(*args, **kw)
        if self.stream.IncludeTick and result: self.stream.UpdateObservers(processtick=1)
        return result

#~ Make a super ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ExtendedClient._ExtendedClient__super = super(ExtendedClient)

