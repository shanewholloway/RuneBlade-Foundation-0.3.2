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

"""Returns attribute value from self if exists, or from an aquirable object.

Allows for dynamic pseudo inheritence from 'acquirable' objects.
Use sparingly, as the acquisition (both spanish and otherwise ;) is an expesive
propsition.  Works great for a subject/observer proxy, where you want notifications
when values are changed.

TODO: Look at doing this with metaclasses ala Aspect Oriented Programming?
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AcquisitionHooks(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getattribute__(self, name):
        """Returns attribute value from self if exists, or from an aquirable object."""
        try:
            return super(AcquisitionHooks, self).__getattribute__(name)
        except AttributeError:
            success, result = self._GetAcquirableAttr(name)
            if success: return result
            raise

    def __setattr__(self, name, value):
        """Sets attribute to value on self if exists, or on an aquirable object."""
        try:
            super(AcquisitionHooks, self).__getattribute__(name)
        except AttributeError:
            success, result = self._SetAcquirableAttr(name, value)
            if success: return result
        return super(AcquisitionHooks, self).__setattr__(name,value)

    def __delattr__(self, name):
        """Removes attribute from self if exists, or from an aquirable object."""
        try:
            super(AcquisitionHooks, self).__getattribute__(name)
        except AttributeError:
            success, result = self._DelAcquirableAttr(name, value)
            if success: return result
        return super(AcquisitionHooks, self).__delattr__(name)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SingleAcquisitionMixin(AcquisitionHooks):
    """Allows for dynamic pseudo inheritence from a list of 'acquirable' objects."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    __AcquirableObject = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetAcquirable(self, obj):
        """Adds obj to the acquisition list, allowing for pseudo inheritance."""
        self.__AcquirableObject = obj

    def RemoveAcquirable(self, obj):
        """Removes obj from the acquisition list."""
        self.SetAcquirable(None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetAcquirableAttr(self, name):
        result = getattr(self.__AcquirableObject, name, id(None))
        if result != id(None): 
            return 1, result
        else: return 0, None

    def _SetAcquirableAttr(self, name, value):
        if hasattr(self.__AcquirableObject, name):
            return 1, setattr(self.__AcquirableObject, name, value)
        else: return 0, None
        
    def _DelAcquirableAttr(self, name):
        if hasattr(self.__AcquirableObject, name):
            return 1, delattr(self.__AcquirableObject, name)
        else: return 0, None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AcquisitionMixin(AcquisitionHooks):
    """Allows for dynamic pseudo inheritence from a list of 'acquirable' objects."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    __AcquirableObjects = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def AddAcquirable(self, obj):
        """Adds obj to the acquisition list, allowing for pseudo inheritance."""
        if not self.__AcquirableObjects:
            self.__AcquirableObjects = []
        self.__AcquirableObjects.append(obj)

    def RemoveAcquirable(self, obj):
        """Removes obj from the acquisition list."""
        self.__AcquirableObjects.remove(obj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetAcquirableAttr(self, name):
        for x in self.__AcquirableObjects:
            result = getattr(x, name, id(None))
            if result != id(None): 
                return 1, result
        return 0, None

    def _SetAcquirableAttr(self, name, value):
        for x in self.__AcquirableObjects:
            if hasattr(x, name):
                return 1, setattr(x, name, value)
        return 0, None
        
    def _DelAcquirableAttr(self, name):
        for x in self.__AcquirableObjects:
            if hasattr(x, name):
                return 1, delattr(x, name)
        return 0, None


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    a = AcquisitionMixin()
    class temp(object):
        v = 1
        u = 2
    a.AddAcquirable(temp())

    if 1:
        assert a.v == 1
        assert a.u == 2
        assert a.u != a.v
        a.u = 'new value'
        assert a.u == 'new value'
        a.new_val = 'a new value!'
        assert a.new_val == 'a new value!'

        import time
        count = 1e4
        start = time.clock()
        for i in xrange(count): me = i + temp.v
        pereach = (time.clock() - start) / count
        print "Normal:", pereach, "per", count

        start = time.clock()
        for i in xrange(count): me = i + a.v
        pereach2 = (time.clock() - start) / count
        print "Acquisition:", pereach2, "per", count

        print "Acquisition is", pereach2/pereach, "times slower" 
    print "Test complete."


