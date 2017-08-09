/*
A KBase module: ExpressionAPI
*/

module ExpressionAPI {
    /*
        Get Differential Expression Matrix from Expression Set input
    */

    /**
        Following are the required input parameters to get Differential Expression Matrix json object
    **/

    typedef structure {

        string      diffExprMatrixSet_ref;

    } getDiffExprMatrixParams;

    typedef structure {

        UnspecifiedObject   volcano_plot_data;
        string              json_filepath;

    } getDiffExprMatrixOutput;

    funcdef  get_differentialExpressionMatrix(getDiffExprMatrixParams params)
                                     returns (getDiffExprMatrixOutput)
                                     authentication required;
};
