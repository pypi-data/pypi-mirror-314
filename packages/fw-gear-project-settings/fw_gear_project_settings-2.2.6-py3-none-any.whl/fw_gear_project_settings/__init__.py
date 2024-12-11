"""The fw_gear_project_settings package."""

from importlib.metadata import version

try:
    __version__ = version(__package__)
except:  # noqa: E722
    pass
