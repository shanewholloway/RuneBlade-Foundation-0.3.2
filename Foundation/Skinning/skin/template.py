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
from Foundation.Skinning.SkinObject import SkinObject
from Foundation.Skinning.UtilitySkinElements import StoreXML, RestoreStoredXMLMixin
from Foundation.XMLClassBuilder import ElementFactory, ElementFactorySet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class template(SkinObject, RestoreStoredXMLMixin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = SkinObject.default_settings.copy()
    #default_settings['name'] = ''
    #default_settings['invoke'] = ''
    #default_settings['expand'] = ''

    ElementFactories = {
        ('http://namespaces.runeblade.com/skin', 'factory'): ElementFactory.StaticImport('Foundation.Skinning.skin.factory', 'factory'),
        None: ElementFactory.Static(StoreXML)
        }

    mode = 0
    _StoringMode = 1
    _ExpandingMode = 2
    _InvokingMode = 3

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, owner, parent, node, attributes, namespacemap): 
        SkinObject.__init__(self, owner, parent, node, attributes, namespacemap)
        self.owner = owner
        self.ElementFactories = ElementFactorySet(self.ElementFactories)

    def SkinInitialize(self):
        if 'name' in self.settings:
            self.mode = self._StoringMode
        elif 'expand' in self.settings:
            self.mode = self._ExpandingMode
        elif 'invoke' in self.settings:
            self.mode = self._InvokingMode
        else:
            raise AttributeError, "%r node must have one attribute in ['name','expand','invoke']" % self.__class__.__name__

        if 'unravelnode' not in self.source_settings:
            if self.mode in [self._ExpandingMode, self._InvokingMode]:
                self.settings['unravelnode'] = '1'

        self.owner.PushElementFactorySet(self.ElementFactories)

    def SkinFinalize(self):
        self.owner.PopElementFactorySet()

        if self.mode == self._StoringMode:
            setattr(self.context, self.settings['name'], weakref.proxy(self))
        elif self.mode == self._ExpandingMode:
            TemplateInner = getattr(self.context, '::invoke:' + self.settings['expand'])
            TemplateInner.RestoreChildren(self.owner)
        elif self.mode == self._InvokingMode:
            InvokeName = self.settings['invoke']
            TemplateOuter = getattr(self.context, InvokeName)
            self.parent().PushContext(force=1)
            setattr(self.context, '::invoke:' + InvokeName, weakref.proxy(self))
            TemplateOuter.RestoreChildren(self.owner)
            delattr(self.context, '::invoke:' + InvokeName)
            self.parent().PopContext()

        del self.owner

