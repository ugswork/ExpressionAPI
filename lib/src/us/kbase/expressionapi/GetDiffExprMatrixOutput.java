
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
 * <p>Original spec-file type: getDiffExprMatrixOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "json_filepath"
})
public class GetDiffExprMatrixOutput {

    @JsonProperty("json_filepath")
    private String jsonFilepath;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("json_filepath")
    public String getJsonFilepath() {
        return jsonFilepath;
    }

    @JsonProperty("json_filepath")
    public void setJsonFilepath(String jsonFilepath) {
        this.jsonFilepath = jsonFilepath;
    }

    public GetDiffExprMatrixOutput withJsonFilepath(String jsonFilepath) {
        this.jsonFilepath = jsonFilepath;
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
        return ((((("GetDiffExprMatrixOutput"+" [jsonFilepath=")+ jsonFilepath)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
