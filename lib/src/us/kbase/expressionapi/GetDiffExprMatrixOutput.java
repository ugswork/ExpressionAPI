
package us.kbase.expressionapi;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: getDiffExprMatrixOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "volcano_plot_data",
    "json_filepath"
})
public class GetDiffExprMatrixOutput {

    @JsonProperty("volcano_plot_data")
    private UObject volcanoPlotData;
    @JsonProperty("json_filepath")
    private String jsonFilepath;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("volcano_plot_data")
    public UObject getVolcanoPlotData() {
        return volcanoPlotData;
    }

    @JsonProperty("volcano_plot_data")
    public void setVolcanoPlotData(UObject volcanoPlotData) {
        this.volcanoPlotData = volcanoPlotData;
    }

    public GetDiffExprMatrixOutput withVolcanoPlotData(UObject volcanoPlotData) {
        this.volcanoPlotData = volcanoPlotData;
        return this;
    }

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
        return ((((((("GetDiffExprMatrixOutput"+" [volcanoPlotData=")+ volcanoPlotData)+", jsonFilepath=")+ jsonFilepath)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
