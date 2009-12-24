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
from transaction import commit
from zope import event, component
from zope.proxy import removeAllProxies
from zope.security.proxy import removeSecurityProxy
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
from zope.traversing.interfaces import IContainmentRoot
from zope.app.component.hooks import getSite, setSite
from zope.app.component.site import LocalSiteManager, SiteManagementFolder
from zope.app.security.interfaces import IEveryoneGroup, IAuthenticatedGroup
from zope.securitypolicy.interfaces import Allow
from zope.securitypolicy.interfaces import IRolePermissionManager
from zope.securitypolicy.interfaces import IPrincipalPermissionManager

from zope.app.intid.interfaces import IIntIds
from zope.app.principalannotation.interfaces import IPrincipalAnnotationUtility

from z3c.configurator import configure, ConfigurationPluginBase

from zojax.product.interfaces import IProduct
from zojax.skintool.interfaces import ISkinTool
from zojax.controlpanel.interfaces import IConfiglet
from zojax.content.space.interfaces import IWorkspaceFactory
from zojax.authentication.interfaces import \
    IAuthenticationConfiglet, IAuthenticatorPluginFactory

from zojax.principal.roles.role import PortalRole
from zojax.principal.roles.interfaces import IPortalRoles, IDefaultPortalRole

from interfaces import IPortal


def reconfigurePortal(app, *args):
    portal = removeSecurityProxy(app)
    configure(portal, {})


class BasicPortalConfiguration(ConfigurationPluginBase):
    component.adapts(IPortal)

    def __call__(self, data):
        portal = self.context

        # create site manager
        try:
            sm = portal.getSiteManager()
        except:
            sm = None

        if sm is None:
            sm = LocalSiteManager(portal)
            portal.setSiteManager(sm)

        setSite(portal)

        if 'system' not in sm:
            system = SiteManagementFolder()
            event.notify(ObjectCreatedEvent(system))
            sm['system'] = system
        else:
            system = sm['system']

        # IIntId utility
        if 'ids' not in system:
            ids = component.createObject('zope.app.intid.IntIds')
            event.notify(ObjectCreatedEvent(ids))
            system['ids'] = ids
        else:
            system['ids'].__init__()

        ids = system['ids']

        sm.registerUtility(system['ids'], IIntIds)
        ids.register(portal)

        # Principal Annotations
        if 'principalannotations' not in system:
            pa = component.createObject('zope.app.PrincipalAnnotationUtility')
            event.notify(ObjectCreatedEvent(pa))

            system['principalannotations'] = pa
            sm.registerUtility(pa, IPrincipalAnnotationUtility)

        # session data container
        configlet = sm.getUtility(IConfiglet, 'system.session')
        configlet.sessiontype = 'ram'

        # set password
        password = sm.getUtility(IConfiglet, 'principals.password')
        password.passwordManager = 'MD5'

        # set site timezone
        fomratter = sm.getUtility(IConfiglet, 'system.formatter')
        fomratter.timezone = u'UTC'

        # set portal access to open
        manager = IPrincipalPermissionManager(portal)
        everyone = sm.queryUtility(IEveryoneGroup)
        if everyone is not None:
            manager.grantPermissionToPrincipal(
                'zojax.AccessPortal', everyone.id)

        authenticated = sm.queryUtility(IAuthenticatedGroup)
        if authenticated is not None:
            manager.unsetPermissionForPrincipal(
                'zojax.AccessPortal', authenticated.id)

        # setup default role
        roles = sm.getUtility(IPortalRoles)
        if 'site.member' not in roles:
            role = PortalRole(title = u'Site Member')
            event.notify(ObjectCreatedEvent(role))

            roles['site.member'] = role
            roleId = role.id
            sm.getUtility(IDefaultPortalRole).roles = [role.id]

            roleperm = IRolePermissionManager(portal)

            for permId in ('zojax.PersonalContent', 'zojax.PersonalSpace',
                           'zojax.forum.addMessage', 'zojax.forum.addTopic',
                           'zojax.SubmitBlogPost', 'zojax.SubmitDocuments',
                           'zojax.forum.SubmitTopic', 'zojax.SubmitPhoto',
                           'zojax.contenttype.SubmitNewsItem',):
                roleperm.grantPermissionToRole(permId, roleId)

        # install catalog
        sm.getUtility(IConfiglet, 'system.catalog').install()

        # install workspaces
        portal.workspaces = ('overview', 'people', 'news', 'documents')
        event.notify(ObjectModifiedEvent(portal))

        setSite(None)


class ContentTypesConfiguration(ConfigurationPluginBase):
    component.adapts(IPortal)

    dependencies = ('basic',)

    def __call__(self, data):
        # install content types
        setSite(self.context)

        sm = self.context.getSiteManager()

        product = sm.queryUtility(IProduct, 'zojax-contenttypes')
        if product is not None and not product.isInstalled():
            product.install()

        setSite(None)


class AuthenticationConfiguration(ConfigurationPluginBase):
    component.adapts(IPortal)

    dependencies = ('basic',)

    def __call__(self, data):
        # authentication
        setSite(self.context)

        sm = self.context.getSiteManager()
        auth = sm.getUtility(IAuthenticationConfiglet)
        auth.installUtility()

        if IContainmentRoot.providedBy(self.context):
            auth.installPrincipalRegistry()

        for name in ('principal.users',):
            factory = sm.queryUtility(IAuthenticatorPluginFactory, name=name)
            if factory is not None:
                factory.install()
                factory.activate()

        setSite(None)
