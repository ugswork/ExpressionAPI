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

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
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
