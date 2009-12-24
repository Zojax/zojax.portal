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
from zope import event, component, interface
from zope.publisher.browser import TestRequest
from zope.security.management import queryInteraction
from zope.app.component.hooks import setSite
from z3c.configurator import ConfigurationPluginBase

from zojax.portal.interfaces import IPortal
from zojax.portlet.interfaces import ENABLED, IPortletManager
from zojax.controlpanel.interfaces import IConfiglet


class ConfigureExtension(ConfigurationPluginBase):
    component.adapts(IPortal)

    dependencies = ('basic',)

    def __call__(self, data):
        # we need request
        setSite(self.context)
        request = TestRequest()

        portal = self.context
        sm = portal.getSiteManager()

        # setup default skin
        skintool = sm.queryUtility(IConfiglet, 'ui.portalskin')
        skintool.skin = u'zojax'

        interface.directlyProvides(request, *skintool.generate())

        # setup portlets
        portlets = sm.queryMultiAdapter(
            (portal, request, None), IPortletManager, 'columns.left')
        portlets.status = ENABLED
        portlets.__data__['portletIds'] = ('portlet.login', 'portlet.actions')

        setSite(None)
