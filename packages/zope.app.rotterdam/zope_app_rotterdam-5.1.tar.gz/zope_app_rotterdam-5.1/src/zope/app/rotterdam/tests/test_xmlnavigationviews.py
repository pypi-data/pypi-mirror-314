##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""XML Navigation Tree Tests
"""

import unittest

import zope.component
import zope.component.interfaces
from zope.component.testing import PlacelessSetup
from zope.container.interfaces import IReadContainer
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
from zope.interface import implementer
from zope.pagetemplate.tests.util import normalize_xml
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.site.folder import Folder
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager
from zope.traversing.api import traverse
from zope.traversing.interfaces import ITraversable

from zope.app.rotterdam.testing import RotterdamLayer
from zope.app.rotterdam.tests import util
from zope.app.rotterdam.xmlobject import ReadContainerXmlObjectView
from zope.app.rotterdam.xmlobject import XmlObjectView


def browserView(for_, name, factory, layer=IDefaultBrowserLayer,
                providing=zope.interface.Interface):
    """Define a global browser view
    """
    provideAdapter(for_, providing, factory, name, (layer,))


stypes = list, tuple


def provideAdapter(required, provided, factory, name='', using=None, **kw):
    assert not isinstance(factory, stypes), "Factory cannot be a list or tuple"

    gsm = zope.component.getGlobalSiteManager()

    if using:
        required = (required, ) + tuple(using)
    assert isinstance(required, stypes)

    gsm.registerAdapter(factory, required, provided, name, event=False)


class File:
    pass


class Place:

    def __init__(self, path):
        self.path = path

    def __get__(self, inst, cls=None):
        if inst is None:  # pragma: no cover
            return self

        # Use __dict__ directly to avoid infinite recursion
        root = inst.__dict__['rootFolder']

        return traverse(root, self.path)


def buildSampleFolderTree():
    # set up a reasonably complex folder structure
    #
    #     ____________ rootFolder ______________________________
    #    /                                    \                 \
    # folder1 __________________            folder2           folder3
    #   |                       \             |                 |
    # folder1_1 ____           folder1_2    folder2_1         folder3_1
    #   |           \            |            |
    # folder1_1_1 folder1_1_2  folder1_2_1  folder2_1_1

    root = rootFolder()
    root['folder1'] = Folder()
    root['folder1']['folder1_1'] = Folder()
    root['folder1']['folder1_1']['folder1_1_1'] = Folder()
    root['folder1']['folder1_1']['folder1_1_2'] = Folder()
    root['folder1']['folder1_2'] = Folder()
    root['folder1']['folder1_2']['folder1_2_1'] = Folder()
    root['folder2'] = Folder()
    root['folder2']['folder2_1'] = Folder()
    root['folder2']['folder2_1']['folder2_1_1'] = Folder()
    root["\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER A}"
         "\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER KA}"
         "\N{CYRILLIC SMALL LETTER A}3"] = Folder()
    root["\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER A}"
         "\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER KA}"
         "\N{CYRILLIC SMALL LETTER A}3"][
        "\N{CYRILLIC SMALL LETTER PE}"
        "\N{CYRILLIC SMALL LETTER A}"
        "\N{CYRILLIC SMALL LETTER PE}"
        "\N{CYRILLIC SMALL LETTER KA}"
        "\N{CYRILLIC SMALL LETTER A}3_1"] = Folder()

    return root


def createSiteManager(folder, setsite=False):
    if not zope.component.interfaces.ISite.providedBy(folder):
        folder.setSiteManager(LocalSiteManager(folder))
    if setsite:
        zope.component.hooks.setSite(folder)
    return zope.traversing.api.traverse(folder, "++etc++site")


def setUpTraversal():
    from zope.traversing.testing import setUp
    setUp()
    zope.component.provideAdapter(ContainerTraversable,
                                  (ISimpleReadContainer,), ITraversable)


class PlacefulSetup(PlacelessSetup):

    # Places :)
    rootFolder = Place('')

    folder1 = Place('folder1')
    folder1_1 = Place('folder1/folder1_1')
    folder1_1_1 = Place('folder1/folder1_1/folder1_1_1')
    folder1_1_2 = Place('folder1/folder1_2/folder1_1_2')
    folder1_2 = Place('folder1/folder1_2')
    folder1_2_1 = Place('folder1/folder1_2/folder1_2_1')

    folder2 = Place('folder2')
    folder2_1 = Place('folder2/folder2_1')
    folder2_1_1 = Place('folder2/folder2_1/folder2_1_1')

    folder3 = Place("\N{CYRILLIC SMALL LETTER PE}"
                    "\N{CYRILLIC SMALL LETTER A}"
                    "\N{CYRILLIC SMALL LETTER PE}"
                    "\N{CYRILLIC SMALL LETTER KA}"
                    "\N{CYRILLIC SMALL LETTER A}3")
    folder3_1 = Place("\N{CYRILLIC SMALL LETTER PE}"
                      "\N{CYRILLIC SMALL LETTER A}"
                      "\N{CYRILLIC SMALL LETTER PE}"
                      "\N{CYRILLIC SMALL LETTER KA}"
                      "\N{CYRILLIC SMALL LETTER A}3/"
                      "\N{CYRILLIC SMALL LETTER PE}"
                      "\N{CYRILLIC SMALL LETTER A}"
                      "\N{CYRILLIC SMALL LETTER PE}"
                      "\N{CYRILLIC SMALL LETTER KA}"
                      "\N{CYRILLIC SMALL LETTER A}3_1")

    def setUp(self, folders=False, site=False):
        PlacelessSetup.setUp(self)
        setUpTraversal()
        if folders or site:
            return self.buildFolders(site)

    def buildFolders(self, site=False):
        self.rootFolder = buildSampleFolderTree()
        if site:
            return self.makeSite()

    def makeSite(self, path='/'):
        folder = traverse(self.rootFolder, path)
        return createSiteManager(folder, True)


class TestXmlObject(PlacefulSetup, unittest.TestCase):

    layer = RotterdamLayer
    maxDiff = None

    def setUp(self):
        PlacefulSetup.setUp(self, site=True)

    def check_xml(self, s1, s2):
        s1 = normalize_xml(s1)
        s2 = normalize_xml(s2)
        self.assertEqual(s1, s2)

    def testXMLTreeViews(self):
        rcxov = ReadContainerXmlObjectView
        treeView = rcxov(self.folder1, TestRequest()).singleBranchTree
        self.check_xml(treeView(), util.read_output('test1.xml'))

        treeView = rcxov(self.folder1, TestRequest()).children
        self.check_xml(treeView(), util.read_output('test2.xml'))

        treeView = rcxov(self.folder1_1_1, TestRequest()).children
        self.check_xml(treeView(), util.read_output('test3.xml'))

        treeView = rcxov(self.rootFolder, TestRequest()).children
        self.check_xml(treeView(), util.read_output('test4.xml'))

        file1 = File()
        self.folder1_1_1["file1"] = file1
        self.file1 = traverse(self.rootFolder,
                              '/folder1/folder1_1/folder1_1_1/file1')

        @implementer(IBrowserPublisher)
        class ReadContainerView(ReadContainerXmlObjectView):
            def browserDefault(self, request):
                raise NotImplementedError()

            def publishTraverse(self, request, name):
                raise NotImplementedError()

            def __call__(self):
                return self.singleBranchTree()

        browserView(IReadContainer, 'singleBranchTree.xml',
                    ReadContainerView)

        treeView = rcxov(self.folder1_1_1, TestRequest()).singleBranchTree
        self.check_xml(treeView(), util.read_output('test5.xml'))

        treeView = XmlObjectView(self.file1, TestRequest()).singleBranchTree
        self.check_xml(treeView(), util.read_output('test5.xml'))

    def test_virtualhost_support(self):

        # we have to add a virtual host subsite
        folder1 = self.rootFolder['folder1']
        subsite = Folder()
        sm = LocalSiteManager(folder1)
        subsite.setSiteManager(sm)
        folder1['subsite'] = subsite

        # add some more folder to the subsite
        subfolder1 = Folder()
        subsite['subfolder1'] = subfolder1
        subfolder2 = Folder()
        subfolder2_1 = Folder()
        subfolder2['subfolder2_1'] = subfolder2_1
        subsite['subfolder2'] = subfolder2

        # set the virtualhost on the request
        request = TestRequest()
        request._vh_root = subsite

        # test virtual host root
        vh = request.getVirtualHostRoot()
        self.assertEqual(vh, subsite)

        rcxov = ReadContainerXmlObjectView
        treeView = rcxov(subsite, request).singleBranchTree
        self.check_xml(treeView(), util.read_output('test6.xml'))

        rcxov = ReadContainerXmlObjectView
        treeView = rcxov(subfolder1, request).singleBranchTree
        self.check_xml(treeView(), util.read_output('test7.xml'))

        rcxov = ReadContainerXmlObjectView
        treeView = rcxov(subfolder2_1, request).singleBranchTree
        self.check_xml(treeView(), util.read_output('test8.xml'))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
