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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class winAlphaBlend(object):
    GWL_EXSTYLE           = 0xffffffec
    WS_EX_LAYERED         = 0x00080000
    LWA_COLORKEY          = 0x00000001
    LWA_ALPHA             = 0x00000002

    alpha = 1.0
    colorkey = None

    def __init__(self, hWnd):
        self.hWnd = hWnd

        import win32api
        win32api.SetWindowLong(hWnd, self.GWL_EXSTYLE, win32api.GetWindowLong(hWnd, self.GWL_EXSTYLE) ^ self.WS_EX_LAYERED);

        import calldll
        self.__calldll = calldll
        self.__User32Library = self.__calldll.load_library ('user32.dll')
        self.__addrSetLayeredWindowAttributes = self.__calldll.get_proc_address(self.__User32Library, 'SetLayeredWindowAttributes')
        assert self.__addrSetLayeredWindowAttributes 

    def __del__(self):
        if self.__User32Library: 
            self.__calldll.free_library(self.__User32Library)

        try: del self.__calldll
        except AttributeError: pass

    def __SetLayeredWindowAttributes(self, alpha, colorkey, flag):
        if flag:
            self.__calldll.call_foreign_function(self.__addrSetLayeredWindowAttributes, 'LLBL', '', (self.hWnd, colorkey, alpha, flag))

    def Blend(self, alpha=None, colorkey=None, usedefaults=1):
        flag = 0
        if alpha is not None:
            self.alpha = alpha
            alpha = int(255 * alpha)
            flag |= self.LWA_ALPHA
        elif usedefaults: 
            alpha = int(255 * self.alpha)
            if alpha < 255: flag |= self.LWA_ALPHA
        else: 
            self.alpha = 1.0
            alpha = 255

        if colorkey is not None:
            flag |= self.LWA_COLORKEY
            self.colorkey = colorkey
        elif usedefaults: 
            if self.colorkey is None: colorkey = 0
            else: 
                colorkey = self.colorkey
                if colorkey is not None:
                    flag |= self.LWA_COLORKEY
        else:
            colorkey = 0
            self.colorkey = None

        self.__SetLayeredWindowAttributes(alpha, colorkey, flag)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxAlphaBlend(winAlphaBlend):
    def __init__(self, window, *args, **kw):
        super(wxAlphaBlend, self).__init__(window.GetHandle(), *args, **kw)
