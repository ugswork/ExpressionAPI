# -*- coding: utf-8 -*-
import os
from pprint import pprint

from TableIndexer import TableIndexer
from Workspace.WorkspaceClient import Workspace as Workspace

class ExprMatrixIndexer:

    def __init__(self, config, logger):

        self.logger = logger
        self.FPKM_SUFFIX = '_FPKM'
        self.TPM_SUFFIX = '_TPM'

        self.ws_url = config["workspace-url"]

        expr_index_dir = config["expression-index-dir"]
        self.expression_index_dir = os.path.join(config['scratch'], expr_index_dir)
        if not os.path.isdir(self.expression_index_dir):
            os.makedirs(self.expression_index_dir)

        self.debug = "debug" in config and config["debug"] == "1"

    def search_exprMatrix_by_geneID(self, token, ref, query, sort_by, start, limit, num_found):

        search_object = 'data'
        info_included = ['values']
        table_indexer = TableIndexer(token, self.ws_url)

        ret = table_indexer.run_search(ref, self.expression_index_dir, self.FPKM_SUFFIX,
                                       search_object, info_included, query,
                                       sort_by, start, limit, num_found, self.debug)
        return ret

    def search_exprMatrix_by_expresion(self, token, ref, query, sort_by, start, limit, num_found):

        search_object = 'data'
        info_included = ['col_ids']
        table_indexer = TableIndexer(token, self.ws_url)

        ret = table_indexer.run_search(ref, self.expression_index_dir, self.FPKM_SUFFIX,
                                       search_object, info_included, query,
                                       sort_by, start, limit, num_found, self.debug)

        return ret

    def search_exprMatrix_by_value(self, token, ref, query, sort_by, start, limit, num_found):

        search_object = 'data'
        info_included = ['values']
        table_indexer = TableIndexer(token, self.ws_url)

        ret = table_indexer.run_search(ref, self.expression_index_dir, self.FPKM_SUFFIX,
                                       search_object, info_included, 'tracted_WT_rep1_hisat2_stringtie_expression',
                                       sort_by, start, limit, num_found, self.debug)
        return ret


