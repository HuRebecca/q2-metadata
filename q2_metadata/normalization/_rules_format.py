# ----------------------------------------------------------------------------
# Copyright (c) 2017-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import datetime
import pandas as pd


def check_val_type(v, v_exp: list, k: str, rule_name: str) -> str:
    """
    :param v: one rule value(s) of the current rules file.
    :param v_exp: the corresponding expected value(s) for the reference rules.
    :param k: one rule of the current metadata rules file.
    :param rule_name: current rule file name (i.e. metadata variable).
    :return: an empty message (no problem encountered) or an error message.
    """
    flag = ''
    if not [x for x in v_exp if isinstance(v, eval(x))]:
        flag = 'value(s) to rule "%s" (variable "%s") not of expected type:' % (k, rule_name)
        flag += '\n - %s' % '\n - '.join(v_exp)
    return flag


def check_val_in_dictionary(v: str, v_exp: list, k: str, rule_name: str):
    """
    :param v: one rule value(s) of the current rules file.
    :param v_exp: the corresponding expected value(s) for the reference rules.
    :param k: one rule of the current metadata rules file.
    :param rule_name: current rule file name (i.e. metadata variable).
    :return: an empty message (no problem encountered) or an error message.
    """
    flag = ''
    if not v.lower() in [x.lower() for x in v_exp]:
        flag = 'value(s) to rule "%s" (variable "%s") not in default dictionary (case-insensitive):' % (k, rule_name)
        flag += '\n - %s' % '\n - '.join(v_exp)
    return flag


def check_var_in_metadata(v: list, md: pd.DataFrame, k: str, rule_name: str):
    """
    :param v: one rule value(s) of the current rules file.
    :param md: input metadata table (only the columns values are used).
    :param rule_name: current rule file name (i.e. metadata variable).
    :return: an empty message (no problem encountered) or an error message.
    """
    flag = ''
    v_lower = set([x.lower() for x in v])
    md_columns = set([x.lower() for x in md.columns.tolist()])
    if sorted(md_columns & v_lower) != sorted(v_lower):
        not_in_dict = sorted(v_lower ^ (md_columns & v_lower))
        flag = 'variable(s) to rule "%s" (variable "%s") not in metadata columns (case-insensitive):' % (k, rule_name)
        flag += '\n - %s' % '\n - '.join(not_in_dict)
    return flag


def check_bool_in_dict(v: list, v_exp: dict, k: str, rule_name: str):
    """

    THIS FUNCTION MAY NEED REVISION UPON DEFINITION IF THE RULES SCOPES (AND HENCE FORMAT)
    THIS FUNCTION MAY NEED REVISION UPON DEFINITION IF THE RULES SCOPES (AND HENCE FORMAT)
    THIS FUNCTION MAY NEED REVISION UPON DEFINITION IF THE RULES SCOPES (AND HENCE FORMAT)

    This function treat sub-rules that could by a list in the current rules file,
    but that exists as booleans in the reference, e.g.
        in the rule file:

            validation:
            - must exist
            - check ontology
            - flag typos

        in the reference:

            validation,dict:
              check ontology,bool: 1
              flag typos,bool: 1
              force_to_blank_if,dict:
                is null,txt:
                - variable
              must exist,bool: 1

    Check if the booleans in the rule list exist in the labeled-as-booleans key of the reference.

    :param v: one rule value(s) of the current rules file.
    :param v_exp: the corresponding expected value(s) for the reference rules.
    :param k: one rule of the current metadata rules file.
    :param rule_name: current rule file name (i.e. metadata variable).
    :return: an empty message (no problem encountered) or an error message.
    """
    flag = ''
    # get the booleans existing as dict keys in the reference for the current rule (and lowercase)
    v_exp_lower = [x.split(',')[0].lower() for x in v_exp if x.split(',')[1] == 'bool']
    # if there are reference booleans (that's could be hard-coded but could be the case for many rules)
    if v_exp_lower:
        # lowercase rule values that are activated booleans (i.e. if present: True)
        v_lower = [x.lower() for x in v]
        # v_lower = [x.lower() for x in v if isinstance(x, str)]
        # flag the activated booleans that would miss in the reference
        if sorted(set(v_exp_lower) & set(v_lower)) != sorted(set(v_lower)):
            not_in_dict_set = set(v_lower) ^ (set(v_exp_lower) & set(v_lower))
            not_in_dict = [x.split(',')[0] for x in v if x.lower() in not_in_dict_set]
            flag = 'bool value(s) to sub-rule "%s" (variable "%s") not in default dictionary (case-insensitive):' % \
            (k, rule_name)
            flag += '\n - %s' % '\n -'.join(not_in_dict)
    else:
        flag = 'value(s) to rule "%s" (variable "%s") should not be a dict' % (k, rule_name)
    return flag


