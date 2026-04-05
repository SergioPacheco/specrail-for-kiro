"""KiroRails — Professional-grade delivery for AI-assisted development."""

try:
    from importlib.metadata import version
    __version__ = version("kirorails")
except Exception:
    __version__ = "0.0.0"
