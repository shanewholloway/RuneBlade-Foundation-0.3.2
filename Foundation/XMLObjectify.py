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

"""Builds a Python object tree from an XML stream.

Functions:

    Objectify
    ObjectifyFile

Classes:

    ObjectifiedXML
    Objectifier

Example:

    from Foundation.XMLObjectify import Objectify
    
    obj = Objectify('''<stream:stream xmlns:stream="Test Stream Namespace">
            <comment>Some generic xml</comment>
            <comment author="Shane Holloway">Fun with xml!</comment>
        </stream:stream>''')

    # iteration
    for each in obj.comment:
        print 'Author: %-20s' % getattr(each, 'author', '?unknown?'),
        print each()

    # direct access
    print obj.comment[1].author

History:

    XMLObjectify found its conceptual roots in similar tool created by David Mertz <mertz@gnosis.cx>
    named objectify.py, which is still extremely useful and can still be found at http://gnosis.cx .  
    Futher history of his module can be found there.  Now I say conceptual roots can be found there, 
    because the present state of XMLObjectify represents a 2nd rewrite code, maintaining only the 
    founding ideas, in order to serve new requirements.  

    One new requirement is the ability to "build" a python object tree by instantiating python classes
    from modules found on disk, and subsequently raising an exception if a suitable module is not found.
    (Raising that exception is one of the essential reasons for the 2nd rewrite, as I did not factor it
    in the 1st.)  This requirement provides the Foundation of the Skinning framework found in the 
    RuneBlade distribution, as well as XMLClassBuilder module.

    A second requirement was "the need for speed".  In both Mertz's objectify code and my first rewrite,
    a python object tree can take quite a while to build.  (2.2 seconds for 31 k skin file.)  This, 
    in part is due to the DOM model provided with python, and partly to creating new python classes
    on the fly.  This second rewrite notes that fact, and uses a prebuilt class (ObjectifiedXML) with
    different data elements to avoid having to create new classes at run time.  This requirement is the 
    corner stone of the RuneBlade Jabber package's XML socket stream.

    However, note that the first and second requirements are pretty much in direct opposition, as 
    dynamic imports will always be slower than using a predefined class that is already in scope.  
    A conflict such as this points us in the direction of refactoring the functionality, allowing 
    for either speedy building of python object trees, or the great flexability of dynamically building
    that object tree from modules on disk.  Hence, a new (pseudo) hierarchy is formed for this:
        
        + XMLBuilder (Abstract)
        |
        +-- XMLObjectify
        |
        +-+ XMLClassBuilder
        | |
        | +-- Skinning.XMLSkinner
        |
        +-- Jabber.Base
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Foundation import XMLBuilder
from xml.sax.saxutils import escape, quoteattr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Classes                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseObjectifiedXML(XMLBuilder.XMLBuilderObjectBase):
    """Represents an objectified XML node and its attributes with links to subnodes and contained PCData.

    Example:
    
        from Foundation.XMLObjectify import Objectify
        
        obj = Objectify('''<stream:stream xmlns:stream="Test Stream Namespace">
                <comment>Some generic xml</comment>
                <comment author="Shane Holloway">
                    Fun with xml!
                    Lots of fun!
                </comment>
            </stream:stream>''')

        assert isinstance(obj, ObjectifiedXML)

        # Element Access (note: there are two comments in the example XML
        assert isinstance(obj.comment, list)
        assert isinstance(obj.comment[1], ObjectifiedXML)

        # PCData Access
        assert isinstance(obj.comment[0](''), str)
        assert isinstance(obj.comment[0](None), list)

        # Attribute Access
        assert isinstance(obj.comment[1].author, str)
        
        # Create new element
        obj._addNewElement(None, 'comment', author='William')
        assert obj.comment[2].author == 'William'

        # Create new data
        obj.comment[2]._addData("Some new data")

        # Modify / create new attribute
        obj.fun = "with XML!"

        # Remove an attribute
        del obj.fun

        # Remove PCData
        obj.comment[1]._removeElement(obj.comment[1](None)[-1])

        # Remove All PCData
        obj.comment[0]._clearData()

        # Remove an element
        obj._removeElement(obj.comment[0])

        # Remove multiple elements
        del obj.comments
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc.                      
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _default_attributes = {}
    _attributes_casts = {}
 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special                                           
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, owner, parent, node, attributes, namespacemap):
        self.__namespace__, self.__node__ =  node
        self.__namespace_map__ = namespacemap
        self._attributes = self._default_attributes.copy()
        self._attributes.update(attributes)

        for key, cast in self._attributes_casts.iteritems():
            try: self._attributes[key] = cast(self._attributes[key])
            except KeyError: pass
            except ValueError: pass
 
        self._elements = []

    def __call__(self, joinstr=''):
        """One way to get the PC data out of the node.  See __str__, __int__, __float__, and __complex__.
        The joinstr argument adjusts how the different lines of PCData are joined, and passing None will 
        signal that the list should not be joined"""
        return self._getData(joinstr)
    
    def __str__(self):
        """Returns the PCData of the node in str format"""
        return self._getData('')
    
    def __int__(self): 
        """Returns the PCData of the node in int format.  Be prepared to catch exceptions in the face of incorrect data.  (Or incorrect assumptions ;) )"""
        return int(self._getData(''))

    def __long__(self): 
        """Returns the PCData of the node in long format.  Be prepared to catch exceptions in the face of incorrect data.  (Or incorrect assumptions ;) )
        Warning:  I think long type is being phased out?  Not quite sure."""
        return long(self._getData('')) 

    def __float__(self): 
        """Returns the PCData of the node in float format.  Be prepared to catch exceptions in the face of incorrect data.  (Or incorrect assumptions ;) )"""
        return float(self._getData('')) 

    def __complex__(self): 
        """Returns the PCData of the node in complex format.  Be prepared to catch exceptions in the face of incorrect data.  (Or incorrect assumptions ;) )"""
        return complex(self._getData('')) 

    def __repr__(self):
        """A slightly different repr"""
        result = XMLBuilder.XMLBuilderObjectBase.__repr__(self)
        return '<%s %r %r>' % (result[1:-1], self.__namespace__, self.__node__)
        
    def __cmp__(self, other):
        """Compare two objects.  If other object is objectified, compare simplest elements first"""
        if isinstance(other, ObjectifiedXML):
            result = cmp(self.__namespace__, other.__namespace__)
            if result: return result
            result = cmp(self.__node__, other.__node__)
            if result: return result
            result = cmp(self._attributes, other._attributes)
            if result: return result
            result = cmp(self._elements, other._elements)
            return result
        else:
            return cmp(other.__class__(self._getData('')), other)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getAllElements(self, andData=0):
        """Returns all elements."""
        if andData: return [x[-1] for x in self._elements]
        else: return [x[-1] for x in self._elements if x[0][-1]]

    def _getElements(self, namespace=None, node=None, andData=0):
        """Returns all elements matching node."""
        lst = self._elements
        if not andData: 
            lst = [x for x in lst if x[0][-1]]
        if node is not None:
            lst = [x for x in lst if x[0][-1] == node]
        if namespace is not None:
            lst = [x for x in lst if x[0][0] == namespace]
        return [x[-1] for x in lst]
    
    def _delAllElements(self, andData=0):
        """Removes all elements, and if andData, all PCData as well."""
        if andData: elements = []
        else: elements = [x for x in self._elements if x[0][-1] == '']

    def _delElements(self, namespace=None, node=None):
        """Removes all elements matching node."""
        lst = self._elements
        if node is not None:
            lst = [x for x in lst if x[0][-1] != node]
        if namespace is not None:
            lst = [x for x in lst if x[0][0] != namespace]
        if len(lst) != len(self._elements):
            self._elements = lst
            return 1
        return 0

    def _addElement(self, node, obj):
        """Adds a subnode obj, that is in namespace, and has name node.  Obj is not necessarily an ObjectifiedXML class, but is required to implement _toXML."""
        self._elements.append((node, obj))
        return self._elements[-1]

    def _addObjectifiedElement(self, obj):
        """Same as _addElement, but assumes object has attributes __namespace__ and __node__.  A little more convenient for adding subnodes in code."""
        return self._addElement((obj.__namespace__, obj.__node__), obj)

    def _addNewElement(self, namespace, node, **attributes):
        """Creates and adds a new element in namespace, with name node, having attributes as given.  Uses self.__class__ for creating the element instance."""
        namespace = namespace or self.__namespace__
        namespacemap = XMLBuilder.ChainedDict({}, self.__namespace_map__)
        return self._addElement((namespace, node), self.__class__(self, self, (namespace, node), attributes, namespacemap))
        
    def _removeElement(self, element):
        """Removes a subnode element based on != relationship.  (Note: Can be a PCData element)"""
        elements = [x[-1] for x in self._elements if x[-1] != element]
        delta = len(self._elements) - len(elements)
        if delta: self._elements = elements
        return delta

    def _clearData(self):
        """Removes all PCData from the element node."""
        return self._delElements(node='')

    __addDataHadNewLine = 1
    def _addData(self, data):
        """Adds PCData to the element node."""
        HadNewline, self.__addDataHadNewLine = self.__addDataHadNewLine, data and data[-1] in '\n\r'
        if not HadNewline and self._elements and self._elements[-1][0][-1] == '':
            data = self._elements.pop()[1] + data
        self._elements.append((('', ''), data))

    def _setData(self, data):
        """Clears PCData, then appends new PCData to the element node."""
        self._clearData()
        self._addData(data)

    def _getData(self, joinstr=''):
        result = [x[-1] for x in self._elements if not x[0][-1]]
        if joinstr is not None:
            return joinstr.join(result)
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _toXML(self, strSplit='', nsOuter={}, bHeaderOnly=0):
        """Converts the python object back into XML.  
        
            - If strSplit is None, the result is a nested list structure; otherwise, strSplit is used to join those lists into a string.  
                (default is '')
            
            - If nsOuter matches node.__namespace__, the namespace will not be included in the XML again.  
                (default is '')

            - If bHeaderOnly is true, then only node, namespace, and attributes are included in the XML.  If bHeaderOnly is greater than 1,
                the header tag will also be closed.  If bHeader is false, then the child elements are included.
                (default is 0)
        """
        if isinstance(nsOuter, str): nsOuter = {nsOuter: None}
        elif nsOuter is None: nsOuter = {self.__namespace__: None}
        if self.__namespace_map__:
            nsOuter = nsOuter.copy()
            nsOuter.update(self.__namespace_map__)

        if self.__namespace__ in nsOuter:
            nodePrefix = nsOuter[self.__namespace__]
        else:
            # Remove old default namespace
            nodePrefix = None
            for key, value in nsOuter.iteritems():
                if value is nodePrefix: del nsOuter[key]
            for key, value in self.__namespace_map__.iteritems():
                if value is nodePrefix: del self.__namespace_map__[key]
            # Add current namespace as "default"
            if self.__namespace__:
                nsOuter[self.__namespace__] = nodePrefix
                self.__namespace_map__[self.__namespace__] = nodePrefix

        # Node start
        if nodePrefix:
            nodename = '%s:%s' % (nodePrefix, self.__node__)
        else: nodename = self.__node__
        result = '<%s' % nodename

        # Namespaces
        for uri, prefix in self.__namespace_map__.iteritems():
            if prefix:
                result += ' xmlns:%s=%s' % (prefix, quoteattr(uri))
            else: 
                result += ' xmlns=%s' % (quoteattr(uri))

        # Attributes
        for attrname, attrvalue in self._attributes.iteritems():
            if isinstance(attrname, tuple):
                if attrname[1] not in self._attributes:
                    prefix = nsOuter[attrname[0]]
                    if prefix: result += ' %s:%s=%s' % (prefix, attrname[1], quoteattr(attrvalue))
                    else: result += ' %s=%s' % (attrname[1], quoteattr(attrvalue))
                #else: will be handled in not extended name form
            elif nodePrefix: result += ' %s:%s=%s' % (nodePrefix, attrname[1], quoteattr(attrvalue))
            else: result += ' %s=%s' % (attrname, quoteattr(attrvalue))

        # Result constrution
        if bHeaderOnly: 
            if bHeaderOnly > 1:
                result += '/>'
            else: result += '>'
            result = [result]
        elif self._elements:
            result += '>'
            result = [result]
            result.append(self._childrenToXML(strSplit, nsOuter))
            result.append('</%s>' % nodename)
        else: 
            result += '/>'
            result = [result]
        if strSplit is not None:
            return strSplit.join(result)
        else: return result
    _toPrettyXML = _toXML

    def _childrenToXML(self, strSplit='', nsOuter={}):
        """Converts child python objects back into XML.
            - If strSplit is None, the result is a nested list structure; otherwise, strSplit is used to join those lists into a string.  
                (default is '')
            
            - If nsOuter matches subnode.__namespace__, the namespace will not be included in the XML again.  
                (default is '')
        """
        if isinstance(nsOuter, str): nsOuter = {nsOuter:None}
        elif nsOuter is None: nsOuter = {self.__namespace__: None}
        result = []
        for tupleNSNode, each in self._elements:
            if not tupleNSNode[-1]:
                result.append(escape(each))
            else:
                result.append(each._toXML(strSplit, nsOuter))

        result = filter(None, result)
        if strSplit is not None:
            return strSplit.join(result)
        else: return result
    _childrenToPrettyXML = _childrenToXML
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class AttributedObjectifiedXML(object):
    def __getattribute__(self, name):
        """Allows for the node.attribute or node.subnode semantics"""
        if '_' != name[0]:
            _attributes = self._attributes
            if name in _attributes: return _attributes[name]
            xmlName = name.replace('_', '-')
            if '-' == xmlName[-1]: xmlName = xmlName[:-1]
            if xmlName in _attributes:
                return _attributes[xmlName]
            result = self._getElements(node=xmlName) 
            if result:
                return result
        return XMLBuilder.XMLBuilderObjectBase.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """Allows user to create new attributes, or change values using node.attribute semantics"""
        if '_' != name[0:1]:
            if name in self._attributes: 
                self._attributes[name] = value
            else:
                xmlName = name.replace('_', '-')
                if '-' == xmlName[-1]: xmlName = xmlName[:-1]
                self._attributes[xmlName] = value
        else:
            return BaseObjectifiedXML.__setattr__(self, name, value)
        
    def __delattr__(self, name):
        """Allows for deletion of attributes or subnodes through node.attribute or node.subnode semantics"""
        if '_' != name[0:1]:
            if name in self._attributes: 
                del self._attributes[name]
                return

            xmlName = name.replace('_', '-')
            if '-' == xmlName[-1]: xmlName = xmlName[:-1]
            if xmlName in self._attributes:
                del self._attributes[xmlName]
                return
            else:
                if self._delElements(node=xmlName):
                    return

        BaseObjectifiedXML.__delattr__(self, name)
        return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ObjectifiedXML(BaseObjectifiedXML, AttributedObjectifiedXML):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Objectifier(XMLBuilder.XMLBuilder): 
    """An implementation of XMLBuilder that creates ObjectifiedXML nodes from an XML stream.
    See Objectify and ObjectifyFile for usage."""
    objectified_class = ObjectifiedXML
    Objectify = XMLBuilder.XMLBuilder.Parse
    ObjectifyFile = XMLBuilder.XMLBuilder.ParseFile

    def _GetElementFactory(self, owner, parent, node, attributes, namespacemap):
        """Signals that we always want to create self.objectified_class, which defaults to the ObjectifiedXML class."""
        return self.objectified_class

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Functional Definitions                            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Objectify(*args, **kw):
    """Simple access to Objectifier.Objectify or Objectifier.ParseFile.  
    Warning: Uses a shared object from _defaultObjectifier, and therefore is not threadsafe."""
    return Objectifier().Objectify(*args, **kw)

