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

from xml.parsers.expat import ParserCreate as _ParserCreate
from WeakBind import BindCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LazyExpatXMLParser(object):
    """Use Expat parser to parse string/file data, but create the
    parser as late as possible."""
    def __init__(self, encoding='ASCII', seperator=' '):
        self._encoding = encoding
        self._seperator = seperator

    def Parse(self, *args, **kw):
        # Ok, use the standard expat parser...
        parser = _ParserCreate(self._encoding, self._seperator)
        parser.returns_unicode = self._encoding != 'ASCII' and 1 or 0
        parser.StartElementHandler = BindCallable(self.StartElementHandler)
        parser.EndElementHandler = BindCallable(self.EndElementHandler)
        parser.CharacterDataHandler = BindCallable(self.CharacterDataHandler)
        parser.StartNamespaceDeclHandler = BindCallable(self.StartNamespaceDeclHandler)
        parser.EndNamespaceDeclHandler = BindCallable(self.EndNamespaceDeclHandler)
        return parser.Parse(*args, **kw)

    def ParseFile(self, *args, **kw):
        # Ok, use the standard expat parser...
        parser = _ParserCreate(self._encoding, self._seperator)
        parser.returns_unicode = self._encoding != 'ASCII' and 1 or 0
        parser.StartElementHandler = BindCallable(self.StartElementHandler)
        parser.EndElementHandler = BindCallable(self.EndElementHandler)
        parser.CharacterDataHandler = BindCallable(self.CharacterDataHandler)
        parser.StartNamespaceDeclHandler = BindCallable(self.StartNamespaceDeclHandler)
        parser.EndNamespaceDeclHandler = BindCallable(self.EndNamespaceDeclHandler)
        return parser.ParseFile(*args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ObjectifiedXMLParser(LazyExpatXMLParser):
    """Mimics the events of the Expat parser with an Objectifed XML
    object as the source data.  Builds on LazyExpatXMLParser in case
    the passed in data is in string form."""
    def Parse(self, obj, *args, **kw):
        if not isinstance(obj, str): 
            # Here's the magic... reuse the already objectified XML
            for uri, prefix in obj.__namespace_map__.iteritems():
                self.StartNamespaceDeclHandler(prefix, uri)
            name = self._seperator.join([obj.__namespace__, obj.__node__])
            self.StartElementHandler(name, obj._attributes)
            for each in obj._elements:
                if each[0][-1]: self.Parse(each[-1])
                else: self.CharacterDataHandler(each[-1])
            result = self.EndElementHandler(name)
            for prefix in obj.__namespace_map__.itervalues():
                self.EndNamespaceDeclHandler(prefix, uri)
            return result
        else:
            return super(ObjectifiedXMLParser, self).Parse(obj, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_XMLObjectify():
    from XMLObjectify import Objectifier
    xmlfile = open('test_objectify.xml', 'r')
    maker = Objectifier()
    maker.SetParserFactory(ObjectifiedXMLParser)

    objFile = maker.ObjectifyFile(xmlfile)
    xmlfile.seek(0)
    objString = maker.Objectify(xmlfile.read())

    assert objFile == objString 

    objObjecitfied1 = maker.Objectify(objFile)
    objObjecitfied2 = maker.Objectify(objString)
    objObjecitfied3 = maker.Objectify(objObjecitfied1)
    objObjecitfied4 = maker.Objectify(objObjecitfied2)

    assert objFile == objObjecitfied1
    assert objString == objObjecitfied1
    assert objFile == objObjecitfied2
    assert objString == objObjecitfied2
    assert objFile == objObjecitfied3
    assert objString == objObjecitfied3
    assert objFile == objObjecitfied4
    assert objString == objObjecitfied4

    assert objObjecitfied1 == objObjecitfied2
    assert objObjecitfied1 == objObjecitfied3
    assert objObjecitfied1 == objObjecitfied4
    assert objObjecitfied2 == objObjecitfied3
    assert objObjecitfied2 == objObjecitfied4
    assert objObjecitfied3 == objObjecitfied4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    _Test_XMLObjectify() 
    print "Test complete."

