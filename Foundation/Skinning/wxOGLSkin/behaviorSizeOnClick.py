#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
from wxOGLSkinObject import wxOGLSkinObject, wx, ogl
from wxPython.ogl import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Initialization 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
class behaviorSizeOnClick(wxOGLSkinObject):

    def SkinInitialize(self):
        self.object = BehaviorHandler()
        #shape = self.wxGetParentObject(ogl.wxShape)
        shape = self.parent().object
        self.object.SetShape(shape)
        self.object.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(self.object)
        
class BehaviorHandler(wxShapeEvtHandler):


    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        shape = self.GetShape()
        #print shape.__class__
        canvas = shape.GetCanvas()
        dc = wxClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(0, dc)
            canvas.Redraw(dc)
        else:
            redraw = 0
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []
            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(1, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(0, dc)
                canvas.Redraw(dc)

