package com.sigma.safari.service;

import com.raise.image.quality.DetectionResult;
import com.raise.image.filter.RaiseFilterException;
import com.sigma.safari.detectors.ProxyObjectDetector;

import java.awt.image.BufferedImage;
import java.io.InputStream;

public class SafariService {
    private static SafariService myInstance;

    private SafariService() {
    }

    public static SafariService getInstance() {
        if (myInstance == null) {
            myInstance = new SafariService();
        }

        return myInstance;
    }

    public DetectionResult predict(InputStream front, InputStream back, InputStream side) throws RaiseFilterException {
        ProxyObjectDetector detector = new ProxyObjectDetector(front, back, side);
        return detector.detect((BufferedImage) null);
    }
}
