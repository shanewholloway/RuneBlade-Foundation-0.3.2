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

from Foundation.WeakBind import BoundCallable, BindCallable
import JID

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _MatchBase(object):
    Negate = 0
    def __call__(self, value):
        if self.Negate:
            return not self.MatchValue(value)
        else: return self.MatchValue(value)

class MatchAnd(list, _MatchBase):
    def MatchValue(self, value):
        for each in self:
            if not each(value): return 0
        else: return len(self) and 1 or 0
MatchAll = MatchAnd
    
class MatchOr(list, _MatchBase):
    def MatchValue(self, value):
        for each in self:
            if each(value): return 1
        else: return 0
MatchOne = MatchOr

class MatchNone(list, _MatchBase):
    def MatchValue(self, value):
        for each in self:
            if each(value): return 0
        else: return 1
    
class MatchAttributesRE(_MatchBase):
    def __init__(self, **attributes):
        import re
        self._MatchInfo = {}
        for key, value in attributes.iteritems():
            self._MatchInfo[key] = re.compile(value).match

    def MatchValue(self, value):
        for key, match in self._MatchInfo.iteritems():
            value = getattr(value, key, None)
            if value is None: 
                return 0
            elif not match(value):
                return 0
        else: return 1

class MatchAttributes(_MatchBase):
    def __init__(self, **attributes):
        self._MatchInfo = attributes

    def MatchValue(self, value):
        for key, compareto in self._MatchInfo.iteritems():
            if isinstance(compareto, JID.JID):
                if getattr(value, key, None) not in compareto:
                    return 0
            elif compareto != getattr(value, key, None):
                return 0
        else: return 1

class MatchHasAttribute(_MatchBase):
    def __init__(self, name):
        self._MatchInfo = name
        
    def MatchValue(self, value):
        return hasattr(value, self._MatchInfo)

class MatchHasNode(_MatchBase):
    def __init__(self, namespace, node):
        self._MatchInfo = (namespace, node)
        
    def MatchValue(self, value):
        for each in value._elements:
            if each[0] == self._MatchInfo: return 1
        else: return 0

class MatchHasChildNode(_MatchBase):
    def __init__(self, node):
        self._MatchInfo = node
        
    def MatchValue(self, value):
        for each in value._elements:
            if each[0][-1] == self._MatchInfo: return 1
        else: return 0

class MatchHasChildNamespace(_MatchBase):
    def __init__(self, namespace):
        self._MatchInfo = namespace
        
    def MatchValue(self, value):
        for each in value._elements:
            if each[0][0] == self._MatchInfo: return 1
        else: return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JabberObserver(BoundCallable):
    _debug = 0
    def __init__(self, callback=None, Match=None, BidValue=1):
        super(JabberObserver, self).__init__(callback)
        self.BidValue = BidValue
        self.Match = Match or MatchAnd()

    def AddRule(self, rule, Negate=0):
        rule.Negate = Negate
        self.Match.append(rule)

    def Bid(self, subject, **UpdateDict):
        for value in UpdateDict.itervalues():
            if self.Match(value):
                return self.BidValue
            elif self._debug:
                print "!!! No Match !!!"
                for each in self.Match:
                    print each(value), '==', each.__class__.__name__


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_():
    from Foundation.XMLObjectify import Objectify
    from Foundation.SubjectObserver.BidableSubject import BidableSubject
    def TestTrue(subject, obj): assert obj.__namespace__ == 'testing' and (obj.__node__ == 'tag' or (obj.myattr.find('haps') >= 0))
    def TestFalse(subject, obj): assert 0
    obj = Objectify('''<test xmlns='testing' myattr='perhaps'><tag attr='1' /> <tag /></test>''')
    subject = BidableSubject()
    observer = JabberObserver(TestTrue, MatchHasNode('testing', 'tag'))
    subject.AddObserver(observer)
    observer = JabberObserver(TestFalse, MatchHasNode('testing', 'tango'))
    subject.AddObserver(observer)
    observer = JabberObserver(TestTrue, MatchAttributes(myattr = '.*haps.*'))
    subject.AddObserver(observer)
    observer = JabberObserver(TestTrue)
    observer.Match.append(MatchHasNode('testing', 'tag'))
    observer.Match.append(MatchAttributes(myattr='.*haps.*'))
    subject.AddObserver(observer)

    subject.UpdateObservers(obj=obj)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    _Test_() 
    print "Test complete."


