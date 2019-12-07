# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# from .plugin_setup import plugin
# import qiime2.plugin.model as model
# from qiime2.plugin as SemanticType
# from qiime2 import Metadata
#
# # --------
# #  Format
# # --------
# class MetadataFormat(model.TextFileFormat):
#     def sniff(self):
#         return True
#
# MetadataDirectoryFormat = model.SingleFileDirectoryFormat(
#     'MetadataDirectoryFormat', 'metadata.tsv', MetadataFormat)
#
# plugin.register_formats(MetadataFormat, MetadataDirectoryFormat)
#
# # -------
# #  types
# # -------
# MetadataX = SemanticType('MetadataX')
# plugin.register_semantic_types(MetadataX)
# plugin.register_semantic_type_to_format(
#     MetadataX, artifact_format=MetadataDirectoryFormat
# )
# plugin.register_formats(MetadataFormat, MetadataDirectoryFormat)
#
# # --------------
# #  transformers
# # --------------
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
