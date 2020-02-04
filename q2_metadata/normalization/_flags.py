# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd


def show_issues(o, issues: list) -> None:
    issues_pd = pd.DataFrame(
        issues,
        columns = ['file', 'type', 'rule',
                   'value', 'reference', 'message'])
    for error_type, error_type_pd in issues_pd.groupby('message'):
        # print('[%s cases] "%s"' % (error_type_pd.shape[0], error_type))
        o.write('[%s cases] "%s"\n' % (error_type_pd.shape[0], error_type))
        for error_file, error_file_pd in error_type_pd.groupby('file'):
            # print('%s: %s' % (error_file, ', '.join(error_file_pd.rule.tolist())))
            o.write('\t%s: %s\n' % (error_file, ', '.join(error_file_pd.rule.tolist())))
        o.write('\n')


def show_missing(o, missing: dict) -> None:
    for mandatory_rule, rule_names in missing.items():
        o.write('[missing] "%s" in:\n' % mandatory_rule)
        for rule_name in rule_names:
            o.write(' - %s\n' % rule_name)
    o.write("\n")
