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

from xml.sax.saxutils import escape, quoteattr
from Foundation.XMLObjectify import BaseObjectifiedXML 
from Foundation.Jabber import JID
from Foundation.Jabber.JabberConnection import JabberConnection
from Foundation import SubjectObserver
from Foundation.XMLClassBuilder import ElementFactory as EF
import sha 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Component(JabberConnection):
    # NOTE: Very preliminary!

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ElementFactories = JabberConnection.ElementFactories.copy()
    ElementFactories.update({
        None: EF.Static(BaseObjectifiedXML), 
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Startup(self, JabberServerURL, port, ServerJID=None, namespace='jabber:component:accept', **kw):
        return super(Component, self).Startup(JabberServerURL, port, ServerJID, namespace, **kw)

    def Handshake(self, secret, id=None):
        data = sha.new(id or self.id)
        data.update(secret)
        self.SendXML('<handshake>%s</handshake>' % data.hexdigest())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    import sys
    jc = Component('cvs-holloways', 5999, 'shanetest.cvs-holloways', fileIn=sys.stdout, fileOut=sys.stdout)
    jc.ProcessPending(1.0)
    print "Test complete."


