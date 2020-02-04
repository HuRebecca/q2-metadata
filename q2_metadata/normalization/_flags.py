# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd


def show_rules_structure_issues(root_dir: str, issues: list) -> None:
    issues_pd = pd.DataFrame(
        issues,
        columns = ['file', 'type', 'rule',
                   'value', 'reference', 'message']
    )
    out_flags = '%s/normalization/outputs/rules_check.txt' % root_dir
    with open(out_flags, 'w') as o:
        for error_type, error_type_pd in issues_pd.groupby('message'):
            # print('[%s cases] "%s"' % (error_type_pd.shape[0], error_type))
            o.write('[%s cases] "%s"\n' % (error_type_pd.shape[0], error_type))
            for error_file, error_file_pd in error_type_pd.groupby('file'):
                # print('%s: %s' % (error_file, ', '.join(error_file_pd.rule.tolist())))
                o.write('\t%s: %s\n' % (error_file, ', '.join(error_file_pd.rule.tolist())))