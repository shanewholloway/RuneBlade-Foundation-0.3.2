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

"""Adds bidding to the Subject/Observer mechanism so that
observers can "voluntarily" be out-bid to provide for 
state-dependant event handling.  

In order to bid, the observer must have a 'Bid' attribute
(value or callable), and the highest bidder wins, as defined
by the > operator."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Subject import Subject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BidableSubjectMixin(object):
    def _GetBid(self, observer, UpdateDict):
        bid = getattr(observer, 'Bid', None)
        if bid is None:
            # This client does not payattention to bids... 
            observer(self, **UpdateDict)
        else:
            if callable(bid):
                bid = bid(self, **UpdateDict)
            if bid:
                if bid > self._bids[0]:
                    self._bids = bid, [observer]
                elif bid == self._bids[0]:
                    self._bids[-1].append(observer)

    def UpdateObserversEx(self, UpdateDict):
        self._bids = 0, []
        result = self.__super.UpdateObserversEx(UpdateDict)
        if result and self._bids:
            for observer in self._bids[-1]:
                observer(self, **UpdateDict)
            result *= self._bids[-1] and 1 or 0
        self._bids = None
        return result
    
    def UpdateObserver(self, observer, UpdateDict):
        if observer: self._GetBid(observer, UpdateDict)

BidableSubjectMixin._BidableSubjectMixin__super = super(BidableSubjectMixin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BidableSubject(BidableSubjectMixin, Subject):
    pass

