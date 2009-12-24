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
import zope.component.interfaces
import zope.publisher.interfaces.browser
from zope.traversing.browser import absoluteURL
from zope.app.component.browser.registration import \
    IRegistrationDisplay, ISiteRegistrationDisplay
from zope.app.component.i18n import ZopeMessageFactory as _


class AdapterRegistrationDisplay(object):
    """Adapter Registration Details"""

    component.adapts(zope.component.interfaces.IAdapterRegistration,
                     zope.publisher.interfaces.browser.IBrowserRequest)
    interface.implements(IRegistrationDisplay)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def required(self):
        required = []

        for iface in self.context.required:
            required.append(iface.__module__ + '.' + iface.__name__)

        return ', '.join(required)

    def provided(self):
        provided = self.context.provided
        return provided.__module__ + '.' + provided.__name__

    def id(self):
        return 'R' + (("%s %s" % (self.provided(), self.context.name))
                      .encode('utf8')
                      .encode('base64')
                      .replace('+', '_')
                      .replace('=', '')
                      .replace('\n', '')
                      )

    def _comment(self):
        comment = self.context.info or ''
        if comment:
            comment = _("comment: ${comment}", mapping={"comment": comment})
        return comment

    def _provided(self):
        name = self.context.name
        provided = self.provided()
        if name:
            info = _("${provided} utility named '${name}'",
                     mapping={"provided": provided, "name": name})
        else:
            info = _("${provided} utility",
                     mapping={"provided": provided})
        return info

    def render(self):
        return {
            "info": self._provided(),
            "comment": self._comment()
            }

    def unregister(self):
        self.context.registry.unregisterAdapter(
            self.context.component,
            self.context.required,
            self.context.provided,
            self.context.name,
            )


class AdapterSiteRegistrationDisplay(AdapterRegistrationDisplay):
    """Adapter Registration Details"""

    interface.implementsOnly(ISiteRegistrationDisplay)

    def render(self):
        try:
            url = absoluteURL(self.context.component, self.request)
        except:
            url = ''

        cname = 'Adapter: %s'%self.required()
        if url:
            url += "/@@SelectedManagementView.html"

        return {
            "cname": cname,
            "url": url,
            "info": self._provided(),
            "comment": self._comment()
            }
