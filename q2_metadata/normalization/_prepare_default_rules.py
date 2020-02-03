# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import yaml
import pandas as pd
import pkg_resources
from os.path import join

TEMPLATES = pkg_resources.resource_filename('q2_metadata', 'assets')
RULES = pkg_resources.resource_filename('q2_metadata', 'normalization/rules/default')


def get_agp_definitions() -> pd.DataFrame:
    """
    Parse the supplementary table from the American Gut Project paper.
    DOI: 10.1128/mSystems.00031-18 (TABLE S2)
        "American Gut data dictionary, proportion of responses per American
        Gut survey question that are represented as a single question
        (multi-selection responses were omitted as these are stored in
        the metadata as per response type), informal dietary questions
        and correlations with the food frequency questionnaire, effect
        size results without bloom sOTUs, and variable mapping with
        reference 2."

    For each of the general questionnaire variable that informs on the
    "general health status, disease history, and lifestyle", it contains:
        - Column header
        - Helpful hints
        - Definition
        - Ontology
        - Format
        - Expected values
        - Missing values
        - Blank value
        - Source columns
        - Derivative columns
        - Introduced
        - Modified
        - Notes
        - Remapping

    :return: the above columns for each variable as a data frame.
    """
    agp_suppl = join(TEMPLATES, 'inline-supplementary-material-3.txt')
    agp_suppl_pd = pd.read_csv(agp_suppl, header=0, sep='\t')
    agp_suppl_pd.rename(columns={
        'Description': 'Definition',
        'Data type': 'Format',
        'Question type': 'Helpful hints'
    }, inplace=True)
    return agp_suppl_pd


def get_kl_md_template() -> pd.DataFrame:
    """
    Qiita's metadata template (version 201910010)
    see https://knightlab.ucsd.edu/wordpress/?page_id=478
    This file provide standards for the preparation of
    a metadata file to be uploaded to Qiita. It contains:
        - column
        - Definition
        - Helpful hints
        - Links
        - Format
        - Example mouse gut feces
        - Example ...

    :return: the above columns for each variable as a data frame.
    """
    metadata_template = join(TEMPLATES, 'metadata_template.txt')
    md_temp_pd = pd.read_csv(metadata_template, header=0, sep='\t')
    md_temp_pd['column'] = md_temp_pd['column'].str.lower()
    return md_temp_pd


def get_md_temp_dict(md_temp_t: pd.DataFrame) -> dict:
    """
    Collect the unique possible values from
         - the template useful columns
            ['Definition',
             'Helpful hints',
             'Links',
             'Format']
         - the template "Example(s)"
    e.g. for variable "altitude"
        {'Definition': 'height above land (in meters) where air was sampled',
         'Examples': {'100': {'100'}, 'not applicable': {'Not applicable'}},
         'Format': 'float',
         'Helpful hints': 'only for air samples',
         'Links': nan}

    :param md_temp_t:
    :return:
    """
    # get template key -> values for columns "Definition", "Helpful hints", "Links" and "Format"
    helpful_headers = ['Definition', 'Helpful hints', 'Links', 'Format']
    md_temp_d = dict(md_temp_t.loc[md_temp_t.col.isin(helpful_headers)].values)
    # collect all the possible unique values for the other columns (in the template "Example(s)")
    md_temp_d['Examples'] = {}
    for (eg_key, eg_value) in md_temp_t.loc[~md_temp_t.col.isin(helpful_headers)].values:
        # otherwise: collect the lowercase, unique responses from the examples
        md_temp_d['Examples'].setdefault(eg_value.lower(), set()).add(eg_value)
    return md_temp_d


def correct_key(key: str, lookup: dict) -> str:
    """
    :param key: to potentially edit...
    :param lookup: ... if present in lookup dict
    :return: values for the lookup dict key
    """
    if key in lookup:
        return lookup[key]
    return key


def compare_with_agp(var: str, agp_pd: pd.DataFrame, in_agp: dict) -> dict:
    """
    Collect the variables that are in the template metadata
    and exist in the the AGP supplementary table.

    :param agp_pd: agp reference metadata variables description
    :param in_agp: collection to fuel with match / no match
    :param var: current metadata variable
    :return: mapping of the variables in the template that already exist in agp
    """
    agp_vars = agp_pd['Column header'].tolist()
    if var in agp_vars:
        in_agp[var] = var
    elif var.startswith('host_'):
        var_edit = var.replace('host_', '')
        if var_edit in agp_vars:
            in_agp[var_edit] = var
    return in_agp


