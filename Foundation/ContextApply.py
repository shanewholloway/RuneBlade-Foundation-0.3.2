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
from WeakBind import BindCallable, WeakBoundCallable, StrongBoundCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Tuple / Dictionary Join Functions for Smart Apply 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _JoinKW(dict1, dict2):
    """Join two dicts without modifying either."""
    result = dict2.copy()
    result.update(dict1)
    return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Default Smart Apply Class                         
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _StrongContextApply(StrongBoundCallable):
    """Base class for adding positional and keyword based "context" to BoundCallable objects"""

    def __init__(self, callback, *args, **kw):
        StrongBoundCallable.__init__(self, callback)
        self.SaveContext(args, kw)

    def SaveContext(self, args, kw):
        """Saves extra paramters to be passed to the BoundCallable object.  Creates the "context" part of ContextApply."""
        self.args = args
        self.kw = kw

class _WeakContextApply(WeakBoundCallable):
    """Base class for adding positional and keyword based "context" to BoundCallable objects"""

    def __init__(self, callback, *args, **kw):
        WeakBoundCallable.__init__(self, callback)
        self.SaveContext(args, kw)

    def SaveContext(self, args, kw):
        """Saves extra paramters to be passed to the BoundCallable object.  Creates the "context" part of ContextApply."""
        self.args = args
        self.kw = kw

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextApply_p_s_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Passed from calling code,
        - Saved context,
    """
    def __call__(self, *args, **kw):
        return self._DoCall(*(args + self.args), **_JoinKW(kw, self.kw))

class ContextApply_s_p_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Saved context,
        - Passed from calling code,
    """
    def __call__(self, *args, **kw):
        return self._DoCall(*(self.args + args), **_JoinKW(self.kw, kw))

class ContextApply_p_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Passed from calling code,

    Note: This is the same as calling the BoundCallable directly, but appears here for completeness.
    """
    def SaveContext(self, args, kw): pass
    def __call__(self, *args, **kw):
        return self._DoCall(*args, **kw)

class ContextApply_s_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Saved context,

    Note: The parameters from the calling code will be completely ignored.
    """
    def __call__(self, *args, **kw):
        return self._DoCall(*self.args, **self.kw)

class ContextApply_0_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - args will be an empty tuple,
        - kw will be an empty dict,

    Note: The parameters from both the calling code and the "context" will be completely ignored.
    """
    def SaveContext(self, args, kw): pass
    def __call__(self, *args, **kw):
        return self._DoCall()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StrongContextApply_p_s(ContextApply_p_s_mixin, _StrongContextApply): pass
class StrongContextApply_s_p(ContextApply_s_p_mixin, _StrongContextApply): pass
class StrongContextApply_p(ContextApply_p_mixin, _StrongContextApply): pass
class StrongContextApply_s(ContextApply_s_mixin, _StrongContextApply): pass
class StrongContextApply_0(ContextApply_0_mixin, _StrongContextApply): pass

class WeakContextApply_p_s(ContextApply_p_s_mixin, _WeakContextApply): pass
class WeakContextApply_s_p(ContextApply_s_p_mixin, _WeakContextApply): pass
class WeakContextApply_p(ContextApply_p_mixin, _WeakContextApply): pass
class WeakContextApply_s(ContextApply_s_mixin, _WeakContextApply): pass
class WeakContextApply_0(ContextApply_0_mixin, _WeakContextApply): pass

ContextApply_p_s = StrongContextApply_p_s 
ContextApply_s_p = StrongContextApply_s_p 
ContextApply_p = StrongContextApply_p 
ContextApply_s = StrongContextApply_s 
ContextApply_0 = StrongContextApply_0 

WeakContextApply = WeakContextApply_p_s
StrongContextApply = StrongContextApply_p_s
ContextApply = StrongContextApply_p_s

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultipleApply(list):
    """Allows a list of callable objects to appear as a single callable object, returning the idx result.
    If idx is None, will return a list of all the results.
    
    Note: Implementation of the composite pattern.
    """
    def __init__(self, idx=-1, *args, **kw):
        list.__init__(self, *args, **kw)
        self.idx = idx

    def __call__(self, *args, **kw):
        if self.idx is None:
            return [method(*args, **kw) for method in self]
        else:
            ## There might be a faster way to do this using map?
            for method in self[:self.idx]:
                method(*args, **kw)

            result = self[self.idx](*args, **kw)

            # Normally you would think to just add one to idx,
            # But by splitting it twice, self.idx can be -1 as well
            ## There might be a faster way to do this using map?
            for method in self[self.idx:][1:]:
                method(*args, **kw)

            return result

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Test Section                                      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    from pprint import pprint

    def printit(*args, **kw):
        print "   args: ", 
        pprint(args)
        print "     kw: ", 
        pprint(kw)
        return args, kw

    def test(Class, callback=printit):
        print
        print "testing:", Class.__name__
        a_s = (1,2,3)
        a_p = (10,20,30)
        k_s = {'a':1,'b':2}
        k_p = {'b':20, 'c':30}
        cb = Class(callback, *a_s, **k_s)
        result = cb(*a_p, **k_p)
        print ' result:', `result`
        return result
    
    assert test(ContextApply_p_s) == ((10, 20, 30, 1, 2, 3), {'a': 1, 'c': 30, 'b': 20})
    assert test(ContextApply_s_p) == ((1, 2, 3, 10, 20, 30), {'a': 1, 'c': 30, 'b': 2})
    assert test(ContextApply_p) == ((10, 20, 30), {'c': 30, 'b': 20})
    assert test(ContextApply_s) == ((1, 2, 3), {'a': 1, 'b': 2})
    assert test(ContextApply_0) == (tuple(), {})

    print
    print "testing:", MultipleApply.__name__
    import operator
    multi = MultipleApply(None, [operator.add, operator.mul, operator.mod, printit])
    assert multi(3,4) == [7, 12, 3, ((3,4), {})]
    multi.idx = 2
    assert multi(3,4) == 3
    multi.idx = -1
    assert multi(3,4) == ((3,4), {})
    
