
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
 * <p>Original spec-file type: SearchExprMatrixByGeneIDParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "exprMatrix_ref",
    "gene_id",
    "start",
    "limit"
})
public class SearchExprMatrixByGeneIDParams {

    @JsonProperty("exprMatrix_ref")
    private String exprMatrixRef;
    @JsonProperty("gene_id")
    private String geneId;
    @JsonProperty("start")
    private Long start;
    @JsonProperty("limit")
    private Long limit;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("exprMatrix_ref")
    public String getExprMatrixRef() {
        return exprMatrixRef;
    }

    @JsonProperty("exprMatrix_ref")
    public void setExprMatrixRef(String exprMatrixRef) {
        this.exprMatrixRef = exprMatrixRef;
    }

    public SearchExprMatrixByGeneIDParams withExprMatrixRef(String exprMatrixRef) {
        this.exprMatrixRef = exprMatrixRef;
        return this;
    }

    @JsonProperty("gene_id")
    public String getGeneId() {
        return geneId;
    }

    @JsonProperty("gene_id")
    public void setGeneId(String geneId) {
        this.geneId = geneId;
    }

    public SearchExprMatrixByGeneIDParams withGeneId(String geneId) {
        this.geneId = geneId;
        return this;
    }

    @JsonProperty("start")
    public Long getStart() {
        return start;
    }

    @JsonProperty("start")
    public void setStart(Long start) {
        this.start = start;
    }

    public SearchExprMatrixByGeneIDParams withStart(Long start) {
        this.start = start;
        return this;
    }

    @JsonProperty("limit")
    public Long getLimit() {
        return limit;
    }

    @JsonProperty("limit")
    public void setLimit(Long limit) {
        this.limit = limit;
    }

    public SearchExprMatrixByGeneIDParams withLimit(Long limit) {
        this.limit = limit;
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
        return ((((((((((("SearchExprMatrixByGeneIDParams"+" [exprMatrixRef=")+ exprMatrixRef)+", geneId=")+ geneId)+", start=")+ start)+", limit=")+ limit)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
