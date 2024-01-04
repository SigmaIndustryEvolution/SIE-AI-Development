/**
 *
 */
package com.sigma.safari.filter;

import com.raise.image.filter.RaiseFilter;
import com.raise.image.filter.RaiseFilterException;
import com.raise.image.filter.tools.AbstractFilter;
import com.sigma.safari.filter.parameters.FeatureDetectionParameters;
import com.sigma.safari.filter.tools.FeatureDetectionOpenCVOp;
import com.sigma.safari.filter.tools.FeatureDetectionScanOp;

import java.awt.image.BufferedImage;

public class FeatureDetectionFilter extends RaiseFilter {
	private FeatureDetectionParameters p;

	public FeatureDetectionFilter(FeatureDetectionParameters parameters) {
		this.p = parameters;
	}

	@Override
	public RaiseFilter filter(BufferedImage image) throws RaiseFilterException {
		AbstractFilter filterOp;

		switch (this.p.algorithm) {
			case Scan: filterOp = new FeatureDetectionScanOp(this.p); break;
			case OpenCV_Haar: filterOp = new FeatureDetectionOpenCVOp(this.p); break;
			default: throw new RaiseFilterException("Unsupported feature detection algorithm '" + this.p.algorithm);
		}

		this.destImage = filterOp.filter(image, this.destImage);

		return this;
	}

	@Override
	public String toString() {
		return "AKLow: " + this.p;
	}
}
