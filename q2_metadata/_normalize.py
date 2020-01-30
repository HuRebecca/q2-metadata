# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import sys
from os.path import abspath, dirname

import qiime2 as q2
import pandas as pd

from q2_metadata.normalization._io_utils import (

)
from .normalization._waving_flags import show_rules_structure_issues


# annotate how types are expected to be passed to the function
# (explicit declare that first arg should be metadata class)
def normalize(metadata: q2.Metadata) -> q2.Metadata:
    """
    :param metadata:
        Input metadata file
    :return:
        A curated metadata table.
    """

    # Get path to metadata dataframe
    md = metadata.to_dataframe()

    # Get hard-coded but possible user-modified data from the "databases" and "rules" folders
    root_dir = dirname(abspath(__file__))

    rules, rules_dict, issues = get_rules(root_dir, md)

    if issues:
        show_rules_structure_issues(issues)
        sys.exit(1)

    databases = get_databases(root_dir)


    # md_out = do_normalize(md, rules)

    # only during dev so that the function return something :)
    md_out = pd.DataFrame({
        'sampleid': ['A', 'B'],
        'col1': ['1', '2'],
        'col2': ['3', '4']
    }).set_index('sampleid')
    return q2.Metadata(md_out)