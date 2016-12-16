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

from score.init import ConfiguredModule


defaults = {
}


def init(confdict, tpl=None, js=None):
    """
    Initializes this module acoording to the :ref:`SCORE module initialization
    guidelines <module_initialization>`.
    """
    conf = defaults.copy()
    conf.update(confdict)
    return ConfiguredMustacheModule(js)


class ConfiguredMustacheModule(ConfiguredModule):

    def __init__(self, js):
        import score.mustache
        super().__init__(score.mustache)
        self.js = js
        urltpl = js.route_single.urltpl.pattern.replace('.js', '.mustache')
        js.http.router.define_static_route(
            'score.mustache', urltpl, js.rootdir,
            after=js.route_single,
            force_mimetype=('text/mustache', 'UTF-8'))
