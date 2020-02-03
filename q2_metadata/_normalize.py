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

# writing default rule.yml files based on metadata standards (KL template + AGP suppl)
# --> NEEDS TO BE REVIEWED AND VALIDATED BY GAIL / EXPERT KNOWLEDGE
from q2_metadata.normalization._prepare_default_rules import prepare_rules_from_template_and_qiita

from q2_metadata.normalization._io_utils import get_rules, get_databases
from q2_metadata.normalization._waving_flags import show_rules_structure_issues


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

    # THIS WILL PROBABLY NOT BE HERE IN THE PACKAGE,
    # BUT I FIGURED MY PARSING OF THE RULES DEFAULTS FROM
    #  (1) Qiita metadata (Knight lab website)
    #  (2) AGP metadata variables definitions
    # COULD BE REVIEWED HERE AND MADE TESTED/REPRODUCIBLE
    prepare_rules_from_template_and_qiita()

    # Get path of the executable
    root_dir = dirname(abspath(__file__))
    rules, rules_dict, issues = get_rules(root_dir, md)

    if issues:
        show_rules_structure_issues(root_dir, issues)
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