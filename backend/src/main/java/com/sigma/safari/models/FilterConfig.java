package com.sigma.safari.models;

import com.raise.image.filter.models.FilterType;
import com.raise.image.filter.parameters.IRaiseFilterParameters;

public class FilterConfig {
    public FilterType type;
    public IRaiseFilterParameters parameters;

    public FilterConfig(FilterType type, IRaiseFilterParameters parameters) {
        this.type = type;
        this.parameters = parameters;
    }

    @Override
    public String toString() {
        return "Type: " + this.type;
    }
}
