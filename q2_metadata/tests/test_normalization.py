# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import os
import tempfile

import pandas as pd
import numpy as np
import qiime2

from os.path import abspath, dirname
from q2_metadata._normalize import (
    get_paths_dict,
    parse_yml_file,
    get_paths,
    get_rules
)


class NormalizationInputTests(unittest.TestCase):

    def setUp(self) -> None:
        self.root = '%s/normalization' % dirname(abspath(__file__))
        self.databases_dict = {
            'dummy_db': '%s/databases/dummy_db/dummy_db.csv' % self.root
        }
        self.rules_dict = {
            'dummy_rule': '%s/rules/dummy_rule.yml' % self.root
        }
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
        test_rule = parse_yml_file(self.rules_dict['dummy_rule'])
        self.assertEqual(test_rule, {'rule1': 'dont'})

    def test_get_rules(self):
        test_rules = get_rules(self.rules_dict)
        self.assertEqual(test_rules, {'dummy_rule': {'rule1': 'dont'}})


if __name__ == '__main__':
    unittest.main()
