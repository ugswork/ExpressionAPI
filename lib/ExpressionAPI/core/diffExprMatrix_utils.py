import os
import uuid
import re
import json
from pprint import pprint, pformat

from Workspace.WorkspaceClient import Workspace
from DataFileUtil.DataFileUtilClient import DataFileUtil
from DataFileUtil.baseclient import ServerError as DFUError

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
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], 'DEM_' + str(uuid.uuid4()))
        self.ws_url = config['workspace-url']
        self.ws_client = Workspace(self.ws_url)
        self.dfu = DataFileUtil(self.callback_url)
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
        for p in [self.PARAM_IN_DIFFEXPMATSET_REF,
                  self.PARAM_IN_WS_NAME
                 ]:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        ws_name_id = params.get(self.PARAM_IN_WS_NAME)
        if not isinstance(ws_name_id, int):
            try:
                ws_name_id = self.dfu.ws_name_to_id(ws_name_id)
            except DFUError as se:
                prefix = se.message.split('.')[0]
                raise ValueError(prefix)

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

    def save_expression_matrix(self, tables, expr_set_data, em_obj_name, hidden = 0):

        all_rows = {}    # build a dictionary of keys only which is a union of all row ids (gene_ids)
        self.logger.info( '***** length of tables is {0}'.format( len( tables )))
        for table in tables:
            for r in table.keys():
                all_rows[r] = []

        for gene_id in all_rows.keys():
            row = []
            for table in tables:
                if ( gene_id in table ):
                    #logger.info( 'append ' + gene_id )
                    #logger.info( pformat( table[gene_id]))
                               #all_rows[gene_id].append( table[gene_id] )
                    row.append( table[gene_id] )
                else:
                    #logger.info( 'append  0' )
                    row.append( 0 )
                all_rows[gene_id] = row
                #logger.info( all_rows[gene_id])

        em_data = {
                    'genome_ref': expr_set_data['genome_ref'],
                    'scale': 'log2',
                    'type': 'level',
                    'data': {
                            'row_ids': [],
                            'values': [],
                            'col_ids': expr_set_data['expr_obj_names']
                            },
                    'feature_mapping' : {}
                   }

        # we need to load row-by-row to preserve the order
        self.logger.info('loading expression matrix data')

        for gene_id in all_rows.keys():
            em_data['feature_mapping'][gene_id] = gene_id
            em_data['data']['row_ids'].append(gene_id)
            em_data['data']['values'].append( all_rows[gene_id] )
            em_data['feature_mapping'][gene_id] = gene_id   # QUESTION: What to do here?

        try:
            self.logger.info( 'saving em_data em_name {0}'.format(em_obj_name))
            obj_info = self.ws_client.save_objects({'workspace': self.params.get(self.PARAM_IN_WS_NAME),
                                                    'objects': [
                                                          { 'type': 'KBaseFeatureValues.ExpressionMatrix',
                                                            'data': em_data,
                                                            'name': em_obj_name,
                                                            'hidden': hidden
                                                          }
                                                    ]})[0]
            self.logger.info('ws save return:\n' + pformat(obj_info))
        except Exception as e:
            self.logger.exception(e)
            raise Exception('Failed Saving Expression Matrix to Workspace')

        return str(obj_info[6]) + '/' + str(obj_info[0]) + '/' + str(obj_info[4])

    def get_diffexpr_matrix(self, params):

        col_names = {'gene_id': 'gene',
                     'log2_fold_change': 'log2fc_f',
                     'p_value': 'p_value_f',
                     'q_value': 'q_value'}

        json_fields = ['log2fc_f', 'p_value_f', 'q_value']

        self.process_params(params)
        self.params = params

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

        return json_outfile





