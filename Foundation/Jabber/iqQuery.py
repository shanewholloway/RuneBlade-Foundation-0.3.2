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

import weakref
from xml.sax.saxutils import escape, quoteattr
from Foundation.WeakBind import BindCallable
import JabberObserver as JObs
import JID
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqQueryBase(JObs.JabberObserver):
    def __init__(self, JC, callback=None, BidValue=1):
        JObs.JabberObserver.__init__(self, callback, BidValue=BidValue)
        if isinstance(JC, weakref.ReferenceType):
            self.JC = JC
        else: self.JC = weakref.ref(JC)
        self.JC().stream.AddObserver('iq', self)

    def SendQuery(self, namespace, jid='', type='get', xml='', idQuery=None, bSetLink=1):
        # Get a new id
        idQuery = idQuery or self.JC()._GetNextID()

        # Setup our match attributes
        del self.Match[:]
        if jid: self.Match.append(JObs.MatchAttributes(from_=JID.JID(jid)))
        if idQuery: self.Match.append(JObs.MatchAttributes(id=idQuery))
        self.Match.append(JObs.MatchHasChildNamespace(namespace))
        
        # and finally send the query
        self.JC().SendXML(self._BuildQuery(namespace, xml, type=type, id=idQuery, to=jid))
        return self
    
    def _BuildQuery(self, namespace, xml, **attrQuery):
        # Build the XML attribute string
        strAttributes = ' '.join([ ('%s=%s' % (a[0], quoteattr(a[1]))) for a in attrQuery.iteritems() if a[1]] )
        # Return the built xml
        return '''<iq %s ><query xmlns=%s>%s</query></iq>''' % (strAttributes, quoteattr(namespace), xml)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class iqQuery(iqQueryBase):
    _serviced = 0
    def __nonzero__(self):
        if self._serviced: return 0
        else: return super(iqQuery, self).__nonzero__()
    def __call__(self, *args, **kw):
        self._serviced = 1
        return super(iqQuery, self).__call__(*args, **kw)
