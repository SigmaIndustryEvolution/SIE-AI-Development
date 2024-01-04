package com.sigma.safari;

import com.raise.image.quality.DetectionResult;
import com.raise.image.filter.RaiseFilter;
import com.raise.image.filter.RaiseFilterException;
import com.raise.image.filter.models.FilterType;
import com.raise.image.filter.parameters.IRaiseFilterParameters;
import com.raise.image.filter.parameters.RaiseFilterParameterHelper;
import com.raise.services.FilterService;
import com.sigma.safari.detectors.TensorflowObjectDetector;
import com.sigma.safari.filter.FeatureDetectionFilter;
import com.sigma.safari.filter.parameters.FeatureDetectionParameters;
import com.sigma.safari.models.FilterConfig;
import org.json.JSONArray;
import org.json.JSONObject;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

public class SafariLab {

    public static final List<String> SUPPORTED_FORMATS = Arrays.asList(
            "gif",
            "png",
            "bmp",
            "tif",
            "tiff",
            "jpeg",
            "jpg",
            "wbmp"
    );

    public static void main(String[] args) {
        try {
            if (args.length != 2) {
                throw new Exception("Usage: <inputfilename> <outputfilename>");
            }

            SafariLab lab = new SafariLab(args[0], args[1], "filter.json");

            lab.run();
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Error reading or filtering image! - " + e.toString());
        }
    }

    private List<FilterConfig> filters;
    private BufferedImage image;
    private File outputFile;

    SafariLab(String inputFilename, String outputFilename, String filterConfigFilename) throws IOException {
        this.filters = this.readFilterConfig(filterConfigFilename);
        System.err.println("Reading '" + inputFilename + "'");
        this.image = ImageIO.read(new File(inputFilename));
        this.outputFile = new File(outputFilename);
    }

    private void run() throws RaiseFilterException, IOException {
        String fileFormat = outputFile.getName().substring(outputFile.getName().lastIndexOf(".") + 1).toLowerCase(Locale.ROOT);

        if (!SafariLab.SUPPORTED_FORMATS.contains(fileFormat)) {
            throw new Error("Unsupported format '" + fileFormat + "'! Supported formats are: " + SafariLab.SUPPORTED_FORMATS.toString());
        }

        FilterService service = FilterService.getInstance();

        int originalWidth = image.getWidth();
        int originalHeight = image.getHeight();

        TensorflowObjectDetector tw = new TensorflowObjectDetector();

        DetectionResult q = tw.detect(image);
        System.err.println("Tensorflow match rate: " + q);

        System.err.println("Input image: " + originalWidth + "x" + originalHeight);
        for (FilterConfig filterConfig : this.filters) {
            if (filterConfig.type == FilterType.FeatureDetection) {
                RaiseFilter fd1Filter = new FeatureDetectionFilter((FeatureDetectionParameters) filterConfig.parameters);
                image = service.filter(fd1Filter, image);
            } else {
                image = service.filter(filterConfig.type, filterConfig.parameters, image);
            }
        }

        boolean result = ImageIO.write(image, fileFormat, outputFile);

        if (!result) {
            throw new Error("Unsupported file format '" + fileFormat + "'! If this is a gray scale image, it can only be written to tiff.");
        }

        System.err.println("Wrote output file to " + outputFile);
    }

    private List<FilterConfig> readFilterConfig(String filename) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(filename)));

        JSONArray array = new JSONArray(content);

        List<FilterConfig> filters = new ArrayList();
        for(Object o : array) {
            JSONObject node = (JSONObject) o;

            try {
                FilterType filterType = FilterType.valueOf(node.getString("type"));
                IRaiseFilterParameters filterParameters;
                if (filterType == FilterType.FeatureDetection) {
                    filterParameters = new FeatureDetectionParameters(node.getJSONObject("parameters"));
                } else {
                    filterParameters = RaiseFilterParameterHelper.parse(filterType, node.getJSONObject("parameters"));
                }
                filters.add(new FilterConfig(filterType, filterParameters));
            } catch (Exception e) {
                System.err.println("Configuration error for filter type '" + node.getString("type") + "'! Skipping this filter.");
                e.printStackTrace();
            }

        }
        return filters;
    }
}
