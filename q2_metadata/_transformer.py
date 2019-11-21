# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd

from ..plugin_setup import plugin
from . import MetadataFormat

from qiime2.plugin import Metadata


@plugin.register_transformer
def _1(data: pd.DataFrame) -> MetadataFormat:
    ff = MetadataFormat()
    with ff.open() as fh:
		# USE METATADA
		# push to new branch under my fork for next meeting
        data.to_csv(fh, index=False, sep='\t')
    return ff


# @plugin.register_transformer
# def _2(ff: NewickFormat) -> skbio.TreeNode:
#     with ff.open() as fh:
#         return skbio.TreeNode.read(fh, format='newick', verify=False)
