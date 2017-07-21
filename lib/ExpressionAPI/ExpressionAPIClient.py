# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class ExpressionAPI(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def get_expressionMatrix(self, params, context=None):
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
        return self._client.call_method(
            'ExpressionAPI.get_expressionMatrix',
            [params], self._service_ver, context)

    def search_expressionMatrix_by_geneID(self, params, context=None):
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
        return self._client.call_method(
            'ExpressionAPI.search_expressionMatrix_by_geneID',
            [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('ExpressionAPI.status',
                                        [], self._service_ver, context)