def get_template_vs_agp_inconsistencies() -> (dict, dict):
    """
    :return:
        (Variable mappings from "md_temp_pd" to "agp_suppl_pd",
         Origin information for some inferred variables of "md_temp_pd")
    """
    real_name_fp = join(TEMPLATES, 'metadata_template_to_agp.txt')
    real_name = dict(pd.read_csv(real_name_fp, header=0, sep=',').values)

    add_on_info_fp = join(TEMPLATES, 'metadata_template_extra_columns_origin.txt')
    add_on_info = dict([x[0], x[1:].tolist()] for x in pd.read_csv(add_on_info_fp, header=0, sep=',').values)
    return real_name, add_on_info


def get_meta_from_template(
        agp_suppl_pd: pd.DataFrame,
        md_temp_pd: pd.DataFrame) -> (dict, dict):
    """
    :param agp_suppl_pd: AGP metadata descriptions table (per variable name)
    :param md_temp_pd: metadata template table
    :return:
        files_data:
            Keys    = variable
            Values  = possible values examples/defaults
                e.g. {'Expected values': ['ex: 1001'],
                      'Missing values': ['Not provided'],
                      'Blank value': ['BLANK[identifier]']}
        variables_renamed:
            Keys    = variable
            Values  =
    """
    real_name, add_on_info = get_template_vs_agp_inconsistencies()
    files_data = {}
    variables_renamed = {}
    # for each enumerated template metadata's variable (in "column" column) and its table data
    for variable_, md_temp in md_temp_pd.groupby('column'):
        # remove the metadata variable names column, transpose, and rename
        md_temp_t = md_temp.drop(columns='column').T.reset_index()
        md_temp_t.columns = ['col', variable_]
        md_temp_t = md_temp_t.loc[(md_temp_t[variable_] != '(pick a) biome') &
                                  (~md_temp_t[variable_].isna())]
        # collect the unique possible values from template
        md_temp_d = get_md_temp_dict(md_temp_t)
        # edit key in template metadata to the matching name in qiita
        variable = correct_key(variable_, real_name)
        # collect the possible values for the current variable
        files_data[variable] = md_temp_d
        # apply changes to roll back to AGP standards
        variables_renamed = compare_with_agp(
            variable,
            agp_suppl_pd,
            variables_renamed
        )
    return files_data, variables_renamed


def get_factors(cell: str) -> list:
    """
    Split a metadata factor and remove the trailing quotes
    :param cell: metadata factor (i.e. table cell content)
    :return: content split on the pipe character
    """
    cell_split = [x.strip().strip('"').strip("'") for x in cell.split('|')]
    return cell_split


def update_derivative_source(
        cur_agp_suppl_pd: pd.DataFrame,
        variable: str,
        derivatives: dict,
        sources: dict) -> (dict, dict):
    """
    Add the current variable's values for AGP definitions of:
    - Derivative columns
    - Source columns
    :param cur_agp_suppl_pd: AGP supplementary info reduce to the current variable.
    :param variable: current variable name.
    :param derivatives: to be update here.
    :param sources: to be update here.
    :return: updated derivatives and sources dicts.
    """
    cur_agp_suppl_pd.set_index('col', inplace = True)
    cur_derivative = str(cur_agp_suppl_pd.loc['Derivative columns', variable])
    if cur_derivative != 'nan':
        derivatives[variable] = get_factors(cur_derivative)
    cur_source = str(cur_agp_suppl_pd.loc['Source columns', variable])
    if cur_source != 'nan':
        sources[variable] = get_factors(cur_source)
    return derivatives, sources