def ObjectifyFile(*args, **kw):
    """Simple access to Objectifier.ObjectifyFile or Objectifier.ParseFile.  
    Warning: Uses a shared object from _defaultObjectifier, and therefore is not threadsafe."""
    return Objectifier().ObjectifyFile(*args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_XMLObjectify():
    from pprint import pprint
    xmlfile = open('test_objectify.xml', 'r')
    obj = ObjectifyFile(xmlfile)
    print repr(obj)
    print ' ~ ' * 20
    print (obj._toXML())
    print ' ~ ' * 20
    print (obj.message[0]._toXML())

    print
    print ' ~ ' * 20
    print

    obj = Objectify('''<test xmlns='OuterNamespace'><inner data='1'>content is fun!</inner></test>''')
    print obj.inner[0]._toXML(nsOuter=None)

    print
    print ' ~ ' * 20
    print

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    builder = Objectifier()
    builder.objectified_class = BaseObjectifiedXML

    xmlfile = open('test_objectify.xml', 'r')
    obj = builder.ObjectifyFile(xmlfile)

    print repr(obj)
    print ' ~ ' * 20
    print (obj._toXML())
    print ' ~ ' * 20

    from Foundation.AspectOriented.Aspect import Aspect
    class MyAspect(Aspect, AttributedObjectifiedXML): pass
    MyAspect.InsertAspect(obj)
    print (obj.message[0]._toXML())

    print
    print ' ~ ' * 20
    print

    obj = builder.Objectify('''<test xmlns='OuterNamespace'><inner data='1'>content is fun!</inner></test>''')
    MyAspect.InsertAspect(obj)
    print obj.inner[0]._toXML(nsOuter=None)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    _Test_XMLObjectify() 
    print "Test complete."


