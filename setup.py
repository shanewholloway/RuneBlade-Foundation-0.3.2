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

from distutils.core import setup
import Foundation 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PackageOptions = {}

try:
    from Foundation import __doc__ as DocBase

    PackageOptions['Base'] = {
        'name': 'RuneBlade Foundation Base',
        'long_description':DocBase,
        'keywords':['select', 'weakbind', 'xml', 'objectify', 'xmlobjectify'],
        'packages':['Foundation', ]
        }
except ImportError: pass

try:
    from Foundation.SubjectObserver import __doc__ as DocSubjectObserver
    PackageOptions['_SubjectObserver'] = {
        'name': 'RuneBlade Subject Observer Base',
        'long_description': DocSubjectObserver,
        'keywords':['subject', 'observer', 'publish', 'subscribe', 'notification'],
        'packages':['Foundation.SubjectObserver'],
        }

    PackageOptions['SubjectObserver'] = {
        'name': 'RuneBlade Subject Observer',
        'long_description': DocSubjectObserver,
        'keywords': PackageOptions['_SubjectObserver']['keywords'] + PackageOptions['Base']['keywords'],
        'packages': PackageOptions['_SubjectObserver']['packages'] + PackageOptions['Base']['packages'],
        }
except ImportError: pass

try:
    from Foundation.Jabber import __doc__ as DocJabber
    PackageOptions['_Jabber'] = {
        'name': 'RuneBlade Jabber Base',
        'long_description': DocJabber,
        'keywords':['jabber'],
        'packages':['Foundation.Jabber'],
        }

    PackageOptions['Jabber'] = {
        'name': 'RuneBlade Jabber',
        'long_description': DocJabber,
        'keywords': PackageOptions['_Jabber']['keywords'] + PackageOptions['SubjectObserver']['keywords'],
        'packages': PackageOptions['_Jabber']['packages'] + PackageOptions['SubjectObserver']['packages'],
        }
except ImportError: pass

try:
    from Foundation.Skinning import __doc__ as DocSkinning
    PackageOptions['_Skinning'] = {
        'name': 'RuneBlade Skinning Base',
        'long_description': DocSkinning,
        'keywords':['skinning','wxPython','locking','docking'],
        'packages':[
            'Foundation.Skinning', 
            'Foundation.Skinning.skin', 
            'Foundation.Skinning.xmlPython', 
            'Foundation.Skinning.wxPythonSkin', 
            'Foundation.Skinning.wxOGLSkin', 
            'Foundation.Skinning.StateSkin', 
            'Foundation.Skinning.xhtml', 
            'Foundation.Skinning.xmlObjectifySkin', 
            'Foundation.Skinning.dotskin', 
            'Foundation.wxTools'],
        }

    PackageOptions['Skinning'] = {
        'name': 'RuneBlade Skinning',
        'long_description':DocSkinning,
        'keywords': PackageOptions['_Skinning']['keywords'] + PackageOptions['SubjectObserver']['keywords'],
        'packages': PackageOptions['_Skinning']['packages'] + PackageOptions['SubjectObserver']['packages'],
        }
except ImportError: pass

try:
    from Foundation import __doc__ as DocFoundation
    PackageOptions['Foundation'] = {
        'name': 'RuneBlade Foundation',
        'long_description': DocFoundation,
        'keywords': ['RuneBlade'] + PackageOptions['_Skinning']['keywords'] + PackageOptions['_Jabber']['keywords'] + PackageOptions['_SubjectObserver']['keywords'] + PackageOptions['Base']['keywords'],
        'packages': PackageOptions['_Skinning']['packages'] + PackageOptions['_Jabber']['packages'] + PackageOptions['_SubjectObserver']['packages'] + PackageOptions['Base']['packages'],
        }
except ImportError: pass

try:
    from Foundation import __doc__ as DocBase

    PackageOptions['Docs'] = {
        'name': 'RuneBlade Foundation Docs',
        'long_description': PackageOptions['Foundation']['long_description'],
        'keywords': PackageOptions['Foundation']['keywords'],
        'packages':[]
        }
except ImportError: pass

try:
    from Foundation import __doc__ as DocBase

    PackageOptions['Demos'] = {
        'name': 'RuneBlade Foundation Demos',
        'long_description': PackageOptions['Foundation']['long_description'],
        'keywords': PackageOptions['Foundation']['keywords'],
        'packages':[]
        }
except ImportError: pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PackageBase = {
    'version': Foundation.__version__,
    'author': Foundation.__author__,
    'author_email': Foundation.__author_email__,
    'url': Foundation.__url__,
    'platforms': 'Linux, BSD, Windows',
    'license': 'LGPL (http://www.fsf.org/licenses/lgpl.txt)', #Foundation.__license__, # 
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import getopt, sys
try:
    options, sys.argv[1:] = getopt.getopt(sys.argv[1:], '', ['package='])
    options = dict(options)
    PackageIndex = options.get('--package','Foundation')
except getopt.GetoptError:
    PackageIndex = 'Foundation'

Package = PackageBase.copy()
Package.update(PackageOptions[PackageIndex])
Package['name'] = Package['name'].replace(' ', '-')
setup(**Package)

