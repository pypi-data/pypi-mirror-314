from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

from mkdocs_content_tabs.utils import ContentTabsParser


class ContentTabsPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files):
        parser = ContentTabsParser()
        return parser.parse(markdown)
