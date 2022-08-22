#!/usr/bin/env python3

"""dsort sorts YAML/JSON according to a configurable preference

Usage:
  dsort.py [options]

Options:
  -s, --sort-order=<keys>  Key sort preference.
  -d, --debug              Print debug information.
  -f, --file=<file>...     Path to input file [default: -].
  -h, --help               Show this screen.
  -l, --sort-lists         Sorts lists.
  -o, --output=<outform>   Output format (yaml or json)  [default: yaml].
  -v, --version            Show version.

"""
from docopt import docopt

from functools import cmp_to_key
import json
import yaml
from pprint import pprint as pp
import sys

infile_data = None

key_sort_order = []

sort_lists = False

def compare(a, b):
    global key_sort_order

    if a in key_sort_order:
        if b in key_sort_order:
            if key_sort_order.index(a) < key_sort_order.index(b):
                return -1
            if key_sort_order.index(a) > key_sort_order.index(b):
                return  1
            else:
                return 0
        else:
            return -1
    elif b in key_sort_order:
        return 1
    elif a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def sort_list_cmp(x):
    if isinstance(x, dict):
        l = [[k, sort_list_cmp(x[k])] for k in x]
    elif isinstance(x, list):
        l = [sort_list_cmp(i) for i in x]
    else:
        l = x
    return l
    

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

            if sort_lists: # key in sort_lists:
                # new_list = sorted(new_list, key=lambda x: x['name'] if 'name' in x else '')
                new_list = sorted(new_list, key=sort_list_cmp)
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


def main(outform, infiles):

    if outform not in ['json', 'yaml', 'dict']:
        print(f"Unknown output format '{outform}'")
        return

    for infile in infiles:
        the_data = load_infile(infile)

        if outform == "json":
            print(json.dumps(the_data, indent=2))
        elif outform == "yaml":
            print(yaml.dump(the_data, sort_keys=False))
        elif outform == "dict":
            pp(the_data, sort_dicts=False)


if __name__ == '__main__':
    arguments = docopt(str(__doc__), version="0.0.1")
    
    if arguments['--debug']:
        print(arguments)

    if arguments['--sort-lists']:
        sort_lists = True

    infiles = arguments['--file']
    key_sort_order = arguments['--sort-order'].split(',')

    main(infiles=infiles, outform=arguments['--output'])
