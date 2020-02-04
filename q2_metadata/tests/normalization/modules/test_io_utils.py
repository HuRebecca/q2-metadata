# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

from os.path import abspath, dirname, exists
from pandas.testing import assert_frame_equal
import pandas as pd

from q2_metadata.normalization._io_utils import (
    get_rules_template,
    get_paths_dict,
    parse_yml_file,
    get_rules_dict,
    get_rules,
    get_databases
)


class NormalizationInputTests(unittest.TestCase):
    def setUp(self):
        self.root = '%s/normalization' % dirname(abspath(__file__))
        self.rules_dict = {
            'dummy_rule': '%s/rules/dummy_rule.yml' % self.root
        }
        self.databases_dict = {
            'dummy_db': '%s/databases/dummy_db/dummy_db.csv' % self.root
        }
        self.dummy_db = {'dummy_db': pd.DataFrame(
            {'entry': ['entry1', 'entry2'],
            'data': ['data1', 'data2']}
        )}
        self.template_dict = {
            'blank,txt': ['not applicable',
                        'not collected',
                        'not provided',
                        'restricted access'],
            'expected,type': ['str', 'list'],
            'format,txt': ['bool', 'float', 'int', 'str'],
            'missing,txt': ['not applicable',
                          'not collected',
                          'not provided',
                          'restricted access'],
            'normalization,dict': {'gated_value,txt': ['Out of bounds'],
                                 'maximum,type': ['int', 'float'],
                                 'minimum,type': ['int', 'float'],
                                 'no range applicable,bool': 1},
            'remap,dict': {'str': 'str'},
            'validation,dict': {'force_to_blank_if,dict': {'is null,txt': ['variable']},
                              'check ontology,bool': 1,
                              'flag typos,bool': 1,
                              'must exist,bool': 1}}

    def test_get_rules_template(self):
        rules_template = get_rules_template()
        self.assertEqual(rules_template, self.template_dict)

    def test_get_paths_dict(self):
        test_db_dict = get_paths_dict(self.root, "databases")
        self.assertEqual(test_db_dict, self.databases_dict)
        test_rules_dict = get_paths_dict(self.root, "rules")
        self.assertEqual(test_rules_dict, self.rules_dict)
        test_nothing_dict = get_paths_dict(self.root, "nothing")
        self.assertEqual(test_nothing_dict, {})

    def test_parse_yml_file(self):
        self.assertTrue(exists(self.rules_dict['dummy_rule']))
        test_rule = parse_yml_file(self.rules_dict['dummy_rule'])
        self.assertEqual(test_rule, {'rule1': 'dont'})

    def test_collect_columns_per_rule_key(self):
        rev_dict = get_rules_dict({'A': [1,2,3], 'B': [2,3,4]})
        self.assertEqual(rev_dict, {1: ['A'], 2: ['A','B'], 3: ['A','B'], 4: ['B']})

    def test_get_rules(self):
        test_rules = get_rules(self.rules_dict)
        self.assertEqual(test_rules, {'dummy_rule': {'rule1': 'dont'}})

    def test_get_databases(self):
        test_databases = get_databases(self.root)
        for db_key, test_database in test_databases.items():
            assert_frame_equal(test_database, self.dummy_db[db_key])


if __name__ == '__main__':
    unittest.main()
