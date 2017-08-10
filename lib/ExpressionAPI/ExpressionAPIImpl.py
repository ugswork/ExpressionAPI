# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import sys
import time
from core.diffExprMatrix_utils import DiffExprMatrixUtils
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
    GIT_URL = "https://github.com/ugswork/ExpressionAPI.git"
    GIT_COMMIT_HASH = "98391d5e5636b8f21cc3a6919205758266fd92fb"

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
        self.ws_url = config['workspace-url']
        self.diffexpr_matrix_utils = DiffExprMatrixUtils(config, self.__LOGGER)
        #END_CONSTRUCTOR
        pass


    def get_differentialExpressionMatrixSet(self, ctx, params):
        """
        :param params: instance of type "getDiffExprMatrixParams" (*
           Following are the required input parameters to get Differential
           Expression Matrix json object *) -> structure: parameter
           "diffExprMatrixSet_ref" of String
        :returns: instance of type "getDiffExprMatrixOutput" -> structure:
           parameter "volcano_plot_data" of unspecified object, parameter
           "json_filepath" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_differentialExpressionMatrixSet

        plot_data = self.diffexpr_matrix_utils.get_diffexpr_matrixset(params, ctx['token'])

        returnVal = {'volcano_plot_data': plot_data}

        #END get_differentialExpressionMatrixSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_differentialExpressionMatrixSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
