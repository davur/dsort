#!/usr/bin/env python3

"""dsort sorts YAML/JSON according to a configurable preference

Usage:
  dsort.py [options]

Options:
  -s, --sort-order=<keys>   Key sort preference.
  -d, --debug               Print debug information.
  -f, --file=<file>...      Path to input file [default: -].
  -h, --help                Show this screen.
  -l, --sort-lists=<lists>  Sorts lists.
  -L, --sort-all-lists      Sorts lists.
  -o, --output=<outform>    Output format (yaml or json)  [default: yaml].
  -v, --version             Show version.

"""
from docopt import docopt

from functools import cmp_to_key
import json
import yaml
from pprint import pprint as pp
import sys


class DSort:

    infile_data = None
    infiles = []

    key_sort_order = []

    sort_lists = []
    sort_all_lists = False

    def compare(self, a, b):

        if a in self.key_sort_order:
            if b in self.key_sort_order:
                if self.key_sort_order.index(a) < self.key_sort_order.index(b):
                    return -1
                if self.key_sort_order.index(a) > self.key_sort_order.index(b):
                    return  1
                else:
                    return 0
            else:
                return -1
        elif b in self.key_sort_order:
            return 1
        elif a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0


    def sort_list_cmp(self, x):
        if isinstance(x, dict):
            l = [[k, self.sort_list_cmp(x[k])] for k in x]
        elif isinstance(x, list):
            l = [self.sort_list_cmp(i) for i in x]
        else:
            l = x
        return l
    

    def sort_keys(self, in_dict):
        keys = sorted(in_dict.keys(), key=cmp_to_key(self.compare))

        new_dict = {}
        for key in keys:
            v = in_dict[key]
            if isinstance(v, dict):
                v = self.sort_keys(v)
            elif isinstance(v, list):
                new_list = []
                for item in v:
                    if isinstance(item, dict):
                        new_list.append(self.sort_keys(item))
                    else:
                        new_list.append(item)

                if self.sort_all_lists or key in self.sort_lists: 
                    # new_list = sorted(new_list, key=lambda x: x['name'] if 'name' in x else '')
                    new_list = sorted(new_list, key=self.sort_list_cmp)
                v = new_list

            new_dict[key] = v

        return new_dict

    def load_infile(self, infile):
        if infile == '-':
            infile_data = yaml.safe_load(sys.stdin)
        else:
            with open(infile, 'r', encoding='UTF-8') as file:
                infile_data = yaml.safe_load(file)

        return self.sort_keys(infile_data)


    def main(self, outform):

        if outform not in ['json', 'yaml', 'dict']:
            print(f"Unknown output format '{outform}'")
            return

        for infile in self.infiles:
            the_data = self.load_infile(infile)

            if outform == "json":
                print(json.dumps(the_data, indent=2))
            elif outform == "yaml":
                print(yaml.dump(the_data, sort_keys=False))
            elif outform == "dict":
                pp(the_data, sort_dicts=False)


if __name__ == '__main__':
    arguments = docopt(str(__doc__), version="0.0.1")

    dsort = DSort()
    
    if arguments['--debug']:
        print(arguments)

    if arguments['--sort-lists']:
        dsort.sort_lists = arguments['--sort-lists'].split(',')

    if arguments['--sort-all-lists']:
        dsort.sort_all_lists = True

    dsort.infiles = [arguments['--file']]

    if arguments['--sort-order']:
        dsort.key_sort_order = arguments['--sort-order'].split(',')

    dsort.main(outform=arguments['--output'])
