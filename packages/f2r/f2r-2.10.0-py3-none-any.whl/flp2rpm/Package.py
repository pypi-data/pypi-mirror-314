import os
import re

from . import config
from .Defaults import Defaults
from .Module import Module
from .helpers import parse_recipe_header


class Package:
    """ Represents a package in alidist, i.e. 1 script
     The recipe is used to know the dependencies, and the build dependencies.
     (The versions of the dependencies are based on the modules.)"""

    def __init__(self, name, version):
        self.name = name
        self.path = os.path.join(config.ali_prefix, 'alidist', name.lower() + '.sh')

        parsed = parse_recipe_header(str(self.path))
        self.requires = parsed['requires'] if 'requires' in parsed.keys() else []

        self.defaults = Defaults()
        if self.defaults is not None and self.defaults.overrides is not None and self.name in self.defaults.overrides.keys() and 'requires' in self.defaults.overrides[self.name].keys(): # todo what is the proper way of expressing this ?
            defaults_deps = self.defaults.overrides[self.name]['requires']
            self.requires = defaults_deps

        self.devel = parsed['build_requires'] if 'build_requires' in parsed.keys() else []
        self.version = parsed['version'] 
        self.tag = parsed['tag'] if 'tag' in parsed else parsed['version']
        self.module_version = version
        self.module_dep_versions = Module(name).deps_as_dict(version)


    def __str__(self):
        return f"package {self.name}: \nRequires: {self.requires}\nDevel: {self.devel}\nTag: {self.tag}\nVersion: {self.version}"

    def filter_dependencies(self, deps):
        """ Filters the provided deps to keep the ones matching the correct architecture and defaults """
        filtered = []
        # Filter on arch
        for dep in deps:
            filters = dep.split(':')
            if len(filters) == 2:
                x = re.match(filters[1], config.architecture)
                if x and filters[0]:
                    filtered.append(filters[0])
            else:
                filtered.append(dep)
        # Filter on disable from defaults
        if self.defaults is not None:
            return [x for x in filtered if x not in self.defaults.disable]
        return filtered

    def deps_with_versions(self) -> dict[str,str]:
        """
        Returns a dictionary matching the dependencies with their versions using the information from the modules.
        In case we don't find the dependency in the modules, then we consider that it comes from the system and return `from_system` for this dependency.
        """
        result = {}
        deps = self.filter_dependencies(self.requires)

        for dep in deps:
            if dep in self.module_dep_versions.keys():
                result[dep] = self.module_dep_versions[dep]
            else:
                result[dep] = 'from_system'  # If not found in the module's dependencies then we conclude that it is a system dependency.
        return result

    def get_extra_deps(self):
        """ Provide extran deps list coming from alidist recipe """
        with open(self.path) as recipe:
            content = recipe.read()
            found = re.search(r'cat ' + re.escape('> $INSTALLROOT/.rpm-extra-deps <<') + 'EoF\n.*?EoF', content, re.DOTALL)
            if found is not None:
                return found.group().split('\n')[1:-1]
        return []

    def get_devel_deps(self):
        deps = self.filter_dependencies(self.devel)
        if 'alibuild-recipe-tools' in deps:
            deps.remove('alibuild-recipe-tools')
        return deps

    def get_devel_deps_with_versions(self):
        result = {}
        deps = self.get_devel_deps()
        for dep in deps:
            avail = Module(dep).versions()
            avail_filter = list(filter(lambda ver: ver.find('latest'), avail))
            # if there is a version name that contains "latest" then we use the first one, otherwise from system.
            if not avail:
                result[dep] = 'from_system'
            else:
                result[dep] = avail_filter.pop()
        return result
