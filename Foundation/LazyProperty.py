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

class LazyProperty(object):
    def __init__(self, name, LazyClass, *args, **kw):
        self.__name__ = name
        self._lazy_name = '_lazy_' + name
        if 'doc' in kw:
            self.__doc__ = kw['doc']
            del kw['doc']
        self.LazyFactory = LazyClass, args, kw

    def __get__(self, obj, klass):
        if obj: 
            result = getattr(obj, self._lazy_name, None)
            if result is None:
                result = apply(*self.LazyFactory)
                setattr(obj, self._lazy_name, result)
            return result
        else: return self

    def __set__(self, obj, value):
        setattr(obj, self._lazy_name, value)

    def __delete__(self, obj):
        delattr(obj, self._lazy_name)

