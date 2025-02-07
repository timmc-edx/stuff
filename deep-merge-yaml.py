#!/bin/python3
"""
Accepts two YAML files, deep-merges them, and formats the output
as YAML on stdout.

The second file is used to add keys to existing dicts, but not to
overwrite existing keys. List items with the same index are also
deep-merged.

Requirements:

- pip install pyyaml
"""

import sys

import yaml


def merge_dict(base, add):
    if type(add) is not dict:
        return base

    ret = {}
    # Merge all the collisions
    for shared_key in base.keys() & add.keys():
        ret[shared_key] = merge_node(base[shared_key], add[shared_key])
    # Copy the unshared items
    for base_key in base.keys() - add.keys():
        ret[base_key] = base[base_key]
    for add_key in add.keys() - base.keys():
        ret[add_key] = add[add_key]
    return ret


def merge_list(base, add):
    if type(add) is not list:
        return base

    ret = []
    for i, base_el in enumerate(base):
        if i < len(add):
            ret.append(merge_node(base_el, add[i]))
        else:
            ret.append(base_el)
    return ret


def merge_node(base, add):
    if type(base) is dict:
        return merge_dict(base, add)
    elif type(base) is list:
        return merge_list(base, add)
    else:
        return base


def main():
    (_, base, add) = sys.argv
    with open(base, 'r') as f:
        base = yaml.safe_load(f.read())
    with open(add, 'r') as f:
        add = yaml.safe_load(f.read())

    out = merge_node(base, add)
    print(yaml.dump(out))


if __name__ == '__main__':
    main()
