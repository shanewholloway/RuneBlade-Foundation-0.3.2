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

class node_settings(DOTSkinObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = DOTSkinObject.default_settings.copy()
    default_settings.update({
        # bottomlabel                           auxiliary label for nodes of shape M*
        # color          black                  node shape color
        # comment                               any string (format-dependent)
        # distortion     0.0                    node distortion for shape=polygon
        # fillcolor      lightgrey/black        node fill color
        # fixedsize      false                  label text has no affect on node size
        # fontcolor      black                  type face color
        # fontname       Times-Roman            font family
        # fontsize       14 point               size of label
        # group                                 name of node’s group
        # height         .5                     height in inches
        # label                                 node name any string
        # layer          overlay range          all, id or id:id
        # orientation    0.0                    node rotation angle
        # peripheries    shape-dependent        number of node boundaries
        # regular        false                  force polygon to be regular
        # shape          ellipse                node shape; see Section 2.1 and Appendix E
        # shapefile                             external EPSF or SVG custom shape file
        # sides          4                      number of sides for shape=polygon
        # skew           0.0                    skewing of node for shape=polygon
        # style                                 graphics options, e.g. bold, dotted, filled; cf. Section 2.3
        # toplabel                              auxiliary label for nodes of shape M*
        # URL                                   URL associated with node (format-dependent)
        # width          .75                    width in inches
        # z              0.0                    z coordinate for VRML output
        })

    _DOTRelatedAttributes = {
        'bottomlabel':1, 'color':1, 'comment':1, 'distortion':1, 'fillcolor':1, 'fixedsize':1, 'fontcolor':1, 'fontname':1,
        'fontsize':1, 'group':1, 'height':1, 'label':1, 'layer':1, 'orientation':1, 'peripheries':1, 'regular':1, 'shape':1,
        'shapefile':1, 'sides':1, 'skew':1, 'style':1, 'filled':1, 'toplabel':1, 'URL':1, 'width':1, 'z':1, }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _toDOT(self, joinstr='\n', close=1):
        return 'node [%s]%s' % (self._OutputDOTSettings(), close and ';' or '')

