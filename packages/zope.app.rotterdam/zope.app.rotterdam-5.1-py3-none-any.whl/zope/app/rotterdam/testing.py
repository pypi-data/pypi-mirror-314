##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""zope.app.rotterdam common test related classes/functions/objects.
"""

__docformat__ = "reStructuredText"


import unittest

import zope.component
import zope.component.interfaces
from webtest import TestApp
from zope.app.wsgi.testlayer import BrowserLayer
from zope.publisher.browser import BrowserView
from zope.security.proxy import removeSecurityProxy
from zope.site.site import LocalSiteManager

import zope.app.rotterdam


RotterdamLayer = BrowserLayer(
    zope.app.rotterdam,
    allowTearDown=True)


class BrowserTestCase(unittest.TestCase):

    layer = RotterdamLayer

    def setUp(self):
        super().setUp()
        self._testapp = TestApp(self.layer.make_wsgi_app())

    def publish(self, path, basic=None, form=None, headers=None):
        assert basic
        self._testapp.authorization = ('Basic', tuple(basic.split(':')))

        env = {'wsgi.handleErrors': False}
        if form:
            response = self._testapp.post(path, params=form,
                                          extra_environ=env, headers=headers)
        else:
            response = self._testapp.get(
                path, extra_environ=env, headers=headers)
        return response


class MakeSite(BrowserView):
    # copied from zope.app.component to break the circular dependency

    def addSiteManager(self):
        assert not zope.component.interfaces.ISite.providedBy(self.context)

        # We don't want to store security proxies (we can't,
        # actually), so we have to remove proxies here before passing
        # the context to the SiteManager.
        bare = removeSecurityProxy(self.context)
        sm = LocalSiteManager(bare)
        self.context.setSiteManager(sm)
        self.request.response.redirect(
            "++etc++site/@@SelectedManagementView.html")
