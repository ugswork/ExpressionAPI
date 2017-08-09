
package us.kbase.expressionapi;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: getDiffExprMatrixParams</p>
 * <pre>
 * *
 * Following are the required input parameters to get Differential Expression Matrix json object
 *     *
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "diffExprMatrixSet_ref"
})
public class GetDiffExprMatrixParams {

    @JsonProperty("diffExprMatrixSet_ref")
    private String diffExprMatrixSetRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("diffExprMatrixSet_ref")
    public String getDiffExprMatrixSetRef() {
        return diffExprMatrixSetRef;
    }

    @JsonProperty("diffExprMatrixSet_ref")
    public void setDiffExprMatrixSetRef(String diffExprMatrixSetRef) {
        this.diffExprMatrixSetRef = diffExprMatrixSetRef;
    }

    public GetDiffExprMatrixParams withDiffExprMatrixSetRef(String diffExprMatrixSetRef) {
        this.diffExprMatrixSetRef = diffExprMatrixSetRef;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("GetDiffExprMatrixParams"+" [diffExprMatrixSetRef=")+ diffExprMatrixSetRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
