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

from Foundation.SubjectObserver.CategorySubject import CategorySubjectBaseMixin
from Foundation.SubjectObserver import ProxyBidableCategorySubjectMixin
from Foundation.WeakBind import BoundCallableBase
import JID

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberSubjectBase(ProxyBidableCategorySubjectMixin, CategorySubjectBaseMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FromJIDSubjectMixin(JabberSubjectBase):
    def AddObserver(self, category, *args, **kw):
        self.__super.AddObserver(JID.JID(category), *args, **kw)

    def RemoveObserver(self, category, observer):
        self.__super.RemoveObserver(JID.JID(category), observer)

    def _ProxyObserverList(self, category):
        result = []
        result.extend(self._ObserverList(category[1].from_.noresource()))
        result.extend(self._ObserverList(category[1].from_))
        result.extend(self.__super._ProxyObserverList(category))

        return result

FromJIDSubjectMixin._FromJIDSubjectMixin__super = super(FromJIDSubjectMixin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FromJIDSubject(BoundCallableBase, FromJIDSubjectMixin):
    pass

