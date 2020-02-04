# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import pandas as pd
import numpy as np

from q2_metadata.normalization._check_rules_format import (
    get_rules_template_keys,
    check_rule_in_temp,
    check_var_in_metadata,
    check_str_in_dictionary,
    check_list_in_dictionary,
    check_val_type,
    traverse_rules
)


class NormalizationCheckRulesFormat(unittest.TestCase):
    def setUp(self):
        self.md = pd.DataFrame({'col1': ['1', '2', np.nan],
                                'col2': ['A', 'B', np.nan],
                                'col3': [1.0, 2.0, 3.0]})
        self.rules_template = {'rule1,txt': 1,
                               'rule2,type': {'nothing': ['else', 'matters']}}

    def test_get_rules_template_keys(self):
        rules_template_keys = get_rules_template_keys(self.rules_template)
        self.assertEqual(rules_template_keys, {'rule1': ['rule1,txt', 'txt'],
                                               'rule2': ['rule2,type', 'type']})

    def test_check_val_type(self):
        val_type = check_val_type([1,2], ['list', 'str'], 'x', 'y')
        self.assertEqual(val_type, '')
        val_type = check_val_type('whatever', ['list', 'str'], 'x', 'y')
        self.assertEqual(val_type, '')
        error_expected = 'value(s) to rule "x" of "y" not of expected type'
        val_type = check_val_type('whatever', ['dict', 'list'], 'x', 'y')
        self.assertEqual(val_type, error_expected)
        val_type = check_val_type([1,2], ['dict', 'str'], 'x', 'y')
        self.assertEqual(val_type, error_expected)

    def test_check_list_in_dictionary(self):
        list_in_dictionary = check_list_in_dictionary(['a'], ['a', 'b'], 'x', 'y')
        self.assertEqual(list_in_dictionary, '')
        list_in_dictionary = check_list_in_dictionary(['A'], ['a', 'b'], 'x', 'y')
        self.assertEqual(list_in_dictionary, '')
        error_expected = 'value(s) to rule "x" of "y" not in reference'
        list_in_dictionary = check_list_in_dictionary(['a'], ['b'], 'x', 'y')
        self.assertEqual(list_in_dictionary, error_expected)

    def test_check_str_in_dictionary(self):
        str_in_dictionary = check_str_in_dictionary('a', ['a', 'b'], 'x', 'y')
        self.assertEqual(str_in_dictionary, '')
        str_in_dictionary = check_str_in_dictionary('A', ['a', 'b'], 'x', 'y')
        self.assertEqual(str_in_dictionary, '')
        error_expected = 'value(s) to rule "x" of "y" not in reference'
        str_in_dictionary = check_str_in_dictionary('a', ['b'], 'x', 'y')
        self.assertEqual(str_in_dictionary, error_expected)

    def test_check_var_in_metadata(self):
        var_in_metadata = check_var_in_metadata(['col1', 'col2'], self.md, 'x', 'y')
        self.assertEqual(var_in_metadata, '')
        var_in_metadata = check_var_in_metadata(['COL1'], self.md, 'x', 'y')
        self.assertEqual(var_in_metadata, '')
        error_expected = 'variable(s) to rule "x" of "y" not in metadata'
        var_in_metadata = check_var_in_metadata(['alien'], self.md, 'x', 'y')
        self.assertEqual(var_in_metadata, error_expected)

    def test_check_rule_in_temp(self):
        rule_in_temp = check_rule_in_temp('str', {'str': 'ok', 'a': 'b'})
        self.assertEqual(rule_in_temp, '')
        rule_not_in_temp = check_rule_in_temp('str', {'a': 'b'})
        self.assertEqual(rule_not_in_temp, 'rule "str" not in rules template')

#    def test_traverse_rules(self):
#        traversed_rules = traverse_rules()
#        self.assertEqual(traversed_rules, '')


if __name__ == '__main__':
    unittest.main()
