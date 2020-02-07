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
from q2_metadata.normalization._check_rules_format import check_rules_issues, check_mandatory_rules
from q2_metadata.normalization._flags import show_issues, show_missing
from q2_metadata.normalization._metadata import check_md_rules, get_edits

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

    #  = = = = THIS WILL PROBABLY NOT BE HERE IN THE PACKAGE = = = = =
    #       BUT I FIGURED MY PARSING OF THE RULES DEFAULTS FROM
    #           (1) Qiita metadata (Knight lab website)
    #           (2) AGP metadata variables definitions
    #       COULD BE REVIEWED HERE AND MADE TESTED/REPRODUCIBLE
    prepare_rules_from_template_and_qiita()
    #  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # =================================================================
    # Get rules business
    rules, rules_dict = get_rules(ROOT)
    issues = check_rules_issues(rules, md)
    missing = check_mandatory_rules(rules)
    if issues or missing:
        out_flags = '%s/normalization/outputs/rules_check.txt' % ROOT
        with open(out_flags, 'w') as o:
            show_issues(o, issues)
            show_missing(o, missing)
        print('Issues/Missing rules... see %s\nExiting...' % out_flags)
        # sys.exit(1)
    # =================================================================

    print("rules_dict")
    print(rules_dict)

    # ==== IN DEV ====
    matches = check_md_rules(md, rules)
    edits = get_edits(matches, rules)
    # ==== IN DEV ====

    print(kfb)

    databases = get_databases(ROOT)

    # md_out = do_normalize(md, rules)

    # only during dev so that the function return something :)
    md_out = pd.DataFrame({
        'sampleid': ['A', 'B'],
        'col1': ['1', '2'],
        'col2': ['3', '4']
    }).set_index('sampleid')
    return q2.Metadata(md_out)