# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin.model as model

from .plugin_setup import plugin


class MetadataFormat(model.TextFileFormat):
    def sniff(self):
        return True


MetadataDirectoryFormat = model.SingleFileDirectoryFormat(
    'MetadataDirectoryFormat', 'metadata.tsv', MetadataFormat)


plugin.register_formats(MetadataFormat, MetadataDirectoryFormat)