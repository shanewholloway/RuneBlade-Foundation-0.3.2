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

from Foundation import XMLBuilder 
from xml.sax.saxutils import escape, quoteattr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nsXMLSchema = 'http://www.w3.org/2001/XMLSchema'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLMetaInformation(XMLBuilder.XMLBuilderObjectBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, owner, parent, node, attributes, namespacemap): 
        self.__namespace__, self.__node__ = node
        self._attributes = attributes
        for each in self._attributes: self._attributes[each] = 1
        self._data = 0
        self._nodata = 1
        self._mincount = 1
        self._mergecount = 1
        self._elements = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _addElement(self, node, obj): 
        self._elements.setdefault(node, obj)._XSDMerge(obj)

    def _addData(self, data): 
        self._data = 1
        self._nodata = 0

    def _xmlInitStarted(self): 
        pass 

    def _xmlInitComplete(self): 
        pass 

    def _xmlChildFactory(self, owner, parent, node, attributes, namespacemap): 
        return self.__class__

    def _XSDMerge(self, other):
        if other is self: return
        assert self.__namespace__ == other.__namespace__
        assert self.__node__ == other.__node__

        self._mergecount += other._mergecount

        # Find out which attributes are common to both this element and the other, 
        # accounting for optional ones
        newattributes = {}
        for key in self._attributes:
            if key in other._attributes:
                newattributes[key] = min(self._attributes[key], other._attributes[key])
            else: newattributes[key] = 0
        for key in other._attributes:
            if key not in self._attributes:
                newattributes[key] = 0
        self._attributes = newattributes

        self._nodata = not self._data  or not other._data
        self._data = self._data or other._data
        self._mincount = min(self._mincount, other._mincount)

        for key in self._elements:
            if key not in other._elements:
                self._elements[key]._mincount = 0

        for key in other._elements:
            if key in self._elements:
                self._elements[key]._XSDMerge(other._elements[key])
            else:
                temp = other._elements[key]
                temp._mincount = 0
                self._elements[key] = temp

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Properties
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetElements(self): return self._elements
    elements = property(_GetElements)

    def _GetAttributes(self): return self._attributes
    attributes = property(_GetAttributes)

    def _GetElementRequired(self): return self._mincount
    requirednode = property(_GetElementRequired)

    def _GetDataFlag(self): return self._data
    dataflag = property(_GetDataFlag)

    def _GetNoDataFlag(self): return self._nodata
    nodataflag = property(_GetNoDataFlag)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XSDfromXML(XMLMetaInformation):
    def _toXSD(self, strSplit='', nsOuter=None, bHeaderOnly=0):
        result = []
        resultEnd = []

        if nsOuter is None:
            nsOuter = {nsXMLSchema:'xs'}
            result.append('<xs:schema xmlns:xs="%s">' % nsXMLSchema)
            resultEnd.append('</xs:schema>')
        elif nsXMLSchema not in nsOuter:
            nsOuter[nsXMLSchema] = 'xs'
            result.append('<xs:schema xmlns:xs="%s">' % nsXMLSchema)
            resultEnd.append('</xs:schema>')

        # Make the prefix for the nodes of the XSD
        prefix = nsOuter[nsXMLSchema] or ''
        if prefix: prefix += ':'

        # Create the root element
        result.append('<%selement name=%s namespace=%s' % (prefix, quoteattr(self.__node__), quoteattr(self.__namespace__ or '')))

        SimpleType = not self._attributes and not self._elements
        if SimpleType:
            if self._data:
                result[-1] += ' type="xs:string"'
            elif self._nodata:
                result[-1] += ' nillable="true"'
            result[-1] += '/>'
        elif bHeaderOnly:
            if bHeaderOnly > 1: result[-1] += '/>'
            else: result[-1] += '>'
        else:
            result[-1] += '>'
            resultEnd.append('</%selement>' % prefix)

            result.append('<%scomplexType' % prefix)
            if self._data or not self._nodata:
                result[-1] += ' mixed="true">'
            else: result[-1] += '>'
            resultEnd.append('</%scomplexType>' % prefix)

            # ~ Elements

            if self._elements:
                result.append('<%sall>' % prefix)
                for element in self._elements.itervalues():
                    result.append(element._toXSD(strSplit, nsOuter))
                result.append('</%sall>' % prefix)

            # ~ Attributes

            for attrname in self._attributes.iterkeys():
                if isinstance(attrname, tuple):
                    if attrname[1] not in self._attributes:
                        result.append('<%sattribute name=%s namespace=%s type="xs:string"/>' % (prefix, quoteattr(attrname[1]), quoteattr(attrname[0])))
                else:
                    result.append('<%sattribute name=%s type="xs:string"/>' % (prefix, quoteattr(attrname)))

        # Return the result of our labors
        resultEnd.reverse()
        if strSplit is not None:
            return strSplit.join(result + resultEnd)
        else: return result + resultEnd

    _toXML = _toXSD

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XSDConverter(XMLBuilder.XMLBuilder): 
    objectified_class = XSDfromXML
    Convert = XMLBuilder.XMLBuilder.Parse
    ConvertFile = XMLBuilder.XMLBuilder.ParseFile

    def _GetElementFactory(self, owner, parent, node, attributes, namespacemap):
        return self.objectified_class

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Functional Definitions                            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def ConvertXSD(*args, **kw):
    return XSDObjectifier().Convert(*args, **kw)

def ConvertXSDFile(*args, **kw):
    return XSDConverter().ConvertFile(*args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    xmlfile = open('test_objectify.xml', 'r')
    obj = ConvertXSDFile(xmlfile)
    print '<?xml version="1.0"?>'
    print obj._toXSD('\n')

