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

class line(wxOGLShapeObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxOGLShapeObject.default_settings.copy()
    default_settings.update({
        'arrow': 'ARROW_ARROW',
        'controlpoints': '0',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        ogldiagram = self.wxGetParentObject(ogl.wxDiagram)
        oglcanvas = self.wxGetParentObject(ogl.wxShapeCanvas)
        fromShape = getattr(self.context, self.settings['from'])
        toShape = getattr(self.context, self.settings['to'])
        self.object = ogl.wxLineShape()
        self.object.SetCanvas(oglcanvas)
        self.object.SetPen(self.oglEval('pen'))
        self.object.SetBrush(self.oglEval('brush'))
        self.object.AddArrow(self.oglEval('arrow'))
        if self.oglEval('controlpoints') >= 2: 
            self.object.MakeLineControlPoints(self.oglEval('controlpoints'))
            self.object.MakeControlPoints()
        fromShape.AddLine(self.object, toShape)
        ogldiagram.AddShape(self.object)
        self.object.Show(self.oglEval('show'))
