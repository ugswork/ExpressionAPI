
package us.kbase.expressionapi;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: SearchExprMatrixByGeneIDResult</p>
 * <pre>
 * num_found - number of all items found in query search
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "start",
    "values",
    "num_found"
})
public class SearchExprMatrixByGeneIDResult {

    @JsonProperty("start")
    private Long start;
    @JsonProperty("values")
    private List<Double> values;
    @JsonProperty("num_found")
    private Long numFound;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("start")
    public Long getStart() {
        return start;
    }

    @JsonProperty("start")
    public void setStart(Long start) {
        this.start = start;
    }

    public SearchExprMatrixByGeneIDResult withStart(Long start) {
        this.start = start;
        return this;
    }

    @JsonProperty("values")
    public List<Double> getValues() {
        return values;
    }

    @JsonProperty("values")
    public void setValues(List<Double> values) {
        this.values = values;
    }

    public SearchExprMatrixByGeneIDResult withValues(List<Double> values) {
        this.values = values;
        return this;
    }

    @JsonProperty("num_found")
    public Long getNumFound() {
        return numFound;
    }

    @JsonProperty("num_found")
    public void setNumFound(Long numFound) {
        this.numFound = numFound;
    }

    public SearchExprMatrixByGeneIDResult withNumFound(Long numFound) {
        this.numFound = numFound;
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
        return ((((((((("SearchExprMatrixByGeneIDResult"+" [start=")+ start)+", values=")+ values)+", numFound=")+ numFound)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
