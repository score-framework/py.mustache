# Copyright © 2015,2016 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

"""
Implements the :term:`engine <template engine>` for mustache templates.
"""


import os
import pystache
from score.tpl.engine import Engine as EngineBase, EngineRenderer


class Engine(EngineBase):
    """
    :class:`score.tpl.Engine` for mustache files.
    """

    def create_subrenderer(self, format, rootdir, cachedir):
        if format == 'html':
            return HtmlRenderer(format, rootdir, cachedir)
        return DefaultRenderer(format, rootdir, cachedir)


class DefaultRenderer(EngineRenderer):
    """
    The :class:`<score.tpl.EngineRenderer>` for mustache templates.
    """

    def __init__(self, format, rootdir, cachedir):
        self.format = format
        self.rootdir = rootdir
        self.cachedir = cachedir
        self.globals = {}

    def add_function(self, name, value, escape_output=True):
        pass

    def add_filter(self, name, callback, escape_output=True):
        pass

    def add_global(self, name, value):
        self.globals[name] = value

    def render_string(self, string, variables):
        renderer = self.create_pystache_renderer()
        variables = variables.copy()
        variables.update(self.globals)
        return renderer.render(string, **variables)

    def render_file(self, filepath, variables):
        renderer = self.create_pystache_renderer(filepath)
        abspath = os.path.join(self.rootdir, filepath)
        variables = variables.copy()
        variables.update(self.globals)
        return renderer.render_path(abspath, **variables)

    def create_pystache_renderer(self, filepath=None):
        search_dirs = [self.rootdir]
        if filepath and '/' in filepath:
            search_dirs.insert(
                os.path.join(self.rootdir, os.path.dirname(filepath)), 0)
        return pystache.Renderer(search_dirs=search_dirs, missing_tags='strict',
                                 escape=lambda x: x)


class HtmlRenderer(DefaultRenderer):
    """
    The :class:`<score.tpl.EngineRenderer>` for mustache templates.
    """

    def create_pystache_renderer(self, filepath=None):
        from html import escape
        renderer = super().create_pystache_renderer(filepath)
        renderer.escape = escape
        return renderer
