# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
import pkg_resources

TEMPLATES = pkg_resources.resource_filename('q2_metadata', 'assets')


def check_rules_in_md(md: pd.DataFrame, rules: dict):
    matches = {}
    print(md.columns.str.lower())
    for rule in rules:
        if rule in md.columns:
            matches[rule] = md[rule].unique().tolist()
        elif rule.lower() in md.columns.str.lower():
            lower_rule_idx = md.columns.str.lower().index(rule.lower())
            matches[rule] = md.iloc[:, lower_rule_idx].unique().tolist()
        else:
            matches[rule] = 0
    print("matches")
    print(matches)
    print(matchesgf)
    return matches

def get_dtypes(md: pd.DataFrame):
    unknowns = {}
    dtypes = {}
    all_unks = {}
    to_replace_per_col = {}
    for col in md.columns.tolist():
        to_replace_per_col[col] = {}
        native_type = str(md[col].dtypes)
        dtypes[col] = [native_type]
        unknowns[col] = {}
        float_to_string = [0, 0, 0, []]
        if col == '#SampleID':
            dtypes[col].append('object')
            continue
        for v in md[col].unique().tolist():
            if str(v) == 'nan':
                float_to_string[0] += 1
            else:
                try:
                    float_v = float(v)
                    float_to_string[1] += 1
                except ValueError:
                    float_to_string[2] += 1
                    float_to_string[3].append(v)
                    if len(v) < 30 and '/' not in v and '-' not in v and ':' not in v and not len([x for x in v if v.isdigit()]):
                        all_unks.setdefault(v, []).append(col)
        unknowns[col] = float_to_string
        if not float_to_string[2]:
            dtypes[col].append('float64')
            for v in md[col].unique().tolist():
                try:
                    float_v = float(v)
                except ValueError:
                    to_replace_per_col[col][v] = np.nan
        elif float_to_string[2]:
            if float_to_string[1] or float_to_string[0]:
                dtypes[col].append('check')
            else:
                dtypes[col].append('object')

    all_unks_pd_L = []
    for col in md.columns.tolist():
        all_unks_pd_L.append([1 if col in vals else 0 for key,vals in sorted(all_unks.items())])

    all_unks_pd = pd.DataFrame(all_unks_pd_L, index=md.columns.tolist(), columns=sorted(all_unks.keys()))
    nrows = all_unks_pd.shape[0]
    sumCols = all_unks_pd.sum(0)
    # all_unks_pd_common = all_unks_pd.loc[:, sumCols > (nrows*0.1)]
    all_unks_pd_common = all_unks_pd.loc[:,sumCols > 10]
    print(all_unks_pd_common.columns)