##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zope.copypastemove.interfaces import IObjectCopier, IObjectMover

from zojax.portal.base import PortalObject
from zojax.portal.interfaces import ICommonPortal
from zojax.content.space.content import ContentSpace


class Portal(ContentSpace, PortalObject):
    interface.implements(ICommonPortal)

    showTabs = True
    showHeader = False
    workspaces = ('overview',)

    def __init__(self, title=u'Portal', **kw):
        super(Portal, self).__init__(title=u'Portal', **kw)


class PortalCopier(object):
    component.adapts(ICommonPortal)
    interface.implements(IObjectCopier)

    def __init__(self, object):
        self.context = object

    def copyTo(self, target, new_name=None):
        raise RuntimeError('Object is not copyable')

    def copyable(self):
        return False

    def copyableTo(self, target, name=None):
        return False


class PortalMover(object):
    component.adapts(ICommonPortal)
    interface.implements(IObjectMover)

    def __init__(self, object):
        self.context = object

    def moveTo(self, target, new_name=None):
        raise RuntimeError('Object is not moveable')

    def moveable(self):
        return False

    def moveableTo(self, target, name=None):
        return False
