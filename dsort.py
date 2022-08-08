#!/usr/bin/env python3

"""dsort sorts YAML/JSON according to a configurable preference

Usage:
  dsort.py <command> [-dhv] [<file>...]

Options:
  -d, --debug           Print debug information
  -h, --help            Show this screen.
  -v, --version         Show version.

"""
from docopt import docopt

from functools import cmp_to_key
import json
import yaml
from pprint import pprint as pp
import sys

infile_data = None

config = ['apiVersion', 'kind', 'metadata', 'name', 'namespace', 'image']
sort_lists = ['containers', 'env']

def compare(a, b):
    global config

    if a in config:
        if b in config:
            if config.index(a) < config.index(b):
                return -1
            if config.index(a) > config.index(b):
                return  1
            else:
                return 0
        else:
            return -1
    elif b in config:
        return 1
    elif a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def sort_keys(in_dict):
    global sort_lists

    keys = sorted(in_dict.keys(), key=cmp_to_key(compare))

    new_dict = {}
    for key in keys:
        v = in_dict[key]
        if isinstance(v, dict):
            v = sort_keys(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, dict):
                    new_list.append(sort_keys(item))
                else:
                    new_list.append(item)

            if key in sort_lists:
                new_list = sorted(new_list, key=lambda x: x['name'] if 'name' in x else '')
            v = new_list

        new_dict[key] = v

    return new_dict

def load_infile(infile):
    # infile_data = SortedDict()

    if infile == '-':
        infile_data = yaml.safe_load(sys.stdin)
    else:
        with open(infile, 'r', encoding='UTF-8') as file:
            infile_data = yaml.safe_load(file)

    return sort_keys(infile_data)


def main(command, infiles):

    if command not in ['json', 'yaml', 'dict']:
        print(f"Unknown command '{command}'")
        return

    for infile in infiles:
        the_data = load_infile(infile)

        # if not command:
        #    command = "yaml"

        if command == "json":
            print(json.dumps(the_data, indent=2))
        elif command == "yaml":
            print(yaml.dump(the_data, sort_keys=False))
        elif command == "dict":
            pp(the_data, sort_dicts=False)


if __name__ == '__main__':
    arguments = docopt(str(__doc__), version="0.0.1")

    if arguments['--debug']:
        print(arguments)

    infiles = arguments['<file>']
    if not infiles:
        infiles = ['-']

    main(infiles=infiles, command=arguments['<command>'])
