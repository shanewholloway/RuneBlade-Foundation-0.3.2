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

"""Observer implementation.

Note: You only need an Observer instance if you need to place a bid value.
otherwise the callable object can be passed straight to the subject.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Foundation.WeakBind import BoundCallable, BindCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Observer(BoundCallable):
    """Note: Only needed if you are adding a Bid value to the observer;
    otherwise the callable object can be passed straight to the subject."""

    def __init__(self, callback=None, Bid=None):
        super(Observer, self).__init__(callback or self.Update)
        self.SetBid(Bid)

    def SetBid(self, Bid=None):
        if callable(Bid): 
            self.Bid = BindCallable(Bid)
        elif Bid: 
            self.Bid = Bid
        elif hasattr(self, 'Bid'): 
            del self.Bid

    def Update(self, subject, **UpdateDict):
        print "On Update:", subject.__class__.__name__, UpdateDict


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    import BidableSubject
    s = BidableSubject.BidableSubject()

    def AssertSubject(subject, value):
        assert subject is s
    def AssertFalse(subject, value):
        assert 0
    
    s.AddObserver(Observer(AssertSubject, 10))
    s.AddObserver(Observer(AssertFalse, 9))
    s.AddObserver(Observer(AssertFalse, 8))
    s.AddObserver(Observer(AssertFalse, -1))
    # The following two will get called because of no bid value
    s.AddObserver(Observer(AssertSubject))
    s.AddObserver(AssertSubject)

    s.UpdateObservers(value=42)
    print "Test complete."

