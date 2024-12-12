import xml.etree.ElementTree as ET  # noqa: N817

from ._version import get_versions


ET.register_namespace("fews", "http://www.wldelft.nl/fews")
ET.register_namespace("pi", "http://www.wldelft.nl/fews/PI")

__version__ = get_versions()["version"]
del get_versions
