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
from wxOGLShapeObject import ogl, wxOGLShapeObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Initialization 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class rectangle(wxOGLShapeObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxOGLShapeObject.default_settings.copy()
    default_settings.update({
        'width':    '5.0',
        'height':   '5.0',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        self.object = ogl.wxRectangleShape()
        kwSettings = self.oglSettingDict(['width', 'height'])
        self.object = ogl.wxRectangleShape(**kwSettings)
        self.AddShape()




