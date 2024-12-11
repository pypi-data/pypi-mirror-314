"""
Sphinx Read the Docs theme. (Patched for ESP-IDF)

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.
"""

from os import path
from sys import version_info as python_version

from sphinx import version_info as sphinx_version
from sphinx.locale import _
from sphinx.util.logging import getLogger


__version__ = '0.1'
__version_full__ = __version__

logger = getLogger(__name__)


def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
    return cur_dir


def config_initiated(app, config):
    theme_options = config.html_theme_options or {}
    if theme_options.get('canonical_url'):
        logger.warning(
            _('The canonical_url option is deprecated, use the html_baseurl option from Sphinx instead.')
        )

# See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
    if python_version[0] < 3:
        logger.warning("Python 2 is deprecated with sphinx_rtd_theme, update to Python 3")
    app.require_sphinx('1.6')
    if sphinx_version <= (2, 0, 0):
        logger.warning("Sphinx 1.x is deprecated with sphinx_rtd_theme, update to Sphinx 2.x or greater")
        if not app.config.html_experimental_html5_writer:
            logger.warning("'html4_writer' is deprecated with sphinx_rtd_theme")
    else:
        if app.config.html4_writer:
            logger.warning("'html4_writer' is deprecated with sphinx_rtd_theme")

    # Register the theme that can be referenced without adding a theme path
    app.add_html_theme('sphinx_idf_theme', path.abspath(path.dirname(__file__)))

    if sphinx_version >= (1, 8, 0):
        # Add Sphinx message catalog for newer versions of Sphinx
        # See http://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_message_catalog
        rtd_locale_path = path.join(path.abspath(path.dirname(__file__)), 'locale')
        app.add_message_catalog('sphinx', rtd_locale_path)
        app.connect('config-inited', config_initiated)

    # sphinx emits the permalink icon for headers, so choose one more in keeping with our theme
    if sphinx_version >= (3, 5, 0):
        app.config.html_permalinks_icon = "\uf0c1"
    else:
        app.config.html_add_permalinks = "\uf0c1"

    app.add_config_value('project_slug', '', 'html')
    app.add_config_value('versions_url', '', 'html')
    app.add_config_value('project_homepage', '', 'html')
    app.add_config_value('languages', None, 'html')
    app.add_config_value('download_url', '', 'html')
    app.add_config_value('latest_branch_name', 'master', 'html')
    app.add_config_value('html_zip', '', 'html')

    # we expect IDF to also add these, but older version may not (and the theme supports non-target-aware docs)
    if "idf_target" not in app.config:
        app.add_config_value('idf_target', None, 'env')
    if "idf_targets" not in app.config:
        app.add_config_value('idf_targets', None, 'env')

    app.connect('html-page-context', inject_template_context)

    return {'parallel_read_safe': True, 'parallel_write_safe': True}


def inject_template_context(app, pagename, templatename, context, doctree):
    # expose some IDF-specific config in the html_context dict for the theme
    for key in [ "project_slug", "versions_url", "project_homepage", "languages", "idf_target", "idf_targets", "project", "pdf_file", "html_zip", "latest_branch_name"]:
        context[key] = app.config[key]

    # Dictonary for converting from idf target slug to a proper title (esp32s2 -> ESP32-S2)
    context["idf_target_title_dict"] = app.config["idf_target_title_dict"]

    if not app.config.languages:
        raise RuntimeError("The 'languages' config item needs to be set to a list of supported languages (even if just a single element list)")
    if not app.config.language:
        raise RuntimeError("The 'language' config item needs to be set to the language in use")
    if bool(app.config.idf_target) != bool(app.config.idf_targets):
        raise RuntimeError("Either both 'idf_target' and 'idf_targets' variables should be set in Sphinx config, or neither should be set in config.")
    if app.config.pdf_file and app.config.html_zip:
        raise RuntimeError('Download link should be either a html zip (html_zip) or pdf (pdf_file). Both configs should not be set at the same time')
