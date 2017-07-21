/*
A KBase module: ExpressionAPI
*/

module ExpressionAPI {
    /*
        Get Expression Matrix from Expression Set input
    */

    /**
        Following are the required input parameters to get Expression Matrix
    **/

    typedef structure {

        string      workspace_name;
        string      output_obj_name;
        string      expressionset_ref;

    } getExprMatrixParams;

    typedef structure {

        string   exprMatrix_FPKM_ref;
        string   exprMatrix_TPM_ref;

    } getExprMatrixOutput;

    funcdef  get_expressionMatrix(getExprMatrixParams params)
                                   returns (getExprMatrixOutput)
                                   authentication required;

    typedef structure {
        string  exprMatrix_ref;
        string  gene_id;
        int     start;
        int     limit;
    } SearchExprMatrixByGeneIDParams;

    /*
        num_found - number of all items found in query search
    */
    typedef structure {
        int         start;
        list<float> values;
        int         num_found;
    } SearchExprMatrixByGeneIDResult;

    funcdef search_expressionMatrix_by_geneID(SearchExprMatrixByGeneIDParams params)
        returns (SearchExprMatrixByGeneIDResult result) authentication optional;
};
