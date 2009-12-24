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
"""UI for browsing database schema managers

$Id$
"""
import transaction
import zope.component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.generations.interfaces import ISchemaManager
from zope.app.generations.generations import generations_key, Context
from zope.app.renderer.rest import ReStructuredTextToHTMLRenderer

from zojax.wizard.step import WizardStep

request_key_format = "evolve-app-%s"


class GenerationsView(WizardStep):

    template = ViewPageTemplateFile('generations.pt')

    def _getdb(self):
        return self.request.publication.db

    def update(self):
        self.managers = managers = dict(
            zope.component.getUtilitiesFor(ISchemaManager))

        db = self._getdb()
        conn = db.open()
        try:
            generations = conn.root().get(generations_key, ())
            request = self.request
            for key in generations:
                generation = generations[key]
                rkey = request_key_format % key
                if rkey in request:
                    manager = managers[key]
                    if generation >= manager.generation:
                        IStatusMessage(self.request).add(
                            _('The database is up to date for ${application}.',
                              mapping={'application': key}))

                    context = Context()
                    context.connection = conn
                    generation += 1
                    manager.evolve(context, generation)
                    generations[key] = generation
                    transaction.commit()
                    IStatusMessage(self.request).add(
                        _('The database was updated to generation ${generation} for ${application}.',
                          mapping={'application': key, 'generation':generation}))
        finally:
            transaction.abort()
            conn.close()

    def applications(self):
        result = []

        db = self._getdb()
        conn = db.open()
        try:
            managers = self.managers
            generations = conn.root().get(generations_key, ())
            for key in generations:
                generation = generations[key]
                manager = managers.get(key)
                if manager is None:
                    continue

                result.append({
                    'id': key,
                    'min': manager.minimum_generation,
                    'max': manager.generation,
                    'generation': generation,
                    'evolve': (generation < manager.generation
                               and request_key_format % key
                               or ''
                               ),
                    })

            return result
        finally:
            conn.close()

    def getEvolvers(self):
        id = self.request.get('id', u'')
        manager = zope.component.queryUtility(ISchemaManager, id)
        if manager is None:
            return

        evolvers = []

        for gen in range(manager.minimum_generation, manager.generation):

            info = manager.getInfo(gen+1)
            if info is None:
                info = ''
            else:
                renderer = ReStructuredTextToHTMLRenderer(
                    unicode(info), self.request)
                info = renderer.render()

            evolvers.append({'from': gen, 'to': gen+1, 'info': info})

        return evolvers
