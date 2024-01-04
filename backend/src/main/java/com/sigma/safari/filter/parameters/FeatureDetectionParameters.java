package com.sigma.safari.filter.parameters;

import com.raise.image.filter.RaiseFilterException;
import com.raise.image.filter.parameters.IRaiseFilterParameters;
import com.raise.image.tools.PixelHelper;
import org.json.JSONObject;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class FeatureDetectionParameters implements IRaiseFilterParameters {
    public File file;
    public FeatureDetectionAlgorithm algorithm;
    public boolean[][] featureMatrix = new boolean[0][0];

    public FeatureDetectionParameters(File file, FeatureDetectionAlgorithm algorithm) throws IOException, RaiseFilterException {
        this.file = file;
        this.algorithm = algorithm;

        if (this.algorithm == FeatureDetectionAlgorithm.Scan) {
            BufferedImage image = ImageIO.read(file);
            this.featureMatrix = PixelHelper.getBwPixels(image);
        }
    }

    public FeatureDetectionParameters(JSONObject parameter) throws IOException, RaiseFilterException {
        this(
                new File(parameter.getString("file")),
                FeatureDetectionAlgorithm.valueOf(parameter.getString("algorithm"))
        );
    }

    public FeatureDetectionParameters(boolean[][] featureMatrix) {
        this.featureMatrix = featureMatrix;
    }

    @Override
    public String toString() {
        int side = this.featureMatrix.length;

        StringBuffer str = new StringBuffer();
        for(int x = 0; x < side; x++) {
            for(int y = 0; y < side; y++) {
                str.append(this.featureMatrix[x][y] ? "W" : ".");
            }
            str.append("\n");
        }
        return "Feature: [\n" + str + "\n]";
    }
}
