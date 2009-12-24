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
"""Server Control View

$Id$
"""
__docformat__ = 'restructuredtext'

from zope.component import getUtility
from zope.app.applicationcontrol.interfaces import IServerControl
from zope.app.applicationcontrol.i18n import ZopeMessageFactory as _

from zojax.wizard.step import WizardStep
from zojax.statusmessage.interfaces import IStatusMessage


class ServerControlView(WizardStep):

    def serverControl(self):
        return getUtility(IServerControl)

    def update(self):
        control = self.serverControl()
        time = self.request.get('time', 0)

        if 'restart' in self.request:
            control.restart(time)
            IStatusMessage(self.request).add(
                _("The server will be restarted in ${number} seconds.",
                  mapping={"number": time}))
        elif 'shutdown' in self.request:
            control.shutdown(time)
            IStatusMessage(self.request).add(
                _("The server will be shutdown in ${number} seconds.",
                  mapping={"number": time}))
