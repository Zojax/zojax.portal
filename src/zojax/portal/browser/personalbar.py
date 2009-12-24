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
from zope import interface
from zope.security import checkPermission
from zope.viewlet.viewlet import ViewletBase
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL


class ControlPanelMenuItem(ViewletBase):

    weight = 999

    def update(self):
        self.url = '%s/settings/'%absoluteURL(getSite(), self.request)

    def isAvailable(self):
        return checkPermission('zojax.Configure', getSite())
