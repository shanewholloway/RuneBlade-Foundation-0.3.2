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

from __future__ import generators

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinContext(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, NextContext, Data={}):
        self._NextContext = NextContext
        self.__dict__.update(Data)

    def __getattribute__(self, name):
        if name in ('__dict__', '_NextContext'):
            return object.__getattribute__(self, name)
        elif name[0] != '_' or name in ('__root__', '__skinner__'):
            ctx = self
            while ctx and (name not in ctx.__dict__):
                ctx = ctx._NextContext
            if ctx: return ctx.__dict__[name]
        return object.__getattribute__(self, name)

    ## Redundant
    #def __setattr__(self, name, value):
    #    return object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name not in self.__dict__ and self._NextContext:
            return self._NextContext.__delattr__(name)
        else:
            return object.__delattr__(self, name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _update(self, Data):
        self.__dict__.update(Data)

    def _OwnerContext(self, name, returnLast=0):
        next = self
        while name not in next.__dict__:
            if not next._NextContext:
                if not returnLast:
                    next = next._NextContext
                break
            next = next._NextContext
        return next
    OwnerOf = _OwnerContext
        
    def _GetContext(self, *args, **kw):
        lst = [self]
        while lst[-1]: 
            lst.append(lst[-1]._NextContext)
        lst.pop()
        return lst.__getitem__(*args,**kw)
        
    def _RootContext(self):
        next = self
        while next._NextContext: next = next._NextContext
        return next
    RootContext = _RootContext
    
    def itercontext(self):
        next = self
        while next: 
            yield next
            next = next._NextContext


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    ctxA = SkinContext(None)
    ctxB = SkinContext(ctxA)
    ctxA.a = 'This is ctxA.a'
    ctxA.c = 'This is ctxA.c'
    ctxB.b = 'This is ctxB.b'
    ctxB.c = 'This is ctxB.c'

    print ctxA.a
    print ctxA.c

    print ctxB.a
    print ctxB.b
    print ctxB.c

    print "Test complete."

