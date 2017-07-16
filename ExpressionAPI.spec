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
};
