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

from wxSkinLayoutObject import wxSkinLayoutObject, wxColorEval, wxSkinObjectNoData
from wxPython.grid import *
from wxPython.wx import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class grid(wxSkinLayoutObject, wxSkinObjectNoData):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = wxSkinLayoutObject.default_settings.copy()
    default_settings.update({
        'name':     __name__,
        'wxid':       'wxNewId()',
        'custom':   '0',
        'lines':    '1',
        'editable': '1',
        'margins':  '0,0',
        'selectmode':'cells',
        'dragsize': 'all',
        'autosize': 'all',
        'columns':  "['A','B','C','D','E']",
        'rows':     "['1','2','3','4','5']",
        'rowlabelsize': '',
        'collabelsize': '',
        'fgselection': 0,
        'bgselection': 0,
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        winParent = self.wxGetParentObject(wx.wxWindowPtr)
        kwSettings = self.wxSettingDict(['wxid', 'style', 'pos', 'size'], ['name'])
        self.object = wxGrid(winParent, **kwSettings)
        self.object.BeginBatch()
        self.wxInitialStandardOptions()

    def SkinFinalize(self):
        self.AddToLayout()
        self.wxFinalStandardOptions()

        if not self.wxEval('custom'):
            cols = self.wxEval('columns')
            if isinstance(cols, int): cols = map(chr, xrange(65, 65+cols))
            colcount = len(cols)

            rows = self.wxEval('rows')
            if isinstance(rows, int): rows = map(str, xrange(1, 1+rows))
            rowcount = len(rows)

            if rowcount or colcount:
                self.object.CreateGrid(rowcount, colcount)
            
            idx = 0
            for each in cols:
                if isinstance(each, tuple): self.object.SetColLabelValue(idx, *each)
                else: self.object.SetColLabelValue(idx, each)
                idx += 1
            idx = 0
            for each in rows:
                if isinstance(each, tuple): self.object.SetRowLabelValue(idx, *each)
                else: self.object.SetRowLabelValue(idx, each)
                idx += 1

            # Misc Options
            self.object.EnableEditing(self.wxEval('editable'))
            self.object.EnableGridLines(self.wxEval('lines'))
            self.object.SetMargins(*self.wxEval('margins'))

            if self.settings['fgselection']:
                self.object.SetSelectionForeground(wxColorEval(self.settings['fgselection']))
            if self.settings['bgselection']:
                self.object.SetSelectionBackground(wxColorEval(self.settings['bgselection']))

            # Row and Column Labels
            if self.settings['rowlabelsize']:
                self.object.SetRowLabelSize(self.wxEval('rowlabelsize'))
            if self.settings['collabelsize']:
                self.object.SetColLabelSize(self.wxEval('collabelsize'))

            # Autosize
            autosize = self.settings['autosize'].lower()
            if autosize == 'all':
                self.object.AutoSizeRows()
                self.object.AutoSizeColumns()
            elif autosize == 'rows':
                self.object.AutoSizeRows()
            elif autosize == 'columns':
                self.object.AutoSizeColumns()

            # Draw Size
            dragsize = self.settings['dragsize'].lower()
            if dragsize == 'all':
                self.object.EnableDragGridSize(1)
            elif dragsize == 'rows':
                self.object.EnableDragRowSize(1)
                self.object.EnableDragColSize(0)
            elif dragsize == 'columns':
                self.object.EnableDragRowSize(0)
                self.object.EnableDragColSize(1)
            elif dragsize == 'none':
                self.object.EnableDragGridSize(0)

            # Selection Mode
            selectmode = self.settings['selectmode'].lower()
            if selectmode == 'cells':
                self.object.SetSelectionMode(self.object.wxGridSelectCells)
            elif selectmode == 'rows':
                self.object.SetSelectionMode(self.object.wxGridSelectRows)
            elif selectmode == 'columns':
                self.object.SetSelectionMode(self.object.wxGridSelectColumns)
 
        self.object.EndBatch()
