# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2 as q2
import pandas as pd

from q2_metadata.normalization._io_utils import get_variables_rules, get_databases
from q2_metadata.normalization._flags import show_issues, show_missing, show_equivalent
from q2_metadata.normalization._metadata import get_edits, get_redundancies, get_md_rules_venn

import pkg_resources

ROOT = pkg_resources.resource_filename("q2_metadata", "")


# annotate how types are expected to be passed to the function
# (explicit declare that first arg should be metadata class)
def normalize(metadata: q2.Metadata) -> q2.Metadata:
    """
    :param metadata:
        Input metadata file
    :return:
        A curated metadata table.
    """

    # Get metadata as pandas data frame
    md = metadata.to_dataframe()

    # Get rules
    mandatory_rules = ['format'] #['blank', 'format', 'missing']
    variables_rules, variables_rules_dict = get_variables_rules(ROOT)

    # ==== IN DEV (i.e. to be explained in next PR) ======
    # get the yaml rules for each column of the passed metadata
    venn = get_md_rules_venn(md, variables_rules)

    # Get redundant columns and factors
    redundant_variable, redundant_factors = get_redundancies(md)
    # FLAGS
    if redundant_variable or redundant_factors:
        out_flags = '%s/normalization/outputs/md_check.txt' % ROOT
        with open(out_flags, 'w') as o:
            show_equivalent(o, redundant_variable, redundant_factors, venn)
        print('Equivalent columns of factors... see %s\nExiting...' % out_flags)
        # sys.exit(1)

    outputs, log = get_edits(md, venn, variables_rules,
                             mandatory_rules, variables_rules_dict)
    # ====================================================

    databases = get_databases(ROOT)
    # md_out = do_normalize(md, rules)

    # only during dev so that the function return something :)
    md_out = pd.DataFrame({
        'sampleid': ['A', 'B'],
        'col1': ['1', '2'],
        'col2': ['3', '4']
    }).set_index('sampleid')
    return q2.Metadata(md_out)