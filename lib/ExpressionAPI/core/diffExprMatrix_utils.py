import os
import uuid
import re
import json
from pprint import pprint, pformat

from Workspace.WorkspaceClient import Workspace

class DiffExprMatrixUtils:
    """
     Constains a set of functions for expression levels calculations.
    """

    PARAM_IN_WS_NAME = 'workspace_name'
    PARAM_IN_OBJ_NAME = 'output_obj_name'
    PARAM_IN_DIFFEXPMATSET_REF = 'diffExprMatrixSet_ref'

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger
        self.scratch = os.path.join(config['scratch'], 'DEM_' + str(uuid.uuid4()))
        self.ws_url = config['workspace-url']
        self.ws_client = Workspace(self.ws_url)
        self._mkdir_p(self.scratch)
        pass

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def process_params(self, params):
        """
        validates params passed to gen expression matrix method
        """
        for p in [self.PARAM_IN_DIFFEXPMATSET_REF]:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def get_expressionset_data(self, expressionset_ref):

        expr_set_obj = self.ws_client.get_objects2(
            {'objects': [{'ref': expressionset_ref}]})['data'][0]

        expr_set_obj_type = expr_set_obj.get('info')[2]
        expr_set_data = dict()
        expr_set_data['ws_name'] = expr_set_obj.get('info')[7]
        expr_set_data['obj_name'] = expr_set_obj.get('info')[1]

        if re.match('KBaseRNASeq.RNASeqExpressionSet-\d.\d', expr_set_obj_type):
            expr_set_data['genome_ref'] = expr_set_obj['data']['genome_id']
            expr_obj_refs = list()
            for expr_obj in expr_set_obj['data']['mapped_expression_ids']:
                expr_obj_refs.append(expr_obj.values()[0])
            expr_set_data['expr_obj_refs'] = expr_obj_refs

        elif re.match('KBaseSets.ExpressionSet-\d.\d', expr_set_obj_type):
            items = expr_set_obj.get('data').get('items')
            expr_obj_refs = list()
            for item in items:
                expr_obj_refs.append(item['ref'])
            expr_obj = self.ws_client.get_objects2(
                {'objects': [{'ref': expr_obj_refs[0]}]})['data'][0]
            expr_set_data['genome_ref'] = expr_obj['data']['genome_id']
            expr_set_data['expr_obj_refs'] = expr_obj_refs
        else:
            raise TypeError(self.PARAM_IN_EXPSET_REF + ' should be of type ' +
                            'KBaseRNASeq.RNASeqExpressionSet ' +
                            'or KBaseSets.ExpressionSet')
        return expr_set_data

    def get_diffexpr_matrix(self, params):

        col_names = {'gene_id': 'gene',
                     'log2_fold_change': 'log2fc_f',
                     'p_value': 'p_value_f',
                     'q_value': 'q_value'}

        json_fields = ['log2fc_f', 'p_value_f', 'q_value']

        self.process_params(params)

        diffexprmatset_list = list()
        diffexprmatset_ref = params.get(self.PARAM_IN_DIFFEXPMATSET_REF)

        diffexprmatset_obj = self.ws_client.get_objects2(
                                {'objects': [{'ref': diffexprmatset_ref}]})['data'][0]

        items = diffexprmatset_obj.get('data').get('items')
        diffexprmat_refs = list()

        for item in items:
            diffexprmat_refs.append(item['ref'])
            self.logger.info('DiffExprMatrix ref: ' + item['ref'])

        for diffexprmat_ref in diffexprmat_refs:
            diffexprmat_dict = dict()
            diffexprmat_obj = self.ws_client.get_objects2(
                                {'objects': [{'ref': diffexprmat_ref}]})['data'][0]
            diffexprmat = diffexprmat_obj.get('data')
            diffexprmat_dict['condition_1'] = diffexprmat.get('condition_mapping').keys()[0]
            diffexprmat_dict['condition_2'] = diffexprmat.get('condition_mapping').values()[0]
            voldata = list()
            data = diffexprmat.get('data')

            for row_index, row_id in enumerate(data.get('row_ids')):
                row_data = dict()
                row_data['gene'] = row_id
                values = data.get('values')[row_index]
                for col_index in range(len(values)):
                    row_data[json_fields[col_index]] = values[col_index]

                voldata.append(row_data)

            diffexprmat_dict['voldata'] = voldata
            diffexprmatset_list.append(diffexprmat_dict)

        json_outfile = os.path.join(self.scratch, 'dems.json')
        with open(json_outfile, 'w+') as outfile:
            json.dump(diffexprmatset_list, outfile, sort_keys=True, indent=4)

        return diffexprmatset_list, json_outfile





