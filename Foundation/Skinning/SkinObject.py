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
from Foundation.Utilities import *
from InheritableSettings import InheritSettingsMixin
import SkinContext
import weakref

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinObject(XMLBuilder.XMLBuilderObjectBase, InheritSettingsMixin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = InheritSettingsMixin.default_settings.copy()
    default_settings.update({
        'contextvar':'',
        'contextnode':'',
        'parentvar':'',
        'parentnode':'',
        'unravelstop':'0',
        'unravelnode':'0',
        'unravel':'0',
        })

    globalnamespace = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, builder, parent, node, settings, namespacemap):
        self.children = []
        self.object = None
        self._InitParent(parent)
        self._InitContext(builder, parent)
        self._InitSettings(settings)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Init Protected Methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _InitParent(self, parent):
        if parent: self.parent = weakref.ref(parent)
        else: self.parent = lambda: None

    def _InitContext(self, builder, parent):
        if parent: self.context = parent.context
        else: self.context = builder.context

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        # self.PushContext() # Call this if you are going to add to the context tree
        pass

    def SkinFinalize(self):
        pass

    def PushContext(self, force=0):
        """Adds a context to the stack, if needed or forced.
        Returns the resultant context."""
        result = self.context
        if force or (self.parent() and self.parent().context is self.context):
            self.context = SkinContext.SkinContext(self.context)
        return result

    def PopContext(self, force=0):
        """Removes a context from the stack if owned or forced.
        Returns the resultant context."""
        result = self.context
        if force or self.context._NextContext:
            self.context = self.context._NextContext
        return result
        
    def Content(self):
        return [child[1] for child in self.children if child[0] == '']

    def Elements(self, node=None):
        if node is None:
            return [child[1] for child in self.children if child[0]]
        elif node == '*':
            return [child[1] for child in self.children]
        else:
            return [child[1] for child in self.children if child[0] == node]
        
    def RemoveElement(self, node):
        self.children[:] = [child for child in self.children if child[1] is not node]

    def Unravel(self):
        unravelstop = int(self.settings.get('unravelstop', '0'))
        if not unravelstop and self.parent():
            # Recursively unravel the next level up
            unravelstop = self.parent().Unravel()
            if unravelstop > 0:
                return result

        if unravelstop < 0:
            # Should unravel N stops up the line
            return unravelstop + 1

        # Unravel this node and everything below it
        self._UnravelNode()

    def _UnravelNode(self):
        # Unravel this node and everything below it
        if self.parent():
            self.parent().RemoveElement(self)

        # Context Var/Node settings
        if self.settings.get('contextnode', None):
            for name in strtolist(self.settings['contextnode']):
                delattr(self.context, name)
        if self.settings.get('contextvar', None) and self.object:
            for name in strtolist(self.settings['contextvar']):
                delattr(self.context, name)

        # Parent Var/Node settings
        if self.context._NextContext:
            if self.settings.get('parentnode', None):
                for name in strtolist(self.settings['parentnode']):
                    delattr(self.context, name)
            if self.settings.get('parentvar', None) and self.object:
                for name in strtolist(self.settings['parentvar']):
                    delattr(self.context._NextContext, name)

        try: del self.children
        except AttributeError: pass
        try: del self.object
        except AttributeError: pass
        try: del self.context
        except AttributeError: pass
        try: del self.parent
        except AttributeError: pass
        try: del self.settings
        except AttributeError: pass
        return 1

    #~ Parent Search Patterns ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def FindParent(self, *Types):
        p = self.parent()
        while p:
            if isinstance(p, *Types):
                return p
            else: p = p.parent()
        return None

    def FindParentOrObject(self, *Types):
        p = self.parent()
        while p:
            if isinstance(p.object, Types) or isinstance(p, Types):
                return p.object
            else: p = p.parent()
        return None

    def FindParentObject(self, *Types):
        p = self.parent()
        while p:
            if isinstance(p.object, Types):
                return p.object
            else: p = p.parent()
        return None

    #~ Eval Helpers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetEvalLocals(self, **variables):
        variables['self'] = weakref.proxy(self)
        variables['ctx'] = variables['context'] = weakref.proxy(self.context)
        if self.parent():
            variables['parentObj'] = self.parent().object
        return variables

    def _GetEvalLocalsEx(self, variables):
        variables.update(self._GetEvalLocals())
        return variables

    def EvalLocal(self, code, **variables):
        return eval(code, self.globalnamespace, self._GetEvalLocals(**variables))

    def EvalLocalEx(self, code, variables):
        return eval(code, self.globalnamespace, self._GetEvalLocalsEx(variables))
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Private Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _addElement(self, node, element):
        self.children.append((node[1], element))

    __addDataHadNewLine = 1
    def _addData(self, data):
        HadNewline, self.__addDataHadNewLine = self.__addDataHadNewLine, data[-1] in '\n\r'
        if not HadNewline and self.children and self.children[-1][0] == '':
            data = self.children.pop()[1] + data
        self.children.append(('', data))

    def _xmlInitStarted(self):
        self.SkinInitialize()

        # Context Var/Node settings
        if self.settings.get('contextnode', None):
            for name in strtolist(self.settings['contextnode']):
                setattr(self.context, name, weakref.proxy(self))
        if self.settings.get('contextvar', None) and self.object:
            for name in strtolist(self.settings['contextvar']):
                setattr(self.context, name, self.object)

        # Parent Var/Node settings
        if self.context._NextContext:
            if self.settings.get('parentnode', None):
                for name in strtolist(self.settings['parentnode']):
                    setattr(self.context._NextContext, name, weakref.proxy(self))
            if self.settings.get('parentvar', None) and self.object:
                for name in strtolist(self.settings['parentvar']):
                    setattr(self.context._NextContext, name, self.object)

    def _xmlInitComplete(self):
        # Test this first
        if self.object:
            # Skin finalize might change it
            self.SkinFinalize()
        else:
            # Skin finalize might change it
            self.SkinFinalize()
            # Now act on knowing that self.object wasn't set before
            if self.settings.get('contextvar', None):
                for name in strtolist(self.settings['contextvar']):
                    setattr(self.context, name, self.object)
            if self.settings.get('parentvar', None) and self.object and self.context._NextContext:
                for name in strtolist(self.settings['parentvar']):
                    setattr(self.context._NextContext, name, self.object)

        if int(self.settings.get('unravel', '0')):
            self.Unravel()
        elif int(self.settings.get('unravelnode', '0')):
            self._UnravelNode()

    def _toXML(self, strSplit='', *args, **kw):
        result = []
        children = getattr(self, 'children', [])
        for node, each in children:
            if node:
                result.append(each._toXML(strSplit, *args, **kw))

        result = filter(None, result)
        if strSplit is not None:
            return strSplit.join(result)
        else: return result

