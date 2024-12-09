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
"""Rotterdam utilities tests
"""
import codecs
import os
import os.path


here = os.path.dirname(__file__)
input_dir = os.path.join(here, 'input')
output_dir = os.path.join(here, 'output')


def read_output(filename):
    filename = os.path.join(output_dir, filename)
    with codecs.open(filename, 'r', 'utf-8') as f:
        return f.read()
