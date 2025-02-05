"""
Accepts YAML on stdin and prints redacted YAML to stdout.

Scalars are mapped to fixed sample values ("hello", True, and
5). Encrypted values become the string '[encrypted]'.

Requirements:

- pip install pyyaml
"""

import sys

import yaml


class Encrypted():
    pass

def _encrypted_constructor(loader, node):
    return Encrypted()

def redact_node(node):
    t = type(node)
    if t is int:
        return 5
    elif t is float:
        return 9.7
    elif t is str:
        return "hello"
    elif t is bool:
        return True
    elif t is dict:
        return {k: redact_node(v) for k, v in node.items()}
    elif t is list:
        return [redact_node(v) for v in node]
    elif node is None:
        return None
    elif t is Encrypted:
        return "[encrypted]"
    else:
        raise Exception(f"Unexpected type {t}: {node}")

def main():
    yaml.SafeLoader.add_constructor('!Encrypted', _encrypted_constructor)
    tree = yaml.safe_load(sys.stdin.read())
    tree = redact_node(tree)
    print(yaml.dump(tree))


if __name__ == '__main__':
    main()
