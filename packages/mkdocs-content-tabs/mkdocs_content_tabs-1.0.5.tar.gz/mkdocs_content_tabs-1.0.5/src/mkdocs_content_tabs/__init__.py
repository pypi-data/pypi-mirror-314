from importlib.metadata import version, PackageNotFoundError
from mkdocs_content_tabs.plugin import ContentTabsPlugin

try:
    __version__ = version("mkdocs-content-tabs")
except PackageNotFoundError:
    # package is not installed
    pass
