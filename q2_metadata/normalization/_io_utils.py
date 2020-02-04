# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import yaml
import pandas as pd
import pkg_resources
from glob import glob
from os.path import basename, splitext

TEMPLATES = pkg_resources.resource_filename('q2_metadata', 'assets')


def get_rules_dict(rules: dict) -> dict:
    """
    "revert" dict to get lists of keys per value
    (i.e. metadata columns that have a rule)
    :param rules:
        Keys    : metadata columns
        Values  : rules dicts
    :return:
        Keys    : rule name
        Values  : list of metadata columns
    """
    d = {}
    for k, vs in rules.items():
        for v in vs:
            d.setdefault(v, []).append(k)
    return d


def get_rules_template() -> dict:
    """
    :return: Reference rules format structure to compare the current rule to.
    """
    rules_template_fp = os.path.join(TEMPLATES, 'rules.txt')
    with open(rules_template_fp, 'r') as f:
        rules_template = yaml.load(f, Loader=yaml.FullLoader)
    return rules_template


def get_rules(root_dir: str) -> dict:
    """
    :param root_dir:
        Directory containing the databases or rules folder
    :param md:
        Input metadata table (only the columns values are used).
    :return:
        Keys    : metadata columns
        Values  : rules dicts (from yaml to dict using yaml.load())
    """
    rules = {}
    for rule_name, rule_path in get_paths_dict(root_dir, "rules").items():
        rule = parse_yml_file(rule_path)
        rules[rule_name] = rule
    return rules


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
        path = '%s/normalization/%s/*/*.csv' % (root_dir, db_rule)
        files = glob(path)
        cur_dict = dict([fil.split('/')[-2], fil] for fil in files)
    elif db_rule == 'rules':
        path = '%s/normalization/%s/*.yml' % (root_dir, db_rule)
        files = glob(path)
        cur_dict = dict([splitext(basename(fil))[0], fil] for fil in files)
    else:
        cur_dict = {}
    return cur_dict


def check_file_existence(path: str, data: str) -> bool:
    if data == 'rule' and path.endswith('.yml'):
        return True
    elif data == 'database' and path.endswith('.csv'):
        return True
    else:
        print('Incorrect file extension %s (.yml or .csv)' % path)
        return False


def parse_yml_file(yml_path: str) -> dict:
    """
    Parse the non-comment contents of a yaml file.
    :param yml_path:
        Path to one metadata column .yml rules
    :return rule:
    """
    if not check_file_existence(yml_path, 'rule'):
        return {}

    # read the lines
    lines = []
    with open(yml_path, 'r') as f:
        for line in f:
            lines.append(line.strip())

    # open read the yaml file and skip the comment lines in the handle
    comment_lines_indices = [x for x, line in enumerate(lines) if line.startswith('#')]
    with open(yml_path, 'r') as handle:
        for comment_line in range(comment_lines_indices[-1]):
            _ = handle.readline()
        rule = yaml.load(handle, Loader=yaml.FullLoader)
    return rule


def get_databases(root_dir: str) -> dict:
    """
    :param root_dir:
        Directory containing the databases or rules folder
    :return:
        Key     : databases name
        Value   : pd.DataFrame()
    """
    databases = {}
    for db, db_path in get_paths_dict(root_dir, "databases").items():
        if not check_file_existence(db_path, 'database'):
            return {}
        database = pd.read_csv(
            db_path, header=0, sep=',', dtype=str, low_memory=False
        )
        databases[db] = database
    return databases
