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

class AttributedDict(dict):
    """AttributedDict is intended to be a handly little class that you can
    stuff attributes and such into like you would any other class, yet have
    the nice iteration capabilities of a dictionary."""
    
    __slots__ = [] # we really didnt want any attributes anyway

    def __getattribute__(self, name):
        """Allows access to "attributes" by either obj.name, or obj[name]"""
        try:
            return dict.__getattribute__(self, name)
        except AttributeError:
            if name in self:
                return self[name]
            else: raise

    def __setattr__(self, name, value):
        """Allows setting "attributes" by obj.name = value, or obj[name] = value"""
        try:
            dict.__setattr__(self, name, value)
        except AttributeError:
            self[name] = value

    def __delattr__(self, name):
        """Allows deleteing of "attributes" by del obj.name  or del obj[name]"""
        try:
            dict.__delattr__(self, name)
        except AttributeError:
            if name in self:
                del self[name]
            else: raise

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    class _test(AttributedDict): 
        answer = 42

    d = _test()

    # Test write
    d.test = 'working'

    # Test read
    assert 'working' == d.test
    assert 42 == d.answer
    assert 'answer' not in d

    # Test delete
    del d.test
    assert not hasattr(d, 'test')

    try:
        # Test reading the now deleted attribute
        d.test == 'this shouldnt really work'
        assert 0
    except AttributeError:
        pass

    try:
        # Test deleting an attribute that wasnt there in the first place...
        del d.ThiSneverExisted
        assert 0
    except AttributeError:
        pass

    import time
    class Normal(object):
        answer = 42**2
    normal = Normal()
    count = 1e4
    start = time.clock()
    for i in xrange(count): me = i + normal.answer
    pereach = (time.clock() - start) / count
    print "Normal:", pereach, "per", count

    start = time.clock()
    for i in xrange(count): me = i + d.answer
    pereach2 = (time.clock() - start) / count
    print "Attributed Dict:", pereach2, "per", count

    print "Attributed Dict is", pereach2/pereach, "times slower" 
