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

class graph_settings(DOTSkinObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = DOTSkinObject.default_settings.copy()
    default_settings.update({
        # bgcolor            background          color for drawing, plus initial fill color
        # center             false               center drawing on page
        # clusterrank        local               may be global or none
        # color              black               for clusters, outline color, and fill color if fillcolor not defined
        # comment                                any string (format-dependent)
        # compound           false               allow edges between clusters
        # concentrate        false               enables edge concentrators
        # fillcolor          black               cluster fill color
        # fontcolor          black               type face color
        # fontname           Times-Roman         font family
        # fontpath                               list of directories to such for fonts
        # fontsize           14                  point size of label
        # label                                  any string
        # labeljust          left-justified      ”r” for right-justified cluster labels
        # labelloc           top                 ”r” for right-justified cluster labels
        # layers                                 id:id:id...
        # margin             .5                  margin included in page, inches
        # mclimit            1.0                 scale factor for mincross iterations
        # nodesep            .25                 separation between nodes, in inches.
        # nslimit                                if set to f, bounds network simplex iterations by (f)(number of nodes) when setting x-coordinates
        # nslimit1                               if set to f, bounds network simplex iterations by (f)(number of nodes) when ranking nodes
        # ordering                               if `out` out edge order is preserved
        # orientation        portrait            if rotate is not used and the value is landscape, use landscape orientation
        # page                                   unit of pagination, e.g. "8.5,11"
        # pagedir            BL                  traversal order of pages
        # quantum                                if quantum ¿ 0.0, node label dimensions will be rounded to integral multiples of quantum
        # rank                                   same, min, max, source or sink
        # rankdir            TB                  LR (left to right) or TB (top to bottom)
        # ranksep            .75                 separation between ranks, in inches.
        # ratio                                  approximate aspect ratio desired, fill or auto
        # remincross                             if true and there are multiple clusters, re-run crossing minimization
        # rotate                                 If 90, set orientation to landscape
        # samplepoints       8                   number of points used to represent ellipses and circles on output (cf. Appendix C
        # searchsize         30                  maximum edges with negative cut values to check when looking for a minimum one during network simplex
        # size                                   maximum drawing size, in inches
        # style                                  graphics options, e.g. filled for clusters
        # URL                                    URL associated with graph (format-dependent)
        })

    _DOTRelatedAttributes = {
        'bgcolor':1, 'center':1, 'clusterrank':1, 'color':1, 'comment':1, 'compound':1, 'concentrate':1, 'fillcolor':1, 'fontcolor':1, 'fontname':1, 
        'fontpath':1, 'fontsize':1, 'label':1, 'labeljust':1, 'labelloc':1, 'layers':1, 'margin':1, 'mclimit':1, 'nodesep':1, 'nslimit':1, 'nslimit1':1, 
        'ordering':1, 'orientation':1, 'page':1, 'pagedir':1, 'quantum':1, 'rank':1, 'rankdir':1, 'ranksep':1, 'ratio':1, 'remincross':1, 'rotate':1, 
        'samplepoints':1, 'searchsize':1, 'size':1, 'style':1, 'URL':1}
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _toDOT(self, joinstr='\n', close=1):
        return 'graph [%s]%s' % (self._OutputDOTSettings(), close and ';' or '')

