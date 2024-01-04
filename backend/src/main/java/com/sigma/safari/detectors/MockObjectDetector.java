package com.sigma.safari.detectors;

import com.raise.image.quality.RaiseDetector;
import com.raise.image.quality.DetectionResult;
import com.raise.image.filter.RaiseFilterException;

import java.awt.image.BufferedImage;

import static org.bytedeco.opencv.global.opencv_imgproc.cvResize;
import static org.bytedeco.opencv.helper.opencv_imgcodecs.cvLoadImage;

enum SafariObjects {
    ALPHA("ALPHA-MICRORIB"),
    CONDOOR("CONDOOR"),
    CRAWFORD("CRAWFOORD"),
    HORMANN("HORMANN"),
    NOVOFERM("NOVOFERM");

    private String myObjectName;

    SafariObjects(String objectName) {
        this.myObjectName = objectName;
    }

    @Override
    public String toString() {
        return this.myObjectName;
    }
}

public class MockObjectDetector extends RaiseDetector {
    private BufferedImage images[];
    public MockObjectDetector(BufferedImage image1, BufferedImage image2, BufferedImage image3) {
        this.images = new BufferedImage[] { image1, image2, image3 };
    }

    public DetectionResult detect() throws RaiseFilterException {
        return this.detect(this.images);
    }

    @Override
    public DetectionResult detect(BufferedImage ...sources) throws RaiseFilterException {
        DetectionResult[] predictions = new DetectionResult[] {
                new DetectionResult(SafariObjects.ALPHA.name(), (int) Math.round(Math.random() * 100)),
                new DetectionResult(SafariObjects.CONDOOR.name(), (int) Math.round(Math.random() * 100)),
                new DetectionResult(SafariObjects.CRAWFORD.name(), (int) Math.round(Math.random() * 100)),
                new DetectionResult(SafariObjects.HORMANN.name(), (int) Math.round(Math.random() * 100)),
                new DetectionResult(SafariObjects.NOVOFERM.name(), (int) Math.round(Math.random() * 100))
        };

        return DetectionResult.combine(predictions);
    }

    @Override
    public String toString() {
        return null;
    }
}
