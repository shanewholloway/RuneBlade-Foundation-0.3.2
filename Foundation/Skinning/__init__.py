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

"""TODO: Document"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from XMLSkinner import XMLSkinner as _XMLSkinner
from Foundation.XMLClassBuilder import ElementFactory as EF

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

StandardElementFactories = {
    ## Long names
    ('http://namespaces.runeblade.com/skin',): EF.NodeImport('Foundation.Skinning.skin'),
    ('http://namespaces.runeblade.com/wxPythonSkin',): EF.NodeImport('Foundation.Skinning.wxPythonSkin'), 
    ('http://namespaces.runeblade.com/xmlPython',): EF.NodeImport('Foundation.Skinning.xmlPython'), 
    ('http://namespaces.runeblade.com/wxogl',): EF.NodeImport('Foundation.Skinning.wxOGLSkin'), 
    ('http://namespaces.runeblade.com/state',): EF.NodeImport('Foundation.Skinning.StateSkin'), 
    ('http://namespaces.runeblade.com/dot',): EF.NodeImport('Foundation.Skinning.dotSkin'), 
    ('http://namespaces.runeblade.com/objectify',): EF.CachedTryList([
        EF.NodeImport('Foundation.Skinning.xmlObjectifySkin'), 
        EF.StaticImport('Foundation.Skinning.xmlObjectifySkin.ObjectifiedXMLSkin', 'ObjectifiedXMLSkin')]),

    ## Not-Just-RuneBlade schemes
    ('http://www.w3.org/1999/xhtml',): EF.CachedTryList([
        EF.NodeImport('Foundation.Skinning.xhtml'), 
        EF.StaticImport('Foundation.Skinning.xhtml.xhtml', 'xhtml'),]),

    ('http://www.w3.org/2000/svg',): EF.CachedTryList([
        EF.NodeImport('Foundation.Skinning.svg'), 
        EF.StaticImport('Foundation.Skinning.svg.svg', 'svg'),]),

    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

StandardNamespaceSynonyms = {
    'skin': 'http://namespaces.runeblade.com/skin',
    'wxPythonSkin': 'http://namespaces.runeblade.com/wxPythonSkin',
    'xmlPython': 'http://namespaces.runeblade.com/xmlPython',
    'wxogl': 'http://namespaces.runeblade.com/wxogl',
    'state': 'http://namespaces.runeblade.com/state',
    'dot': 'http://namespaces.runeblade.com/dot',
    'objectify': 'http://namespaces.runeblade.com/objectify',

    'xhtml': 'http://www.w3.org/1999/xhtml',
    'svg': 'http://www.w3.org/2000/svg',
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StandardXMLSkinner(_XMLSkinner):
    ElementFactories = _XMLSkinner.ElementFactories.copy()
    ElementFactories.update(StandardElementFactories)

    NamespaceSynonyms = _XMLSkinner.NamespaceSynonyms.copy()
    NamespaceSynonyms.update(StandardNamespaceSynonyms)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def SkinFile(*args, **kw):
    return StandardXMLSkinner().SkinFile(*args, **kw)

def SkinXML(*args, **kw):
    return StandardXMLSkinner().SkinXML(*args, **kw)

