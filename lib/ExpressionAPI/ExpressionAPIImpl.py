# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import sys
import time
from core.exprMatrix_utils import ExprMatrixUtils
from core.ExprMatrixIndexer import ExprMatrixIndexer
#END_HEADER


class ExpressionAPI:
    '''
    Module Name:
    ExpressionAPI

    Module Description:
    A KBase module: ExpressionAPI
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/ExpressionAPI.git"
    GIT_COMMIT_HASH = "7989cdea44e2da11700ec259b9211729a9855037"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.__LOGGER = logging.getLogger('ExpressionUtils')
        self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")
        self.config = config
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        self.expr_matrix_utils = ExprMatrixUtils(config, self.__LOGGER)
        self.indexer = ExprMatrixIndexer(config, self.__LOGGER)
        #END_CONSTRUCTOR
        pass


    def get_expressionMatrix(self, ctx, params):
        """
        :param params: instance of type "getExprMatrixParams" (* Following
           are the required input parameters to get Expression Matrix *) ->
           structure: parameter "workspace_name" of String, parameter
           "output_obj_name" of String, parameter "expressionset_ref" of
           String
        :returns: instance of type "getExprMatrixOutput" -> structure:
           parameter "exprMatrix_FPKM_ref" of String, parameter
           "exprMatrix_TPM_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_expressionMatrix

        fpkm_ref, tpm_ref = self.expr_matrix_utils.get_expression_matrix(params)

        returnVal = {'exprMatrix_FPKM_ref': fpkm_ref,
                     'exprMatrix_TPM_ref': tpm_ref}

        #END get_expressionMatrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_expressionMatrix return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def search_expressionMatrix_by_geneID(self, ctx, params):
        """
        :param params: instance of type "SearchExprMatrixByGeneIDParams" ->
           structure: parameter "exprMatrix_ref" of String, parameter
           "gene_id" of String, parameter "start" of Long, parameter "limit"
           of Long
        :returns: instance of type "SearchExprMatrixByGeneIDResult"
           (num_found - number of all items found in query search) ->
           structure: parameter "start" of Long, parameter "values" of list
           of Double, parameter "num_found" of Long
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN search_expressionMatrix_by_geneID

        result = self.indexer.search_exprMatrix_by_geneID(ctx['token'],
                                                          params.get('exprMatrix_ref'),
                                                          query)
        #END search_expressionMatrix_by_geneID

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search_expressionMatrix_by_geneID return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
