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

"""Subject-based Foundation.AttributedDict

Similar to Foundation.AttributedDict, except that every modification causes an 
UpdateObservers call.

TODO: Look at doing this with metaclasses ala Aspect Oriented Programming?
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Subject import Subject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AttributedSubjectMixin(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        super(AttributedSubjectMixin, self).__init__(*args, **kw)
        self._attributes = {}

    def __getattribute__(self, name):
        if '_' != name[0]:
            result = self._attributes.get(name, self)
            if result is not self:
                return result
        return super(AttributedSubjectMixin, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if '_' != name[0]:
            self._attributes[name] = value
            self.UpdateObserversEx({name: value})
        else:
            return super(AttributedSubjectMixin, self).__setattr__(name, value)

    def __delattr__(self, name):
        if '_' != name[0]:
            if name in self._attributes:
                del self._attributes[name]
                self.UpdateObserversEx({name: None})
        else:
            return super(AttributedSubjectMixin, self).__delattr__(name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Dictonary Compatability
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __contains__(self, obj): 
        return self._attributes.__contains__(obj)

    def __iter__(self): 
        return self._attributes.__iter__()

    def __str__(self): 
        return self._attributes.__str__()

    def __repr__(self): 
        return self._attributes.__repr__()

    def __getitem__(self, *args, **kw): 
        return self._attributes.__getitem__(*args, **kw)

    def __setitem__(self, name, value): 
        result = self._attributes.__setitem__(name, value)
        self.UpdateObserversEx({name: value})
        return result

    def __delitem__(self, name):
        result = self._attributes.__delitem__(name)
        self.UpdateObserversEx({name: None})
        return result

    def __hash__(self):
        return  self._attributes.__hash__()

    def clear(self): 
        UpdateDict = dict(map(None, self._attributes.keys(), tuple()))
        result = self._attributes.clear()
        self.UpdateObserversEx(UpdateDict)
        return result

    def copy(self): 
        return self._attributes.copy()

    def get(self, *args, **kw): 
        return self._attributes.get(*args, **kw)

    def has_key(self, *args, **kw): 
        return self._attributes.has_key(*args, **kw)

    def popitem(self, *args, **kw): 
        result = self._attributes.popitem(*args, **kw)
        self.UpdateObserversEx({name:None})
        return result

    def setdefault(self, name, default):
        if name not in self._attributes:
            result = self._attributes.setdefault(name, default)
            self.UpdateObserversEx({name:default})
        else:
            result = self._attributes.get(name)
        return result

    def update(self, other): 
        result = self._attributes.update(other)
        self.UpdateObserversEx(other)
        return result

    def keys(self): 
        return self._attributes.keys()

    def values(self): 
        return self._attributes.values()

    def items(self): 
        return self._attributes.items()

    def iterkeys(self): 
        return self._attributes.iterkeys()

    def itervalues(self): 
        return self._attributes.itervalues()

    def iteritems(self): 
        return self._attributes.iteritems()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AttributedSubject(AttributedSubjectMixin, Subject): 
    """Couples AttributedSubjectMixin with a Subject propigation scheme."""
    def AddObserver(self, observer, call=0, **kw):
        Subject.AddObserver(self, observer, **kw)
        if call: observer(self, **self._attributes)

