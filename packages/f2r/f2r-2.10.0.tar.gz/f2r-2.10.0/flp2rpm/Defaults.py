import os

from . import config # TODO this makes it impossible to overwrite from a test.
from .helpers import parse_recipe_header


class Defaults:
    """
    Class representing a default in alidist.
    TODO once we fix the "config" we must write a test for it.
    """
    def __init__(self, name='o2-dataflow'):
        self.name = name
        filename = 'defaults-%s.sh' % name
        self.path = os.path.join(config.ali_prefix, 'alidist', filename)
        parsed_header = parse_recipe_header(self.path)
        self.disableRaw = parsed_header['disable']
        self.disableException = ["curl", "OpenSSL"]
        self.disable = [x for x in self.disableRaw if x not in self.disableException]
        self.overrides = parsed_header['overrides']
