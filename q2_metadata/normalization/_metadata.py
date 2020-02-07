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


def check_md_rules(md: pd.DataFrame, rules: dict) -> dict:
    """
    Collect the unique values of the metadata columns
    for which there is also a rule file.
    Otherwise, give a 0 values to columns without rule:
        - these columns may have a rule but a slight typo,
        e.g. rule "geo_loc_name" for column geo_locname".
    :param md: metadata table to normalize.
    :param rules:
        keys    = yaml rules file for each column.
        values  = rules (not used here).
    :return:
        keys    = columns of the metadata.
        values  = unique values for the column.
        e.g.
            {'body_product_': 0,    <-- NO MATCH
             'collection_timestamp': ['2016-11-22'],
             'country': ['Not applicable', 'USA'],
             'diabetes': ['I do not have this condition',
              'Diagnosed by a medical professional (doctor, physician assistant)',
              'Not provided'],
             'DNA_extracted': ['Not provided', '0.33'],
             'fermented_plant_frequency': ['Occasionally (1-2 times/week)',
              'Never',
              'Daily'],
             'geo_locname': 0,      <-- NO MATCH
             'height_Cm': ['10', '121', 'Not applicable'],
             'host_taxid': 0        <-- NO MATCH
             }
    """
    matches = {}
    for col in md.columns:
        if col in rules or col.lower() in rules:
            matches[col] = md[col].unique().tolist()
        else:
            matches[col] = 0
    return matches


def check_rules(factors: list, rule: list):
    if 'exist' in rule:
        # check that the variable has factors for all entries
        pass
    if 'ontology' in rule:
        # check that the terms appear in the given ontology database
        pass
    if 'typos' in rule:
        # check for typos...
        pass


def get_edits(matches: dict, rules: dict):
    """
    Get the values that should be replaced according to the
    application of the rules.

    :param matches: unique factors of the variables that have a rule.
    :param rules: nested structure containing the rules values.
    :return:
    """
    edits = []
    for col, factors in matches.items():
        if not factors:
            continue
        rule = rules[col]
        check_rules(factors, rule['check'])
        print(factors)
        print(col_rules)
        print(fds)



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