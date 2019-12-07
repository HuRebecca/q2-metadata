# # ----------------------------------------------------------------------------
# # Copyright (c) 2016-2019, QIIME 2 development team.
# #
# # Distributed under the terms of the Modified BSD License.
# #
# # The full license is in the file LICENSE, distributed with this software.
# # ----------------------------------------------------------------------------
#
# from .plugin_setup import plugin
# from . import MetadataFormat
#
# from qiime2.plugin import Metadata
#
#
# @plugin.register_transformer
# def _1(data: Metadata) -> MetadataFormat:
#     ff = MetadataFormat()
#     path = str(ff) + '/metadata.tsv'
#     data.save(path)
#     return ff
#
#
# def _2(ff: MetadataFormat) -> Metadata:
#     path = str(ff) + '/metadata.tsv'
#     return Metadata.load(path)
