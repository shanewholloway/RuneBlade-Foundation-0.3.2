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

"""ProxySubejcts draw out some commonalities of subjects observing
other subjects.  Based upon what they observer, the proxy subjects
may filter/modify/extrapolate further results, or simple pass on a 
subset of those results.

TODO: Look at doing this with metaclasses ala Aspect Oriented Programming?
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Foundation import Acquisition
import Subject
import CategorySubject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProxySubjectTriggerMixin(object):
    """This class makes it so that any setattr/delattr
    calls UpdateObservers on the associated subject."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _subject = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, subject=None):
        self.SetSubject(subject)

    def __setattr__(self, name, value):
        result = self.__super.__setattr__(name, value)
        if name != '_subject' and self._subject:
            self._subject.UpdateObserversEx({name: value})
        return result

    def __delattr__(self, name):
        result = self.__super.__delattr__(name)
        if name != '_subject' and self._subject:
            self._subject.UpdateObserversEx({name: None})
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetSubject(self, subject):
        self._subject = subject

ProxySubjectTriggerMixin._ProxySubjectTriggerMixin__super = super(ProxySubjectTriggerMixin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProxySubjectAcquisitionMixin(ProxySubjectTriggerMixin, Acquisition.AcquisitionMixin):
    """This class couples the methods of Acquisition with UpdateObserver calls on attribute sets or deletes."""
    def __init__(self, subject=None):
        ProxySubjectTriggerMixin.__init__(self, subject)
        Acquisition.AcquisitionMixin.__init__(self)

    def SetSubject(self, subject):
        if self._subject: self.RemoveAcquirable(self._subject)
        super(ProxySubjectAcquisitionMixin, self).SetSubject(subject)
        if self._subject: self.AddAcquirable(self._subject)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProxySubject(ProxySubjectAcquisitionMixin):
    """Binds ProxySubjectAcquisitionMixin to the Subject class by default"""
    def __init__(self, subject=None):
        ProxySubjectAcquisitionMixin.__init__(self, subject or Subject.Subject())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProxyCategorySubject(ProxySubjectAcquisitionMixin):
    """Binds ProxySubjectAcquisitionMixin to the CategorySubject class by default"""
    def __init__(self, subject=None):
        ProxySubjectAcquisitionMixin.__init__(self, subject or CategorySubject.CategorySubject())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    from Foundation.AttributedDict import AttributedDict
    ad = AttributedDict({'a':1,'b':2})

    test = ProxySubject()
    test.AddAcquirable(ad)

    def TestObserver(subject, **kw):
        print subject, kw

    test.AddObserver(TestObserver)

    test.UpdateObservers(testing='yep')

    print test.a
    assert test.a is ad.a

    print test.b
    assert test.b is ad.b

    test.a = test.a * 3
    print test.a
    assert test.a is ad.a

    print "Test complete."

