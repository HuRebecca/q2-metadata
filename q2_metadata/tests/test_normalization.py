# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest
from pandas.testing import assert_frame_equal
import pandas as pd

from os.path import abspath, dirname, exists
from q2_metadata._normalize import (
    get_paths_dict,
    parse_yml_file,
    get_paths,
    get_rules,
    get_databases
)



#class NormalizationMetadataHandling(unittest.TestCase):

#    def setUp(self) -> None:
#        self.md = pd.DataFrame(
#            {
#                'col1': ['1', '2', np.nan],
#                'col2': ['A', 'B', np.nan],
#                'col3': [1.0, 2.0, 3.0],
#            }
#        )
#        self.rules = {
#            'col1': {}
#        }

#    def test_(self):
#         = (self.rules_dict)
#        self.assertEqual()




class NormalizationInputTests(unittest.TestCase):

    def setUp(self) -> None:
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
        # print("self.databases_dict", self.databases_dict)
        # print("self.rules_dict", self.rules_dict)

    def test_get_paths_dict(self):
        test_db_dict = get_paths_dict(self.root, "databases")
        self.assertEqual(test_db_dict, self.databases_dict)
        test_rules_dict = get_paths_dict(self.root, "rules")
        self.assertEqual(test_rules_dict, self.rules_dict)
        test_nothing_dict = get_paths_dict(self.root, "nothing")
        self.assertFalse(test_nothing_dict)

    def test_get_paths(self):
        # print("self.root", self.root)
        test_dicts = get_paths(self.root)
        # print("test_dicts", test_dicts)
        self.assertEqual(test_dicts, (self.databases_dict, self.rules_dict))

    def test_parse_yml_file(self):
        self.assertTrue(exists(self.rules_dict['dummy_rule']))
        test_rule = parse_yml_file(self.rules_dict['dummy_rule'])
        self.assertEqual(test_rule, {'rule1': 'dont'})

    def test_get_rules(self):
        test_rules = get_rules(self.rules_dict)
        self.assertEqual(test_rules, {'dummy_rule': {'rule1': 'dont'}})

    def test_get_databases(self):
        test_databases = get_databases(self.databases_dict)
        for db_key, test_database in test_databases.items():
            assert_frame_equal(test_database, self.dummy_db[db_key])


if __name__ == '__main__':
    unittest.main()
