
"""
Module to expose more detailed version info for the installed `scikitplot`
"""
git_revision = "c299857d91d3e639b2f185a71bf10c61f314c7d6"

version = "0.4.0.post0"
__version__ = version
full_version = version
short_version = version.split("+")[0]

release = 'dev' not in version and '+' not in version
if not release:
    version = full_version