def get_meta_from_qiita(
        files_data: dict,
        agp_suppl_pd: pd.DataFrame) -> (dict, dict, dict, dict):
    """
    :param files_data:
    :param variables_renamed:
    :param agp_suppl_pd: AGP metadata descriptions table (per variable name)
    :return:
    """
    sources, derivatives = {}, {}
    red_agp_columns = ['Expected values', 'Missing values', 'Blank value']
    agp_columns = red_agp_columns + ['Ontology', 'Introduced', 'Source columns',
                                     'Derivative columns', 'Modified', 'Notes', 'Remapping']
    for variable, cur_agp_suppl_pd_ in agp_suppl_pd.groupby('Column header'):
        # remove the metadata variable names column, transpose, and rename
        cur_agp_suppl_pd = cur_agp_suppl_pd_.drop(columns='Column header').T.reset_index().copy()
        cur_agp_suppl_pd.columns = ['col', variable]
        # whether current AGP variable encountered or not in template
        cur_d = {}
        if variable in files_data:
            for k, v in cur_agp_suppl_pd.loc[(cur_agp_suppl_pd.col.isin(red_agp_columns)) &
                                             (~cur_agp_suppl_pd[variable].isna())].values:
                cur_d[k] = get_factors(v)
        else:
            for k,v in cur_agp_suppl_pd.values:
                if k not in agp_columns:
                    cur_d[k] = v
                elif k in red_agp_columns and str(v) != 'nan':
                    cur_d[k] = get_factors(v)

        files_data[variable] = cur_d
        derivatives, sources = update_derivative_source(
            cur_agp_suppl_pd, variable, derivatives, sources
        )
    return files_data, derivatives, sources


def default_validation() -> str:
    norm_valid = {'normalization':
       {
           'minimum': 0,
           'maximum': 120,
           'gated_value': 'Out of bounds'
       },
     'validation':
     {'warn_if_null': ['country'],
      'force_to_null_if':
      {'is null': ['host_subject_id', 'host_taxid']}
     }
    }
    norm_valid = yaml.dump(norm_valid, default_flow_style=False)
    return norm_valid


def write_rules(files_data: dict) -> None:
    """
    :param files_data:
    :return:
    """
    replacement = {
        'Format': 'format',
        'Blank value': 'blank',
        'Expected values': 'expected',
        'Missing values': 'missing'
    }
    for variable, rule_values in files_data.items():
        rule_fp = '%s/%s.yml' % (RULES, variable)
        with open(rule_fp, 'w') as o:
            rules = []
            comments = ['# variable: %s' % variable]
            for rule_, values in sorted(rule_values.items()):
                if rule_ in replacement:
                    rule = replacement[rule_]
                else:
                    rule = rule_
                if rule in ['Definition', 'Helpful hints', 'Links']:
                    comments.append('# %s: %s' % (rule, values))
                elif rule == 'Examples':
                    comments.append('# Examples:\n')
                    for eg_key, eg_val in values.items():
                        comments.append('#\t* %s: "%s"' % (eg_key, '", "'.join(sorted(eg_val))))
                else:
                    if isinstance(values, list):
                        comments.append('# %s: "%s"' % (rule, '", "'.join(values)))
                        if rule == 'expected':
                            rules.append('%s:' % rule)
                            rules.extend(['- %s' % val for val in values])
                        else:
                            rules.append('%s: %s' % (rule, values[0]))
                    else:
                        rules.append('%s: %s' % (rule, values))
            for comment in comments:
                o.write('%s\n' % comment)
            for rule in rules:
                o.write('%s\n' % rule)
            o.write('remap:\n  BEFORE: AFTER\n')
            o.write(default_validation())
        print(rule_fp)


def prepare_rules_from_template_and_qiita() -> None:
    """
    Get the metadata variables in KL template and AGP supplementary
    Collect their attributes such as Format and Expected values, etc:
      (a python Class definition would work better -> to be reviewed)
    Write the default rules files based on these "default" attributes
    """
    # get AGP metadata (supplementary table)
    agp_suppl_pd = get_agp_definitions()
    # get the Knight lab metadata (template from website)
    md_temp_pd = get_kl_md_template()

    # Collect the metadata variables and their default factor values from:
    # - AGP supplementary table.
    files_data, variables_renamed = get_meta_from_template(
        agp_suppl_pd, md_temp_pd
    )
    # - Qiita metadata template
    # (derivatives and sources may be useful for actual rules implementation)
    files_data, derivatives, sources = get_meta_from_qiita(
        files_data, agp_suppl_pd
    )
    write_rules(files_data)