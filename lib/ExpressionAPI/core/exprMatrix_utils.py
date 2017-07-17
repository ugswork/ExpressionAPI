import os
import uuid
from pprint import pprint, pformat

from Workspace.WorkspaceClient import Workspace
from DataFileUtil.DataFileUtilClient import DataFileUtil
from DataFileUtil.baseclient import ServerError as DFUError

class ExprMatrixUtils:
    """
     Constains a set of functions for expression levels calculations.
    """

    PARAM_IN_WS_NAME = 'workspace_name'
    PARAM_IN_OBJ_NAME = 'output_obj_name'
    PARAM_IN_EXPSET_REF = 'expressionset_ref'

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], 'EM_' + str(uuid.uuid4()))
        self.ws_url = config['workspace-url']
        self.ws_client = Workspace(self.ws_url)
        self.dfu = DataFileUtil(self.callback_url)
        pass

    def process_params(self, params):
        """
        validates params passed to gen expression matrix method
        """
        for p in [self.PARAM_IN_EXPSET_REF,
                  self.PARAM_IN_OBJ_NAME,
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

        expr_set = self.ws_client.get_objects2(
            {'objects': [{'ref': expressionset_ref}]})['data'][0]

        expr_set_data = dict()
        if expr_set.get('info')[2].startswith('KBaseRNASeq.RNASeqExpressionSet'):
            pprint(expr_set)

            expr_set_data['ws_name'] = expr_set['info'][7]
            expr_set_data['obj_name'] = expr_set['info'][1]
            expr_set_data['genome_ref'] = expr_set['data']['genome_id']
            expr_obj_names = list()
            for expr_obj in expr_set['data']['mapped_expression_objects']:  # better with ids
                expr_obj_names.append(expr_obj.values()[0])
            expr_set_data['expr_obj_names'] = expr_obj_names
        elif expr_set.get('info')[2].startswith('KBaseSets.ExpressionSet'):
            pass
        else:
            raise TypeError('"{}" should be of type KBaseRNASeq.RNASeqExpressionSet ' +
                            'or KBaseSets.ExpressionSet'.format(self.PARAM_IN_EXPSET_REF))
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

    def get_expression_matrix(self, params):

        self.process_params(params)
        self.params = params

        expressionset_ref = params.get(self.PARAM_IN_EXPSET_REF)

        expr_set_data = self.get_expressionset_data(expressionset_ref)
        fpkm_tables = []
        tpm_tables = []
        tpm_table = None
        for expr_obj_name in expr_set_data['expr_obj_names']:
            try:
                self.logger.info('*** getting expression set {0} from workspace ****'
                                 .format(expr_obj_name))

                expr = self.ws_client.get_objects([{'name': expr_obj_name,
                                                    'workspace': expr_set_data['ws_name']}])[0]
            except Exception, e:
                self.logger.exception(e)
                raise Exception('Unable to download expression object {0} from workspace {1}'.
                                format(expr_obj_name, expr_set_data['ws_name']))

            num_interp = expr['data']['numerical_interpretation']
            if num_interp != 'FPKM':
                raise Exception(
                    'Did not get expected FPKM value from numerical interpretation key from \
                     Expression object {0}, instead got '.format(expr_obj_name, num_interp))

            pr_comments = expr['data']['processing_comments']  # log2 Normalized
            self.logger.info('pr_comments are {0}'.format(pr_comments))

            fpkm_table = expr['data']['expression_levels']  # QUESTION: is this really FPKM levels?
            self.logger.info('FPKM keycount: {0}'.format(len(fpkm_table.keys())))
            fpkm_tables.append(fpkm_table)

            tpm_table = None  # Cufflinks doesn't generate TPM
            if 'tpm_expression_levels' in expr['data']:  # so we need to check for this key
                tpm_table = expr['data']['tpm_expression_levels']
                self.logger.info('TPM keycount: {0}'.format(len(tpm_table.keys())))
                tpm_tables.append(tpm_table)

        output_obj_name = params.get(self.PARAM_IN_OBJ_NAME)
        fpkm_ref = self.save_expression_matrix(fpkm_tables,
                                            expr_set_data,
                                            '{0}_FPKM_ExpressionMatrix'.format(output_obj_name))
        tpm_ref = None
        if tpm_table is not None:
            tpm_ref = self.save_expression_matrix(tpm_tables,
                                               expr_set_data,
                                               '{0}_TPM_ExpressionMatrix'.format(output_obj_name))
        return fpkm_ref, tpm_ref

