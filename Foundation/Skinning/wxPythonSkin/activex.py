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

from wxSkinLayoutObject import wx, wxSkinLayoutObject
from Foundation.wxTools.wxActiveXWrapper import wxActiveXControlFactory
from win32com.client import gencache, dynamic
import pywintypes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class activex(wxSkinLayoutObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinLayoutObject.default_settings.copy()
    default_settings.update({
        'name': __name__,

        #'progid': None,
        #'clsid': None,

        'eventClasses': 'tuple()',
        'eventObj': 'None',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        CoClass = self.GetAXControlCoClass()

        # Prepare to make the ActiveX class that we can instantiate
        kwAXSettings = self.wxSettingDict(['eventClasses', 'eventObj'], [])
        ActiveXClass = wxActiveXControlFactory(CoClass, **kwAXSettings)

        # Find the necessary things to instantiate the ActiveX control
        winParent = self.wxGetParentObject(wx.wxWindowPtr)
        kwSettings = self.wxSettingDict(['wxid', 'style', 'pos', 'size'], [])

        # Make the ActiveX Control Instance!
        self.object = ActiveXClass(winParent, **kwSettings)

        # Do our standard wxPythonSkin thing
        self.wxInitialStandardOptions()

    def SkinFinalize(self):
        self.AddToLayout()
        self.wxFinalStandardOptions()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GetAXControlCoClass(self):
        ClassIndex = self.settings.get('progid', None) or self.settings['clsid']
        CoClass = gencache.GetClassForProgID(ClassIndex)
        if not CoClass:
            # Well, we might not have a cached one... so lets go find the TypeLib
            dis = dynamic.Dispatch(pywintypes.IID(ClassIndex))
            tlbAttr = dis._lazydata_[0].GetContainingTypeLib()[0].GetLibAttr()
            # Now gencache it
            TLB = gencache.EnsureModule(tlbAttr[0], tlbAttr[1], tlbAttr[3], tlbAttr[4])
            # And try Aagain
            CoClass = gencache.GetClassForProgID(ClassIndex)
            if not CoClass:
                # Dang... still didn't work
                raise KeyError, "ActiveX class not found for %r (%r)" % (ClassIndex, )
        return CoClass

    def GetAXControlModule(self):
        ClassIndex = self.settings.get('progid', None) or self.settings['clsid']
        module = gencache.GetModuleForProgID(ClassIndex)
        if not module:
            # Well, we might not have a cached one... so lets go find the TypeLib
            dis = dynamic.Dispatch(pywintypes.IID(ClassIndex))
            tlbAttr = dis._lazydata_[0].GetContainingTypeLib()[0].GetLibAttr()
            # Now gencache it
            TLB = gencache.EnsureModule(tlbAttr[0], tlbAttr[1], tlbAttr[3], tlbAttr[4])
            # And try Aagain
            module = gencache.GetModuleForProgID(ClassIndex)
            if not module:
                # Dang... still didn't work
                raise KeyError, "ActiveX class not found for %r (%r)" % (ClassIndex, )
        return module

