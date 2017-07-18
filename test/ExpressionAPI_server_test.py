# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time

from os import environ

try:
    from ConfigParser import ConfigParser  # py2
except BaseException:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ExpressionAPI.ExpressionAPIImpl import ExpressionAPI
from ExpressionAPI.ExpressionAPIServer import MethodContext
from ExpressionAPI.authclient import KBaseAuth as _KBaseAuth

class ExpressionAPITest(unittest.TestCase):
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
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        suffix = int(time.time() * 1000)
        cls.wsName = "test_exprAPI_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})

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
    # Following test uses object refs from a narrative. Comment the next line to run the test
    #@unittest.skip("skipped test_cuffdiff_RNASeq_objects_success")
    def test_get_expr_matrix_RNASeq_object_success(self):
        """
        Input object: downsized_AT_reads_tophat_AlignmentSet_cufflinks_ExpressionSet (4389/45/1)
        Expected output object: downsized_AT_tophat_cufflinks_cuffdiff_output (4389/58/1)
        Files in output object should be the same as in expected output object
        """

        appdev_exprset_obj_ref1 = '4389/18/2'
        appdev_exprset_obj_name1 = 'downsized_AT_reads_hisat2_AlignmentSet_stringtie_ExpressionSet'

        appdev_exprset_obj_ref2 = '4389/45/1'
        appdev_exprset_obj_name2 = 'downsized_AT_reads_tophat_AlignmentSet_cufflinks_ExpressionSet'

        self.expressionset_ref = appdev_exprset_obj_ref1

        params = {'expressionset_ref': appdev_exprset_obj_ref1,
                  'workspace_name': self.getWsName(),
                  'output_obj_name': 'test_exprAPI',
                  'test_ws_name': 'mccorkle:1490980504571',
                  'test_obj_name': appdev_exprset_obj_name1
                  }

        getExprMat_retVal = self.getImpl().get_expressionMatrix(self.ctx, params)[0]

        inputObj = self.dfu.get_objects(
            {'object_refs': [self.expressionset_ref]})['data'][0]

        print("============ INPUT EXPRESSION SET OBJECT ==============")
        pprint(inputObj)
        print("==========================================================")

        fpkm_ref = getExprMat_retVal.get('exprMatrix_FPKM_ref')
        tpm_ref = getExprMat_retVal.get('exprMatrix_TPM_ref')

        outputFPKM_Obj = self.dfu.get_objects(
            {'object_refs': [fpkm_ref]})['data'][0]

        print("============  EXPRESSION MATRIX FPKM OUTPUT  ==============")
        pprint(outputFPKM_Obj)
        print("==========================================================")


        outputTPM_Obj = self.dfu.get_objects(
            {'object_refs': [tpm_ref]})['data'][0]

        print("============  EXPRESSION MATRIX TPM OUTPUT  ==============")
        pprint(outputTPM_Obj)
        print("==========================================================")

    '''
    def fail_getExprMat(self, params, error, exception=ValueError, do_startswith=False):

        test_name = inspect.stack()[1][3]
        print('\n*** starting expected get Expression Matrix fail test: ' + test_name + ' **********************')

        with self.assertRaises(exception) as context:
            self.getImpl().run_Cuffdiff(self.ctx, params)
        if do_startswith:
            self.assertTrue(str(context.exception.message).startswith(error),
                            "Error message {} does not start with {}".format(
                                str(context.exception.message),
                                error))
        else:
            self.assertEqual(error, str(context.exception.message))

    def test_getExprMat_fail_no_ws_name(self):
        self.fail_getExprMat(
            {
                'expressionset_ref': self.expressionset_ref,
                'output_obj_name': 'test_exprMatrix'
            },
            '"workspace_name" parameter is required, but missing')

    def test_getExprMat_fail_no_obj_name(self):
        self.fail_getExprMat(
            {
                'workspace_name': self.getWsName(),
                'expressionset_ref': self.expressionset_ref
            },
            '"output_obj_name" parameter is required, but missing')

    def test_getExprMat_fail_no_exprset_ref(self):
        self.fail_getExprMat(
            {
                'workspace_name': self.getWsName(),
                'output_obj_name': 'test_exprMatrix'
            },
            '"expressionset_ref" parameter is required, but missing')

    def test_getExprMat_fail_bad_wsname(self):
        self.fail_getExprMat(
            {
                'workspace_name': '&bad',
                'expressionset_ref': self.expressionset_ref,
                'output_obj_name': 'test_exprMatrix'
            },
            'Illegal character in workspace name &bad: &')

    def test_getExprMat_fail_non_existant_wsname(self):
        self.fail_getExprMat(
            {
                'workspace_name': '1s',
                'expressionset_ref': self.expressionset_ref,
                'output_obj_name': 'test_exprMatrix'
            },
            'No workspace with name 1s exists')

    def test_getExprMat_fail_non_expset_ref(self):
        self.fail_getExprMat(
            {
                'workspace_name': self.getWsName(),
                'expressionset_ref': self.reads_ref_1,
                'output_obj_name': 'test_exprMatrix'
            },
            '"expressionset_ref" should be of type KBaseRNASeq.RNASeqExpressionSet',
            exception=TypeError)
    '''
