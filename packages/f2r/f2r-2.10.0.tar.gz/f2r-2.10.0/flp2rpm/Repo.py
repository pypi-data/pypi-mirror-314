import glob
import os
import sys
import logging

from . import config
from .helpers import run_subprocess

class Repo:

    def __init__(self):
        if not run_subprocess(['createrepo', '-h'], failOnError=False) and not config.dry_run:
            logging.error('createrepo is not installed')
            sys.exit(1)

    @staticmethod
    def create():
        logging.info('Recreating repo in %s' % config.target_rpm_dir)
        command = ['createrepo', config.target_rpm_dir]
        if config.dry_run:
            print(*command)
        else:
            run_subprocess(command)

    @staticmethod
    def validate_rpms():
        """ Validates the generated RPMs by running a dry yum install """
        # get the actual RPM paths to pass to yum and avoid subprocess using shell
        rpm_paths = glob.glob(os.path.join(config.target_rpm_dir, '*.rpm'))
        if not rpm_paths:
            logging.error("No RPMs found under %s, exiting", config.target_rpm_dir)
            return
        logging.info("Validating the RPMs under %s (will ask for sudo))", config.target_rpm_dir)
        logging.debug("RPMs: \n%s", '\n'.join(rpm_paths))
        yum_command = ['sudo', 'yum', '-y', 'install',
                      *rpm_paths,
                      '--setopt', 'tsflags=test',
                      '--setopt', 'skip_missing_names_on_install=False']
        if config.dry_run:
            print(*yum_command)
        else:
            run_subprocess(yum_command)