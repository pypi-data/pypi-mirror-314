##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Tests for navigation tree
"""
import unittest
from xml.dom import minidom

from zope.app.rotterdam.testing import BrowserTestCase


class TestNavTree(BrowserTestCase):

    def test_navtree(self):
        # Add some folders
        response = self.publish("/+/action.html", basic='mgr:mgrpw',
                                form={'type_name': 'zope.app.content.Folder',
                                      'id': 'First'})
        self.assertEqual(response.status_int, 302)
        response = self.publish("/+/action.html", basic='mgr:mgrpw',
                                form={'type_name': 'zope.app.content.Folder',
                                      'id': 'S&econd'})
        self.assertEqual(response.status_int, 302)
        response = self.publish("/+/action.html", basic='mgr:mgrpw',
                                form={'type_name': 'zope.app.content.Folder',
                                      'id': 'Third'})
        self.assertEqual(response.status_int, 302)
        response = self.publish("/First/+/action.html", basic='mgr:mgrpw',
                                form={'type_name': 'zope.app.content.Folder',
                                      'id': 'Firsts"Folder'})
        self.assertEqual(response.status_int, 302)
        response = self.publish("/First/+/action.html", basic='mgr:mgrpw',
                                form={'type_name': 'zope.app.content.Folder',
                                      'id': 'somesite'})
        self.assertEqual(response.status_int, 302)

        # add a site manager This will break when site adding is fixed
        # see above for examples to fix by filling out a form
        # when further action is required to make a site
        response = self.publish("/First/somesite/addSiteManager.html",
                                basic='mgr:mgrpw')
        self.assertEqual(response.status_int, 302)
        # /First/FirstsFolder/@@singleBranchTree.xml
        # contains those 4 elements above
        # /@@children.xml
        # contains First Second and Third

        response = self.publish(
            "/First/somesite/++etc++site/@@singleBranchTree.xml",
            basic='mgr:mgrpw')
        self.assertEqual(response.status_int, 200)

        minidom.parseString(response.body)

        response = self.publish("/@@children.xml", basic='mgr:mgrpw')
        self.assertEqual(response.status_int, 200)

        minidom.parseString(response.body)

        response = self.publish("/First/+/action.html", basic='mgr:mgrpw',
                                form={'type_name': 'zope.app.content.Folder',
                                      'id': 'Firsts2ndFolder'})
        self.assertEqual(response.status_int, 302)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
