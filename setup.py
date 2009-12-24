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
"""Setup for zojax.portal package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.0.3'


setup(name = 'zojax.portal',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "zojax portal",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax'],
      install_requires = ['setuptools', 'ZODB3',
                          'zope.component',
                          'zope.interface',
                          'zope.proxy',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.keyreference',
                          'zope.traversing',
                          'zope.publisher',
                          'zope.security',
                          'zope.securitypolicy',
                          'zope.lifecycleevent',
                          'zope.copypastemove',
                          'zope.size',
                          'zope.app.appsetup',
                          'zope.app.component',
                          'zope.app.security',
                          'zope.app.zopeappgenerations',
                          'zope.app.generations',
                          'zope.app.applicationcontrol',
                          'zope.app.server',
                          'zope.app.twisted',
                          'zope.app.wsgi',
                          'zope.app.http',
                          'zope.app.intid',
                          'zope.app.principalannotation',
                          'zope.app.pagetemplate',
                          'zope.app.renderer',

                          'z3c.configurator',

                          'zojax.content.type',
                          'zojax.content.forms',
                          'zojax.content.browser',
                          'zojax.content.model',
                          'zojax.content.space',
                          'zojax.content.actions',
                          'zojax.content.attachment',
                          'zojax.content.permissions',
                          'zojax.content.discussion',
                          'zojax.content.models.document',
                          'zojax.content.models.container',

                          'zojax.contenttypes',
                          'zojax.contenttype.page',
                          'zojax.contenttype.event',
                          'zojax.contenttype.newsitem',
                          'zojax.contenttype.file',
                          'zojax.contenttype.image',
                          'zojax.contenttype.document',

                          'zojax.folder',
                          'zojax.groups',
                          'zojax.site',

                          'zojax.activity',
                          'zojax.authentication',
                          'zojax.controlpanel',
                          'zojax.error',
                          'zojax.extensions',
                          'zojax.mail',
                          'zojax.portlet',
                          'zojax.product',
                          'zojax.formatter',
                          'zojax.memcached',
                          'zojax.language',
                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.wizard',
                          'zojax.security',
                          'zojax.session',
                          'zojax.skintool',

                          'zojax.personal.bar',
                          'zojax.personal.space',
                          'zojax.personal.profile',
                          'zojax.personal.content',
                          'zojax.personal.invitation',

                          'zojax.principal.ban',
                          'zojax.principal.profile',
                          'zojax.principal.password',
                          'zojax.principal.management',
                          'zojax.principal.registration',
                          'zojax.principal.roles',
                          'zojax.principal.users',

                          'zojax.portlets.login',
                          'zojax.portlets.htmlsource',
                          'zojax.portlets.navigation',

                          'zojax.theme.default',
                          ],
      extras_require = dict(test=['zojax.autoinclude']),
      include_package_data = True,
      zip_safe = False
      )
