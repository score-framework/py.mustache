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