def check_rule_in_temp(k: str, rules_template_keys: dict) -> str:
    """
    Simply check if the rule exists in the sum of all the rules.

    :param k: one rule of the current rules file
    :param rules_template_keys: reference rules format structure.
    :return: an empty message (no problem encountered) or an error message.
    """
    flag = ''
    if k not in rules_template_keys:
        flag = 'rule "%s" not in rules template' % k
    return flag


def get_rules_template_keys(rules_template: dict) -> dict:
    """
    Get template rule keys and their corresponding type and key in the actual rule files.

    :param rules_template: rules freshly parsed from the reference rules.txt file.
    :return: keys of the reference rules split on comma (where type is encoded).
    """
    rules_template_keys = {}
    for k, v in rules_template.items():
        key = k.split(',')[0]   # the actual "rule name"
        value = [k] + k.split(',')[1:]  # the "rule name + type" and the "type"
        rules_template_keys[key] = value
    return rules_template_keys


def traverse_rules(rule_name: str, rule: dict, rules_template: dict, issues: list, md: pd.DataFrame) -> list:
    """
    Go through the nested dict structure of the actual, current rules parsed from the yml into
    a dict, and check that the values associated with each rule are indeed as expected.
    Expectations are in the reference file "rules.txt", in which the rule names are labeled with
    a type info, e.g.
        for the "blank" rule:
            blank: Not applicable
        the reference if this "blank" rule:
            blank,txt:
            - not applicable
            - not collected
            - not provided
            - restricted access
        (the case-sensitivity is taken care of)
    Inspired from https://stackoverflow.com/questions/10756427/loop-through-all-nested-dictionary-values
    :param rule_name: current rule name.
    :param rule: current rules parsed from the yml file.
    :param rules_template: reference rules format structure to compare the current rule to.
    :param issues: collected problems encountered for this and other rules.
    :param md: input metadata table (only the columns values are used).
    :return: collected problems encountered for this and other rules (appended).
    """
    #
    # {'blank': ['blank,txt', 'txt'], ..., 'validation': ['validation,dict', 'dict']}
    rules_template_keys = get_rules_template_keys(rules_template)

    # parse the current rule keys
    cur_rule = rule.copy()
    for k, v in cur_rule.items():

        if check_rule_in_temp(k, rules_template_keys):
            issues.append([rule_name, typ, k, v, 'must exist in template', 'rule not in template'])
            continue

        key, typ = rules_template_keys[k]
        v_exp = rules_template[key]
        if isinstance(v, dict):
            # end of a rule (nested dict is for replacement)
            if v_exp == {'str': 'str'}:
                continue
            # not the end of rule (keep going in nested dict)
            else:
                issues = traverse_rules(rule_name, v, v_exp, issues, md)
        else:
            # -----------------------------------------------------------------------------
            # this entire part could be more "hard-coded"
            if typ == 'dict':
                flag = check_bool_in_dict(v, v_exp, k, rule_name)
                if flag.startswith('value'):
                    issues.append([rule_name, typ, k, v, v_exp, 'value is a mapping'])
                elif flag.startswith('bool'):
                    issues.append([rule_name, typ, k, v, v_exp, 'bool value not in dictionary'])
            elif typ == 'txt':
                if isinstance(v, datetime.date):
                    continue
                # case where the passed values to check are the metadata columns
                if key == 'is null,txt':
                    if check_var_in_metadata(v, md, k, rule_name):
                        issues.append([rule_name, typ, k, v, 'metadata columns', 'variable not in metadata'])
                elif check_val_in_dictionary(v, v_exp, k, rule_name):
                    issues.append([rule_name, typ, k, v, v_exp, 'value not in dictionary'])
            elif typ == 'type' and check_val_type(v, v_exp, k, rule_name):
                issues.append([rule_name, typ, k, key, v, 'value not of expected type'])
            # -----------------------------------------------------------------------------
    return issues
