# Copyright © 2016,2017 STRG.AT GmbH, Vienna, Austria
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

from score.init import ConfiguredModule
from score.tpl import Renderer
from pystache import Renderer as PystacheRenderer


defaults = {
    'extension': 'mustache',
}


def init(confdict, tpl):
    """
    Initializes this module acoording to the :ref:`SCORE module initialization
    guidelines <module_initialization>` with the following configuration keys:
    """
    conf = defaults.copy()
    conf.update(confdict)
    return ConfiguredMustacheModule(tpl, conf['extension'])


class ConfiguredMustacheModule(ConfiguredModule):

    def __init__(self, tpl, extension):
        import score.jslib
        super().__init__(score.jslib)
        self.tpl = tpl
        self.extension = extension
        tpl.engines[extension] = self._create_renderer
        tpl.filetypes['text/html'].extensions.append(extension)

    def _create_renderer(self, tpl_conf, filetype):
        return MustacheRenderer(self, tpl_conf, filetype)


class MustacheRenderer(Renderer):

    def __init__(self, mustache_conf, *args, **kwargs):
        self._mustache_conf = mustache_conf
        super().__init__(*args, **kwargs)
        self.renderer = PystacheRenderer(
            file_extension=self._mustache_conf.extension,
            partials=self._create_partial_loader())

    def render_file(self, file, variables, path=None):
        string = open(file).read()
        return self.render_string(string, variables, path)

    def render_string(self, string, variables, path=None):
        variables = self._get_variables(variables)
        return self.renderer.render(string, variables)

    def _get_variables(self, variables):
        # Cannot respect the "escape" flag, as pystache does not support
        # unescaped *variables*. If you need to render something unescaped, you
        # need to use triple-braces in your mustache templates:
        # http://mustache.github.io/mustache.5.html#Variables
        result = dict((name, value)
                      for name, value, escape in self.filetype.globals)
        result.update(variables)
        return result

    def _create_partial_loader(self):
        class PartialLoader:
            def get(loader, path):
                is_file, result = self._tpl_conf.load(
                    '%s.%s' % (path, self._mustache_conf.extension))
                if is_file:
                    result = open(result).read()
                return result
        return PartialLoader()
