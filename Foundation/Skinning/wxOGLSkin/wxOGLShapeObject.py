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

from wxOGLSkinObject import wxOGLSkinObject, ogl, wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Initialization 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
class wxOGLShapeObject(wxOGLSkinObject):

    default_settings = wxOGLSkinObject.default_settings.copy()
    default_settings.update({
        'x':    '10',
        'y':    '10',
        'show': '1',
        'drag': '0',
        'dragrecursive': '0',
        'pen': 'wxBLACK_PEN',
        'brush': 'wxLIGHT_GREY_BRUSH',
        'text': '',
        'shadowmode': 'SHADOW_RIGHT',
        'controlpoints': '0',

        })

    def AddShape(self):
        """Add a self.object to the parent diagram"""
        ogldiagram = self.wxGetParentObject(ogl.wxDiagram)
        oglcanvas = self.wxGetParentObject(ogl.wxShapeCanvas)

        self.object.SetDraggable(self.oglEval('drag'), self.oglEval('dragrecursive'))
        self.object.SetCanvas(oglcanvas)
        self.object.SetX(self.oglEval('x'))
        self.object.SetY(self.oglEval('y'))
        self.object.SetPen(self.oglEval('pen'))
        self.object.SetBrush(self.oglEval('brush'))
        self.object.AddText(self.settings['text'])
        self.object.SetShadowMode(self.oglEval('shadowmode'))
        if self.oglEval('controlpoints'): 
            self.object.MakeControlPoints()
        self.object.Show(self.oglEval('show'))
        ogldiagram.AddShape(self.object)


        #self.objects.append(self.object)

    
