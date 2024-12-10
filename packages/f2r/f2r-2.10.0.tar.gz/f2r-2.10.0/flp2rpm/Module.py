import os
import logging

from . import config
from .helpers import run_subprocess


class Module:

    # Global caches
    modules_versions: dict[tuple[str, bool], list[str]] = {}  # cache the versions : the key tuple is the name+exact_match
    modules_deps_versions: dict[tuple[str, str], list[str]] = {}  # cache the dependencies of the versions ([name,version] -> list of dependencies)

    def __init__(self, name):
        self.name = name
        os.environ["MODULEPATH"] = os.path.join(config.ali_prefix, 'sw/MODULES', config.architecture)


    def versions(self, exact_match=True) -> list[str]:
        """
        Return a list of available versions for this module.
        :param bool exact_match: Only return modules that match exactly this module's name (otherwise Python matches Python-modules).
        """
        if (self.name, exact_match) in Module.modules_versions:
            logging.debug(f"Returning cached versions for {self.name}")
            return Module.modules_versions[(self.name, exact_match)]

        available_versions = run_subprocess(['module', '-t', 'avail', self.name, '--no-pager'], forceTty=True, shell=True)
        if not isinstance(available_versions, str):  # there was an issue or there was not output, i.e. no versions
            Module.modules_versions[(self.name, exact_match)] = []
            return []

        versions = []
        for entry in (available_versions.strip().split()[1:]):
            split = entry.rsplit('/')
            # modules wrongly match prefix, e.g. Python matches Python-modules, etc..
            if split[0] != self.name and exact_match:
                continue
            versions.append(split[1])

        Module.modules_versions[(self.name, exact_match)] = versions
        return versions


    def deps(self, version) -> list[str]: # TODO rename to dependencies_list
        """ Returns the list of dependencies for the given version of this module """
        # todo give an example of the format
        if (self.name, version) in Module.modules_deps_versions:
            logging.debug(f"Returning cached dependencies and versions for {(self.name, version)}")
            return Module.modules_deps_versions[(self.name, version)]

        dependencies = []
        output = run_subprocess(['module', 'display', 'BASE/1.0', self.name + '/' + version, '--no-pager'], forceTty=True, shell=True).strip()
        for line in output.split('\n'):
            if len(line) > 1 and line.split()[0] == 'module':
                dependencies += line.split()[2:]

        Module.modules_deps_versions[(self.name, version)] = dependencies
        return dependencies


    def deps_as_dict(self, version) -> dict[str,str]: # TODO rename to dependencies_dict
        """ Returns a dictionary mapping dependencies to their versions. """
        result = {}
        dependencies = self.deps(version)
        for dep in dependencies:
            temp = dep.split('/')
            result[temp[0]] = temp[1]
        return result
