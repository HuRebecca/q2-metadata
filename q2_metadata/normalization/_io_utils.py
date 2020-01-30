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

from ._rules_format import traverse_rules

TEMPLATES = pkg_resources.resource_filename('q2_metadata', 'assets')


def collect_columns_per_rule_key(rules: dict) -> dict:
    """
    :param rules:
        Keys    : metadata columns
        Values  : rules dicts
    :return:
        Keys    : rule name
        Values  : list of metadata columns
    """
    all_rule_names = {}
    for col, rule in rules.items():
        for rule_key in rule:
            all_rule_names.setdefault(rule_key, []).append(col)
    return all_rule_names


def get_rules_dict(rules: dict) -> dict:
    """
    :param rules:
        Keys    : metadata columns
        Values  : rules dicts
    :return:
        Keys    : rule name
        Values  : possible values for the rule
    """
    # "revert" dict to get lists of keys per value (i.e. metadata columns that have a rule)
    columns_per_rule_key = collect_columns_per_rule_key(rules)
    return columns_per_rule_key


def get_rules_template() -> dict:
    """
    :return: Reference rules format structure to compare the current rule to.
    """
    rules_template_fp = os.path.join(TEMPLATES, 'rules.txt')
    with open(rules_template_fp, 'r') as f:
        rules_template = yaml.load(f, Loader=yaml.FullLoader)
    return rules_template


def get_rules(root_dir: str, md: pd.DataFrame) -> (dict, dict):
    """
    :param root_dir:
        Directory containing the databases or rules folder
    :param md:
        Input metadata table (only the columns values are used).
    :return:
        Keys    : metadata columns
        Values  : rules dicts (from yaml to dict using yaml.load())
    """
    # get per-column info
    # columns_info_fp = '%s/databases/defaults/columns_info.tsv' % root_dir
    # columns_info = pd.read_csv(columns_info_fp, header=0, sep='\t')

    rules_template = get_rules_template()

    rules = {}
    issues = []
    for col, rule_path in get_paths_dict(root_dir, "rules").items():
        rule = parse_yml_file(rule_path)
        rules[col] = rule
        # check that the passed rules are in correct format and types
        issues = traverse_rules(col, rule, rules_template, issues, md)
    rules_dict = get_rules_dict(rules)
    return rules, rules_dict, issues


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
        paths = glob('%s/normalization/%s/*/*.csv' % (root_dir, db_rule))
        cur_dict = dict([path.split('/')[-2], path] for path in paths)
    elif db_rule == 'rules':
        paths = glob('%s/normalization/%s/*.yml' % (root_dir, db_rule))
        cur_dict = dict([splitext(basename(path))[0], path] for path in paths)
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
