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

from DOTSkinObject import DOTSkinObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Initialization 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class edge_settings(DOTSkinObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = DOTSkinObject.default_settings.copy()
    default_settings.update({
        # arrowhead                             normal style of arrowhead at head end
        # arrowsize         1.0                 scaling factor for arrowheads
        # arrowtail         normal              style of arrowhead at tail end
        # color             black               edge stroke color
        # comment                               any string (format-dependent)
        # constraint        true                use edge to affect node ranking
        # decorate                              if set, draws a line connecting labels with their edges
        # dir               forward             forward, back, both, or none
        # fontcolor         black               type face color
        # fontname          Times-Roman         font family
        # fontsize          14                  point size of label
        # headlabel                             label placed near head of edge
        # headport                              n,ne,e,se,s,sw,w,nw
        # headURL                               URL attached to head label if output format is ismap
        # label                                 edge label
        # labelangle        -25.0               angle in degrees which head or tail label is rotated off edge
        # labeldistance     1.0                 scaling factor for distance of head or tail label from node
        # labelfloat        false               lessen constraints on edge label placement
        # labelfontcolor    black               type face color for head and tail labels
        # labelfontname     Times-Roman         font family for head and tail labels
        # labelfontsize     14                  point size for head and tail labels
        # layer             overlay range       all, id or id:id
        # lhead                                 name of cluster to use as head of edge
        # ltail                                 name of cluster to use as tail of edge
        # minlen            1                   minimum rank distance between head and tail
        # samehead                              tag for head node; edge heads with the same tag are merged onto the same port
        # sametail                              tag for tail node; edge tails with the same tag are merged onto the same port
        # style                                 graphics options, e.g. bold, dotted, filled; cf. Section 2.3
        # taillabel                             label placed near tail of edge
        # tailport                              n,ne,e,se,s,sw,w,nw
        # tailURL                               URL attached to tail label if output format is ismap
        # weight            1                   integer cost of stretching an edge
        })

    _DOTRelatedAttributes = {
        'arrowhead':1, 'arrowsize':1, 'arrowtail':1, 'color':1, 'comment':1, 'constraint':1, 'decorate':1, 'dir':1, 'fontcolor':1,
        'fontname':1, 'fontsize':1, 'headlabel':1, 'headport':1, 'headURL':1, 'label':1, 'labelangle':1, 'labeldistance':1, 'labelfloat':1,
        'labelfontcolor':1, 'labelfontname':1, 'labelfontsize':1, 'layer':1, 'lhead':1, 'ltail':1, 'minlen':1, 'samehead':1, 'sametail':1,
        'style':1, 'taillabel':1, 'tailport':1, 'tailURL':1, 'weight':1,}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _toDOT(self, joinstr='\n', close=1):
        return 'edge [%s]%s' % (self._OutputDOTSettings(), close and ';' or '')

