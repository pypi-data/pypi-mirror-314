from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Iframe, Link, Script


@plugin_pool.register_plugin
class LinkTagPlugin(CMSPluginBase):

    model = Link
    name = 'LINK'
    module = 'HTML Elements'
    render_template = "cms_qe_plugins/link.html"


@plugin_pool.register_plugin
class ScriptTagPlugin(CMSPluginBase):

    model = Script
    name = 'SCRIPT'
    module = 'HTML Elements'
    render_template = "cms_qe_plugins/script.html"


@plugin_pool.register_plugin
class IframeTagPlugin(CMSPluginBase):

    model = Iframe
    name = 'IFRAME'
    module = 'HTML Elements'
    render_template = "cms_qe_plugins/iframe.html"
