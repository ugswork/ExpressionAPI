# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time
import inspect
import shutil

from os import environ

try:
    from ConfigParser import ConfigParser  # py2
except BaseException:
    from configparser import ConfigParser  # py3

import pprint

from biokbase.workspace.client import Workspace as workspaceService
from ExpressionAPI.ExpressionAPIImpl import ExpressionAPI
from ExpressionAPI.ExpressionAPIServer import MethodContext
from ExpressionAPI.authclient import KBaseAuth as _KBaseAuth

class DiffExprMatrixUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('ExpressionAPI'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        # authServiceUrlAllowInsecure = cls.cfg['auth_service_url_allow_insecure']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'ExpressionAPI',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = ExpressionAPI(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        suffix = int(time.time() * 1000)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    def get_diff_expr_matrix_success(self, input_diffexprmatrixset_ref):

        test_name = inspect.stack()[1][3]
        print('\n*** starting expected get diff expr matrix success test: ' + test_name + ' *****************')

        params = {'diffExprMatrixSet_ref': input_diffexprmatrixset_ref
                  }

        getDiffExprMat_retVal = self.getImpl().get_differentialExpressionMatrixSet(self.ctx, params)[0]

        pp = pprint.PrettyPrinter(depth=6)

        plot_data = getDiffExprMat_retVal.get('volcano_plot_data')

        '''
        print("============ VOLCANO PLOT DATA  ==============")
        pp.pprint(plot_data)
        print("==========================================================")
        '''

    # Following test uses object refs from a narrative in appdev. Comment the next line to run the test
    @unittest.skip("skipped test_get_expr_matrix_rnaseq_exprset_success")
    def test_get_appdev_diff_expr_matrix_success(self):

        appdev_diffexpr_matrixset_obj_ref = '5264/11/1'
        appdev_diffexpr_matrixset_obj_ref = '5264/7/2'
        appdev_diffexpr_matrixset_obj_name = 'cuffdiff_diff_exp_out'

        appdev_three_by_two_diffexpr_matrixset_obj_ref = '5264/17/1'
        appdev_three_by_two_diffexpr_matrixset_obj_name = 'three_by_two_diffexp_output'

        self.get_diff_expr_matrix_success(appdev_three_by_two_diffexpr_matrixset_obj_ref)

    # Following test uses object refs from a narrative in ci. Comment the next line to run the test
    #@unittest.skip("skipped test_get_expr_matrix_rnaseq_exprset_success")
    def test_get_ci_diff_expr_matrix_success(self):

        ci_diffexpr_matrixset_obj_ref = '19647/7/5'

        self.get_diff_expr_matrix_success(ci_diffexpr_matrixset_obj_ref)

    '''
    def fail_getDiffExprMat(self, params, error, exception=ValueError, do_startswith=False):

        test_name = inspect.stack()[1][3]
        print('\n*** starting expected get Expression Matrix fail test: ' + test_name + ' **********************')

        with self.assertRaises(exception) as context:
            self.getImpl().get_differentialExpressionMatrixSet(self.ctx, params)
        if do_startswith:
            self.assertTrue(str(context.exception.message).startswith(error),
                            "Error message {} does not start with {}".format(
                                str(context.exception.message),
                                error))
        else:
            self.assertEqual(error, str(context.exception.message))

    def test_getDiffExprMat_fail_no_ws_name(self):
        self.fail_getDiffExprMat(
            {
                'diffExprMatrixSet_ref': '1/1/1'
            },
            '"workspace_name" parameter is required, but missing')

    def test_getDiffExprMat_fail_no_obj_name(self):
        self.fail_getDiffExprMat(
            {
                'workspace_name': self.getWsName(),
                'diffExprMatrixSet_ref': '1/1/1'
            },
            '"output_obj_name" parameter is required, but missing')

    def test_getDiffExprMat_fail_no_exprset_ref(self):
        self.fail_getDiffExprMat(
            {
                'workspace_name': self.getWsName(),
                'output_obj_name': 'test_diffExprMatrix'
            },
            '"expressionset_ref" parameter is required, but missing')

    def test_getDiffExprMat_fail_bad_wsname(self):
        self.fail_getDiffExprMat(
            {
                'workspace_name': '&bad',
                'diffExprMatrixSet_ref': '1/1/1',
                'output_obj_name': 'test_exprMatrix'
            },
            'Illegal character in workspace name &bad: &')

    def test_getDiffExprMat_fail_non_existant_wsname(self):
        self.fail_getDiffExprMat(
            {
                'workspace_name': '1s',
                'diffExprMatrixSet_ref': '1/1/1',
                'output_obj_name': 'test_exprMatrix'
            },
            'No workspace with name 1s exists')

    def test_getDiffExprMat_fail_non_expset_ref(self):
        self.fail_getDiffExprMat(
            {
                'workspace_name': self.getWsName(),
                'diffExprMatrixSet_ref': self.genome_ref,
                'output_obj_name': 'test_exprMatrix'
            },
            'diffExprMatrixSet_ref should be of type KBaseRNASeq.RNASeqExpressionSet ' +
            'or KBaseSets.ExpressionSet', exception=TypeError)
    '''

