# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import yaml
import pandas as pd
from glob import glob
from os.path import abspath, basename, dirname, isfile, splitext
import qiime2 as q2


# annotate how types are expected to be passed to the function
# (explicit declare that first arg should be metadata class)
def normalize(metadata: q2.Metadata) -> q2.Metadata:
    """
    :param metadata:
        Input metadata file
    :return:
        A curated metadata table.
    """
    # Get hard-coded but possible user-modified data from the "databases" and "rules" folders
    root_dir = dirname(abspath(__file__))
    databases_paths, rules_paths = get_paths(root_dir)
    rules = get_rules(rules_paths)
    databases = get_databases(databases_paths)

    md = metadata.to_dataframe()

    # md_out = normalize()

    # only during dev so that the function return something :)
    md_out = pd.DataFrame({
        'sampleid': ['A', 'B'],
        'col1': ['1', '2'],
        'col2': ['3', '4']
    }).set_index('sampleid')
    return q2.Metadata(md_out)


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


def get_databases(db_paths: dict) -> dict:
    """
    :param db_paths:
        Key     : databases name
        Value   : paths to .csv database
    :return:
        Key     : databases name
        Value   : pd.DataFrame()
    """
    databases = {}
    for db, db_path in db_paths.items():
        if not check_file_existence(db_path, 'database'):
            return {}
        database = pd.read_csv(
            db_path, header=0, sep=',', dtype=str, low_memory=False
        )
        databases[db] = database
    return databases


def get_rules(rules_paths: dict) -> dict:
    """
    Collect the
    :param rules_paths:
        Keys    : metadata columns
        Values  : path to the yaml file rules
    :return:
        Keys    : metadata columns
        Values  : rules dicts (from yaml to dict using yaml.load())
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
