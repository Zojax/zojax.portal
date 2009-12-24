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
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.content.space.interfaces import IContentSpace

_ = MessageFactory(u'zojax.portal')


class IPortal(IContentSpace):
    """ zojax portal instance """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Portal title.'),
        required = True)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Portal description.'),
        required = False)


class ICommonPortal(IPortal):
    """ common portal """


class IPortalConfiglet(interface.Interface):
    """ configlet """


class IPortalRegistrations(interface.Interface):
    """ porta registration """


class IPortalRegistries(interface.Interface):
    """ porta registries """
