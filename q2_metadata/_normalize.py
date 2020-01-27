# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import sys
import yaml
from glob import glob
from os.path import abspath, basename, dirname, splitext
import qiime2 as q2


# annotate how types are expected to be passed to the function
# (explicit declare that first arg should be metadata class)
def normalize(metadata: q2.Metadata) -> None:
    # def normalize(metadata: q2.Metadata) -> q2.Metadata:
    """
    :param metadata:
        A non-curated metadata table.
    :return:
        A curated metadata table.
    """

    # Get hard-coded but possible user-modified data from the "databases" and "rules" folders
    root_dir = dirname(abspath(__file__))
    print('root_dir:', root_dir)
    databases_paths, rules_paths = get_paths(root_dir)

    rules = get_rules(rules_paths)
    print(rules)

#    return q2.Metadata()


def parse_yml_file(yml_path: str) -> dict:
    """
    Parse the non-comment contents of a yaml file.
    :param yml_path:
        Path to one metadata column .yml rules
    :return:
    """
    # read the lines
    lines = [x.strip() for x in open(yml_path, 'rU').readlines()]
    comment_lines_indices = [idx for idx, x in enumerate(lines) if x[0] == '#']

    # open read the yaml file and skip the comment lines in the handle
    with open(yml_path) as handle:
        for comment_line in range(comment_lines_indices[-1]):
            _ = handle.readline()
        rule = yaml.load(handle)
    return rule


def get_rules(rules_paths: dict) -> dict:
    """
    Collect the
    :param rules_paths:
    :return:
    """
    rules = {}
    for col, rule_path in rules_paths.items():
        rule = parse_yml_file(rule_path)
    rules[col] = rule
    return rules


def get_paths(root_dir: str) -> (dict, dict):
    """
    Get the path to the databases of ontology terms
    and per-metadata column yaml rules files ad
    :param root_dir:
        Directory containing the databases or rules folder
    :return:
        First dict is for the databases paths (values) per database (key)
        Second dict is for the rules paths (values) per metadata column (key)
    """
    databases_paths = get_paths_dict(root_dir, "databases")
    rules_paths = get_paths_dict(root_dir, "rules")
    return databases_paths, rules_paths


def get_paths_dict(root_dir: str, db_rule: str) -> dict:
    """
    :param root_dir:
        Directory containing the databases or rules folder
    :param db_rule:
        "databases" if key is the folder
        "rules" if key is in the file name
    :return: file paths as values per database/rule as key
    """
    if db_rule == 'databases':
        paths = glob('%s/%s/*/*.csv' % (root_dir, db_rule))
        cur_dict = dict([path.split('/')[-2], path] for path in paths)
    elif db_rule == 'rules':
        paths = glob('%s/%s/*.yml' % (root_dir, db_rule))
        cur_dict = dict([splitext(basename(path))[0], path] for path in paths)
    else:
        cur_dict = {}
    return cur_dict
