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
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ChainedDict(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    chained = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetChained(self, chained):
        self.chained = chained or {}
        
    def GetChained(self):
        return self.chained

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Dictonary Compatability
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, data=None, chained=None):
        self.source = data or {}
        self.chained = chained or {}

    def __contains__(self, obj): 
        return self.source.__contains__(obj) or self.chained.__contains__(obj)
    
    def __getitem__(self, key):
        if key in self.source:
            return self.source[key]
        else: return self.chained[key]

    def __setitem__(self, *args, **kw): 
        return self.source.__setitem__(*args, **kw)

    def __delitem__(self, name):
        if self.source.__contains__(name):
            return self.source.__delitem__(name)

    def copy(self): 
        result = self.source.copy()
        result.update(self.chained)
        return result

    def get(self, key, *args): 
        if key in self.source:
            return self.source[key]
        else: return self.chained.get(key, *args)

    def clear(self, *args, **kw): 
        return self.source.clear(*args, **kw)
    
    def update(self, *args, **kw): 
        return self.source.update(*args, **kw)

    def has_key(self, *args, **kw): 
        return self.source.has_key(*args, **kw) or self.chained.has_key(*args, **kw)

    def setdefault(self, name, default):
        if name not in self:
            return self.source.setdefault(name, default)
        else: return self.get(name)

    def __not_contains(self, obj):
        return not self.source.__contains__(obj)

    def keys(self, include_chained=0): 
        if include_chained:
            chainedkeys = filter(self.__not_contains, self.chained)
            return self.source.keys() + chainedkeys
        else: return self.source.keys()

    def values(self, include_chained=0): 
        if include_chained:
            chainedkeys = filter(self.__not_contains, self.chained)
            chainedvalues = map(self.chained.get, chainedkeys)
            return self.source.values() + chainedvalues 
        else: return self.source.values()

    def items(self, include_chained=0): 
        if include_chained:
            chainedkeys = filter(self.__not_contains, self.chained)
            chainedvalues = map(self.chained.get, chainedkeys)
            return self.source.items() + zip(chainedkeys, chainedvalues)
        else: return self.source.items()

    def iterkeys(self, include_chained=0): 
        if include_chained:
            return iter(self.keys())
        else: return self.source.iterkeys()

    def itervalues(self, include_chained=0): 
        if include_chained:
            return iter(self.values())
        else: return self.source.itervalues()

    def iteritems(self, include_chained=0): 
        if include_chained:
            return iter(self.items())
        else: return self.source.iteritems()

    def __iter__(self): 
        return self.iterkeys()

    def __hash__(self):
        return self.source.__hash__()

    ## Incorrectly (?) implemented methods from inheritence
    #def __str__(self): 
    #def __repr__(self): 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print 

    cd = ChainedDict({'testing': 1})
    cd.SetChained({'testing': 21, 'chained': 42})

    print cd
    print cd.source
    print cd.chained
    print

    print cd.items()
    print cd.items(include_chained=1)
    print
    assert cd['testing'] == 1
    assert cd['chained'] == 42
    del cd['testing']
    assert cd['testing'] == 21
    cd['testing'] = 37

    print cd.items(include_chained=1)
    print cd.items()
    print

    assert cd['testing'] == 37
    assert cd.get('testing', None) == 37
    del cd['testing']
    assert cd['testing'] == 21

    assert 'testing' in cd
    assert 'chained' in cd
    assert 'not_there' not in cd

    assert cd.get('testing', None) == 21
    assert cd.get('chained', None) == 42

    print cd.items()
    print cd.items(include_chained=1)
    print
