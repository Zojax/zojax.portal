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
import zope.component.interfaces

from zope.app.component import vocabulary
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ILocalSiteManager
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.portal.interfaces import _
from zojax.product.registry import broken
from zojax.layoutform import button, Fields, PageletEditForm


class IComponentsBases(interface.Interface):
    """An interface describing the bases API of the IComponents object."""

    __bases__ = schema.List(
        title=_(u'Bases'),
        description=_(u'The base components registires of this registry.'),
        value_type=schema.Choice(vocabulary='zojax.portal.baseComponents'),
        required=True)


BROKEN = _('-- Broken Registry --')
BASENAME = _('-- Global Base Registry --')

class BaseComponentsVocabulary(vocabulary.UtilityVocabulary):
    """A vocabulary for ``IComponents`` utilities."""

    interface = zope.component.interfaces.IComponents

    def __init__(self, context, **kw):
        super(BaseComponentsVocabulary, self).__init__(context, **kw)
        self._terms[BASENAME] = vocabulary.UtilityTerm(
            zope.component.globalregistry.base, BASENAME)
        self._terms[BROKEN] = vocabulary.UtilityTerm(broken, BROKEN)


class SetBasesPage(PageletEditForm):
    """A page to set the bases of a local site manager"""

    fields = Fields(IComponentsBases)

    label = _(u'Components registry')

    def getContent(self):
        site = getSite().getSiteManager()

        bases = [sm for sm in site.__bases__ if not ILocalSiteManager.providedBy(sm)]

        return {'__bases__': bases}

    @button.buttonAndHandler(_(u"Apply"))
    def handle_edit_action(self, action):
        data, errors = self.extractData()

        site = getSite().getSiteManager()

        bases = [sm for sm in site.__bases__ if
                 ILocalSiteManager.providedBy(sm) and sm not in data['__bases__']]
        site.__bases__ = tuple(data['__bases__'] + bases)
