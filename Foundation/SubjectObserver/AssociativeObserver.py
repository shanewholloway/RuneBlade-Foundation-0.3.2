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

"""Observer implementation that can delegate multiple input updates to multiple
receivers based on what the delegate observer is interested in.  Note: This is less
effecient than Subject-side category based filtering, but does not depend upon the 
subject implementing the category interface.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Foundation.WeakBind import BindCallable
from Foundation.SubjectObserver import ProxyBidableCategorySubjectMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AssociativeObserver(ProxyBidableCategorySubjectMixin):
    def __init__(self):
        self._associations = {}

    def AddAssociation(self, category, observer):
        self._associations.setdefault(category, []).append(BindCallable(observer))
        return self

    def _ObserverList(self, category):
        return self._associations.get(category, [])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    import BidableSubject
    s = BidableSubject.BidableSubject()
    from Observer import Observer

    def AssertSubject(subject, value):
        assert subject is s
    def AssertFalse(subject, value):
        assert 0

    ao = AssociativeObserver()
    s.AddObserver(ao)

    ao.AddAssociation('test', Observer(AssertFalse, 100))
    ao.AddAssociation('test', Observer(AssertFalse, -1))

    ao.AddAssociation('value', Observer(AssertFalse, 9))
    ao.AddAssociation('value', Observer(AssertSubject, 10))
    ao.AddAssociation('value', Observer(AssertSubject))
    ao.AddAssociation('value', AssertSubject)

    ao.AddAssociation('value2', Observer(AssertSubject))
    ao.AddAssociation('value2', AssertSubject)

    s.UpdateObservers(value=42)

    print "Test complete."

