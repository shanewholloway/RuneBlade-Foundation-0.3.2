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

"""Subject/Observer with bells on.

The goal of this package is to make both observers and subjects very simple to create
maintain, while retaining both flexable and powerful subjects / observers.  The simplest
observers are just callable objects, and the simplest subjects keep a list of observers
to notify.  More advanced classes include bidable, attributed, and categorized 
subject/observers.

This main module collects and blends many of the subject and observer types to create
extremely useful subjects and observers.  
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import Observer as _Observer
import Subject as _Subject
import CategorySubject as _CategorySubject
import AttributedSubject as _AttributedSubject
import BidableSubject as _BidableSubject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AttributedCategorySubject(_AttributedSubject.AttributedSubjectMixin, _CategorySubject.CategorySubjectMixin, _Subject.Subject): 
    pass
class AttributedBidableSubject(_AttributedSubject.AttributedSubjectMixin, _BidableSubject.BidableSubjectMixin, _Subject.Subject):
    pass
class AttributedBidableCategorySubject(_AttributedSubject.AttributedSubjectMixin, _BidableSubject.BidableSubjectMixin, _CategorySubject.CategorySubjectMixin, _Subject.Subject):
    pass

class BidableCategorySubject(_BidableSubject.BidableSubjectMixin, _CategorySubject.CategorySubjectMixin, _Subject.Subject):
    pass
class BidableAttributedSubject(_AttributedSubject.AttributedSubjectMixin, _BidableSubject.BidableSubjectMixin, _Subject.Subject):
    pass
class BidableAttributedCategorySubject(_AttributedSubject.AttributedSubjectMixin, _BidableSubject.BidableSubjectMixin, _CategorySubject.CategorySubjectMixin, _Subject.Subject):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProxyBidableCategorySubjectMixin(object):
    """Allows some subject to proxy for a different subject as an observer of that subject, 
    while maintaining bid-sequences and categories"""

    def __call__(self, subject, **UpdateDict):
        pass

    def _ProxyObserverList(self, category):
        return self._ObserverList(category[0])

    def Bid(self, subject, **UpdateDict):
        for value in UpdateDict.iteritems():
            for obs in self._ProxyObserverList(value):
                subject._GetBid(obs, UpdateDict)
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProxyBidableSubjectMixin(object):
    """Allows some subject to proxy for a different subject as an observer of that subject, 
    while maintaining bid-sequences"""

    def __call__(self, subject, **UpdateDict):
        pass
        
    def _ProxyObserverList(self):
        return self._ObserverList()

    def Bid(self, subject, **UpdateDict):
        for obs in self._ProxyObserverList():
            subject._GetBid(obs, UpdateDict)
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_SubjectObservers():
    def printo1(subject, **UpdateDict):
        print "O1: ", UpdateDict
    def printo2(subject, **UpdateDict):
        print "O2: ", UpdateDict
    def printo3(subject, **UpdateDict):
        print "O3: ", UpdateDict
    s1 = _Subject.Subject()
    s2 = _AttributedSubject.AttributedSubject()
    s3 = AttributedCategorySubject()

    s1.AddObserver(printo1)
    s1.AddObserver(printo2, priority=-1)
    s2.AddObserver(printo2)

    s1.UpdateObservers(Hello='World')
    s2.UpdateObservers(Goodbye='Complexity')

    s2.NewValue = 'A New Value'

    print "Locked"
    lock = s1.Lock()
    s1.UpdateObservers(Locked='Update')
    print "Post-lock"
    del lock
    print "Unlocked"

    o3 = _Observer.Observer(printo3)
    s3.AddObserver('CategoryA', printo1)
    s3.AddObserver('CategoryB', printo2)
    s3.AddObserver('CategoryC', o3)

    s3.Nobody = 1
    s3.CategoryA = 'Hello'
    s3.CategoryC = 'Goodbye'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    _Test_SubjectObservers() 
    print "Test complete."

