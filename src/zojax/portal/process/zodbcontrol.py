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
""" Server Control View

$Id$
"""
from ZODB.interfaces import IDatabase
from ZODB.FileStorage.FileStorage import FileStorageError

from zope.size import byteDisplay
from zope.component import getUtilitiesFor, getUtility
from zope.app.applicationcontrol.i18n import ZopeMessageFactory as _
from zojax.wizard.step import WizardStep
from zojax.statusmessage.interfaces import IStatusMessage


class ZODBControlView(WizardStep):

    @property
    def databases(self):
        res = []
        for name, db in getUtilitiesFor(IDatabase):
            d = dict(
                dbName = db.getName(),
                utilName = str(name),
                size = self._getSize(db),
                )
            res.append(d)
        return res

    def _getSize(self, db):
        """Get the database size in a human readable format."""
        size = db.getSize()
        if not isinstance(size, (int, long, float)):
            return str(size)
        return byteDisplay(size)

    def update(self):
        status = []
        if 'PACK' in self.request.form:
            dbs = self.request.form.get('dbs', [])
            try:
                days = int(self.request.form.get('days','').strip() or 0)
            except ValueError:
                IStatusMessage(self.request).add(
                    _('Error: Invalid Number'), 'error')
                return

            for dbName in dbs:
                db = getUtility(IDatabase, name=dbName)
                try:
                    db.pack(days=days)
                    IStatusMessage(self.request).add(
                        _('ZODB "${name}" successfully packed.',
                          mapping=dict(name=str(dbName))))
                except FileStorageError, err:
                    IStatusMessage(self.request).add(
                        _('ERROR packing ZODB "${name}": ${err}',
                          mapping=dict(name=str(dbName), err=err)), 'error')
