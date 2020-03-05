# ----------------------------------------------------------------------------
# Copyright (c) 2016-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


def get_intersection(variables_rules: list, md_columns: list) -> list:
    """
    Get the names of the metadata variables that have associated rules.

    Parameters
    ----------
    variables_rules : list
        Names of variables that have associated rules.
    md_columns : list
        Names of the variables in the metadata table.

    Returns
    -------
    intersection : list
       Metadata variables that have associated rules.
    """
    intersection = set(variables_rules) & set(md_columns)
    if not len(intersection):
        raise ValueError(
            "No metadata columns associated with yaml rules."
        )
    return sorted(intersection)
