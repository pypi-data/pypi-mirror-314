import logging
import os
import re
import sys

from . import config
from .helpers import load_yaml_from_file, strip_dashes
from .helpers import run_subprocess


class Fpm:
    """
    Class to handle fpm invocations.

    We use extra files called "[runtime|devel].[osrelease].yaml" to know how to translate the system dependencies into actual RPM dependencies.
    """

    def __init__(self):
        self.buildDir = os.path.join(config.ali_prefix, 'sw', config.architecture)
        self.forceBuild = ['--force'] if config.force_build else []
        self.packagePrefix = "o2-"
        self.targetDir = config.target_rpm_dir
        self.skipDeps = ['openmp', 'VecGeom', 'O2-customization']  # as sometimes there's mismatch between "requires" deps and modulefile

        # Create output dir
        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)

        arch_split = config.architecture.split('_')
        self.architecture = arch_split[1].replace('-', '_')
        self.release_suffix = arch_split[0]

        self.runtimeDepsDict = load_yaml_from_file(str(os.path.join(config.work_dir, 'runtime.' + self.release_suffix + '.yaml')))
        self.develDepsDict = load_yaml_from_file(str(os.path.join(config.work_dir, 'devel.' + self.release_suffix + '.yaml')))

        if config.tag_version:
            self.release_suffix += '_' + config.release_tag.replace('/', '_')

    def run(self, name, version, deps, devel_deps, extra_deps, rpms_generated: list[str]=None):
        """ Prepares arguments and executes fpm """
        if rpms_generated is None:
            rpms_generated = []
        logging.debug(f"Running FPM on {name} {version}")
        full_version = version
        version = version.replace('local', '', 1)
        # Handle not standard versions, nightly, latest-o2-dataflow
        if 'latest' in version:
            iteration_arg = ['--iteration', self.release_suffix]
        elif version.count('-') > 1:
            version_split = version.split('-')
            iteration_arg = ['--iteration', version_split.pop() + '.' + self.release_suffix]
            if name == 'O2' and (version_split[0] == 'daily' or version_split[0] == 'nightly' or version_split[0] == 'epn'):
                version_split.pop(0)
            version = '_'.join(version_split)
        else:
            version_split = version.split('-', 1)
            version = version_split[0]
            iteration_arg = ['--iteration', version_split[1].replace('-', '_') + '.' + self.release_suffix]

        rpm_type = 'dir'
        # prep dir arguments
        # `=.` is necessary so that the complete source dir path
        # is not replicated and the target dir consists of only
        # prefix + package name + dir
        package_dir = self.buildDir + "/" + name + "/" + full_version + "/"
        sub_dirs = ['bin', 'lib', 'lib64', 'etc', 'include', 'bin-safe', 'libexec', 'WebDID', 'share', 'plugins', 'cmake', 'sbin', 'icons', 'fonts',
                    'response']
        paths = []
        for subdir in sub_dirs:
            if os.path.exists(package_dir + subdir):
                if subdir == 'etc' and os.listdir(package_dir + subdir) == ['modulefiles', 'profile.d']:
                    continue
                # This is an ugly fix to a temporary problem. (OCONF-799)
                # The lib64 symlink to lib in the Python-modules causes issues with fpm.
                if name == 'Python-modules' and subdir == 'lib64' and os.path.islink(package_dir + subdir):
                    continue
                if name == 'Python-modules' and subdir == 'lib':
                    continue
                if name == 'Python-modules' and subdir == 'bin':
                    continue

                paths.append(package_dir + subdir + '=.')

        # if there are not dirs change RPM type to 'empty'
        if not paths:
            rpm_type = 'empty'

        logging.info('Processing %s version %s:\n' \
                     ' - deps: %s\n - extra deps: %s\n - devel deps: %s\n' \
                     % (name, version, list(deps.items()), extra_deps, list({**devel_deps, **self.convert_deps_to_devel(deps)}.items())))

        # Handle extra_deps
        extra_deps = [v for dep in extra_deps for v in ('--depends', dep.replace('local', '', 1))]

        # Handle install_path
        install_path = '/opt/o2/'
        if name == 'mesos':
            install_path = '/usr/'

        package_name = self.packagePrefix + name
        fpm_command = ['fpm',
                      '-s', rpm_type,
                      '-t', 'rpm',
                      '--log', 'warn',
                      *self.translate_deps_to_args(deps),
                      *extra_deps,
                      *self.forceBuild,
                      '-p', self.targetDir,
                      '--architecture', self.architecture,
                      '--prefix', install_path,
                      '-n', package_name,
                      '--version', version,
                      *iteration_arg,
                      '--no-rpm-auto-add-directories',
                      '--rpm-compression', 'xzmt',
                      '--template-scripts',
                      '--after-install', os.path.join(config.work_dir, 'after_install_template.sh'),
                      '--after-remove', os.path.join(config.work_dir, 'after_remove_template.sh'),
                      '--vendor', 'ALICE FLP',
                      '--url', 'https://alice-flp.docs.cern.ch',
                      '--maintainer', 'Barthelemy von Haller <bvonhall@cern.ch>',
                      '--license', 'GPL-3.0']

        # This is an ugly fix (OCONF-799)
        # We need to make sure we survive the python-modules duplicated python binaries.
        if name == 'Python-modules':
            fpm_command.extend(['--rpm-tag', '%define _build_id_links none', "--rpm-tag", '%undefine _missing_build_ids_terminate_build'])

        if paths:
            fpm_command.extend(['--exclude=*/modulefiles', '--exclude=*/profile.d', '--exclude=*/info/dir', '--exclude=*/version'])
            fpm_command.extend(paths)

        devel_package_name = package_name + '-devel'
        fpm_command_devel = ['fpm',
                             '-s', 'empty',
                             '-t', 'rpm',
                             '--log', 'warn',
                             '--architecture', self.architecture,
                             '--prefix', '/opt/o2/',
                             '-n', devel_package_name,
                             '--version', version,
                             '-p', self.targetDir,
                             *iteration_arg,
                             '--template-scripts',
                             '--rpm-compression', 'xz',
                             '--after-install', os.path.join(config.work_dir, 'after_install_template.sh'),
                             '--after-remove', os.path.join(config.work_dir, 'after_remove_template.sh'),
                             *self.translate_devel_deps_to_args(deps),
                             *self.translate_devel_deps_to_args(devel_deps),
                             *self.translate_deps_to_args(self.convert_deps_to_devel(deps))
                             ]

        if not config.dry_run:
            self.generate_rpm(package_name, fpm_command, rpms_generated)
            if config.devel:
                self.generate_rpm(devel_package_name, fpm_command_devel, rpms_generated)
        else:
            print(*fpm_command)
            if config.devel:
                print(*fpm_command_devel)
            return ''

    def convert_deps_to_devel(self, deps: dict[str,str]) -> dict[str,str]:
        """
        Transform the provided dependencies into devel dependencies: remove system deps and append `-devel` to the name of the remaining ones.
        """
        return {name + '-devel': version for name, version in deps.items() if version != 'from_system'}

    # Run subprocess to generate RPM
    def generate_rpm(self, name: str, command: list[str], rpms_generated: list[str]):
        logging.info('Generating RPM: %s', name)
        ret = run_subprocess(command, failOnError=False)
        if not ret:
            logging.warning('Generation of the RPM skipped')
        else:
            # try to parse the generated RPM path from the fpm output
            match = re.search(':path=>\"(.*)\"}', ret)
            generated_rpm_path = match.group(1) if match else ''
            rpms_generated.append(generated_rpm_path)

    # Convert map name:version to fpm compatible command line params
    def translate_devel_deps_to_args(self, deps):
        deps_arg = []
        for name, version in deps.items():
            if name not in self.skipDeps:
                if name in self.develDepsDict:
                    for dep in self.develDepsDict.get(name):
                        deps_arg.extend(['--depends', dep])
                else:
                    deps_arg.extend(['--depends', self.packagePrefix + name])
        return deps_arg

    # Convert map name:version to fpm compatible command line params
    def translate_deps_to_args(self, deps) -> list[str]:
        """ Prepares dependency arguments for fpm """
        deps_arg = []
        for depName, dep_version in deps.items():
            if depName not in self.skipDeps:
                if dep_version != "from_system":
                    dep_version = dep_version.replace('local', '', 1)  # TODO why ?
                    dep_version = strip_dashes(dep_version)

                    # Handle "nightly", "daily" prefixes in O2
                    if depName == 'O2':
                        version_split = dep_version.split('_')
                        if version_split[0] == 'daily' or version_split[0] == 'nightly' or version_split[0] == 'epn':
                            version_split.pop(0)
                            dep_version = '_'.join(version_split)

                    deps_arg.extend(['--depends', self.packagePrefix + depName + ' >= ' + dep_version])
                else:  # coming from system, get name from dict
                    if depName not in self.runtimeDepsDict:
                        logging.critical('Could not find system dependency: %s \nDoes it suppose to come from aliBuild?' % depName)
                        sys.exit(1)
                    for dep in self.runtimeDepsDict.get(depName):
                        deps_arg.extend(['--depends', dep])
        return deps_arg
