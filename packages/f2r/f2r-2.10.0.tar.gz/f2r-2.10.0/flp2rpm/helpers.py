import logging
import subprocess
import sys

import yaml

cache_recipe_header: dict[str, any] = {}  # cache the recipe headers

def parse_recipe_header(path: str):
    """ Parses header of alidist recipe"""
    global cache_recipe_header
    if path in cache_recipe_header:
        logging.debug(f"Using cached recipe header: {path}")
        return cache_recipe_header[path]

    # take only the header from the recipe
    header_string = ''
    with open(path, 'r') as file:
        for line in iter(lambda: file.readline().rstrip(), '---'):
            header_string += line + '\n'

    result = yaml.safe_load(header_string)
    cache_recipe_header[path] = result
    return result


def load_yaml_from_file(path: str):
    """ Parses a yaml list into a dict """
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def run_subprocess(command : list[str], **flags):
    """ Run a subprocess and returns the output
        In case of exception we exit if failOnError is set to true.
        We return the output if it succeeded and is not empty, False if it failed, True if output is empty. TODO: this is weird.
        :param command: command to run as a list
        :param flags: extra flags to pass to `subprocess.check_output`. Two extra params are accepted : failOnError and forceTty.
    """
    # TODO consider having dedicated function parameters for tty and failOnError
    #  rather than hijacking the flags that are aimed to subprocess.check_output
    options = {
        'failOnError': True,
        'forceTty': False
    }
    for option in options:
        if option in flags:
            options[option] = flags[option]
            del flags[option]
    if options['forceTty']:
        # TODO why do we use `script` ??? that certainly is not necessary
        command = ["script -q -e -c '" + ' '.join(command) + "'"] # TODO that does not work on Mac (and we develop on mac)

    try:
        logging.debug('Running as subprocess: %s' % (subprocess.list2cmdline(command)))
        output = subprocess.check_output(command, **flags).strip()
        if type(output) != str:
            output = output.decode('ascii')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        output = e.output
        if type(output) != str:
            output = output.decode('ascii')
        if 'File already exists' in output:
            # TODO this very specific case should probably not be here, the method is generic
            logging.warning('The RPM already exists, continuing...')
        else:
            logging.error(output)
            logging.error(e)
            if options['failOnError']:
                logging.critical('Exiting...')
                sys.exit(1)
            else:
                return False
    if len(output) < 1:
        return True
    return output


def strip_dashes(version: str) -> str:
    """ Replaces all dashes with underscore, except last one """
    if version.count('-') > 1:
        version_split = version.split('-')
        release = version_split.pop()
        return '_'.join(version_split) + '-' + release
    else:
        return version