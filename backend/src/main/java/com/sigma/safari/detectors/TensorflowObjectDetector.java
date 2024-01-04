package com.sigma.safari.detectors;

import com.raise.image.quality.RaiseDetector;
import com.raise.image.quality.DetectionResult;
import com.raise.image.filter.RaiseFilterException;

import java.awt.image.BufferedImage;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.bytedeco.opencv.opencv_core.CvScalar;
import org.bytedeco.opencv.opencv_core.IplImage;
import org.tensorflow.Graph;
import org.tensorflow.Session;
import org.tensorflow.Tensor;

import static org.bytedeco.opencv.global.opencv_core.cvGet2D;
import static org.bytedeco.opencv.global.opencv_imgproc.cvResize;
import static org.bytedeco.opencv.helper.opencv_imgcodecs.cvLoadImage;

public class TensorflowObjectDetector extends RaiseDetector {

    public class ImageProcessor {
        /* Constants specific to trained model
         * All RGB values are converted to normalized float values
         * using this formula (value - mean) / scale
         * */
        private final int height = 224;
        private final int width = 224;
        private final float mean = 117f;
        private final float scale = 1f;


        public ImageProcessor() {
        }

        public float[][][][] loadAndNormalizeImages(String... path) {
            //First dimension of the result is a number of images, because we may accept multiple paths
            float[][][][] result = new float[path.length][height][width][3];
            for (int i = 0; i < path.length; i++) {
                IplImage origImg = cvLoadImage(getFullPath(path[i]));
                //Creating image placeholder to put resized image data
                IplImage resizedImg = IplImage.create(width, height, origImg.depth(), origImg.nChannels());
                cvResize(origImg, resizedImg);
                result[i] = getRGBArray(resizedImg);
            }
            return result;
        }

        private float[][][] getRGBArray(IplImage image) {
            float[][][] result = new float[image.height()][image.width()][3];
            for (int i = 0; i < image.height(); i++) {
                for (int j = 0; j < image.width(); j++) {
                    CvScalar pixel = cvGet2D(image, i, j);
                    result[i][j][0] = (float)(pixel.val(2) - mean) / scale; //R
                    result[i][j][1] = (float)(pixel.val(1) - mean) / scale; //G
                    result[i][j][2] = (float)(pixel.val(0) - mean) / scale; //B
                }
            }
            return result;
        }

        private String getFullPath(String path) {
            return new File(this.getClass().getResource(path).getFile()).getAbsolutePath();
        }
    }

    public class Classificator {
        private Session session;
        private Graph modelGraph;
        private List<String> labels;

        public Classificator() {
            try {
                Path modelPath = Paths.get("/tmp/saved_model.pb");
                byte[] graphData = Files.readAllBytes(modelPath);
                System.err.println("Importing model file of size " + graphData.length + " bytes");
                labels = Arrays.asList(new String[] {
                        "ett",
                        "två"
                });

                modelGraph = new Graph();
                modelGraph.importGraphDef(graphData);
                session = new Session(modelGraph);
            } catch(Exception e) {e.printStackTrace(); throw new RuntimeException(e);}
        }

        public List<String> classify(float[][][][] imageData) {
            Tensor imageTensor = Tensor.create(imageData, Float.class);
            float[][] prediction = predict(imageTensor);
            return findPredictedLabel(prediction);
        }

        private float[][] predict(Tensor imageTensor) {
            Tensor result = session.runner()
                    .feed("input", imageTensor)
                    .fetch("output").run().get(0);
            int batchSize = (int)result.shape()[0];
            //create prediction buffer
            float[][] prediction = new float[batchSize][1008];
            result.copyTo(prediction);
            return prediction;
        }

        private List<String> findPredictedLabel(float[][] prediction) {
            List<String> result = new ArrayList<>();
            int batchSize = prediction.length;
            for (int i = 0; i < batchSize; i++) {
                //Finding maximum value for each predicted image
                int maxValueIndex = 0;
                for (int j = 1; j < prediction[i].length; j++) {
                    if (prediction[i][maxValueIndex] < prediction[i][j]) {
                        maxValueIndex = j;
                    }
                }
                result.add(labels.get(maxValueIndex) + ": " + (prediction[i][maxValueIndex] * 100) + "%");
            }
            return result;
        }
    }

    public TensorflowObjectDetector() throws RaiseFilterException  {
        try {
            ImageProcessor imageProcessor = new ImageProcessor();
            Classificator classificator = new Classificator();
            float[][][][] imageData = imageProcessor.loadAndNormalizeImages("images/ship.jpg", "images/dog.jpg");
            List<String> result = classificator.classify(imageData);
            for(String label: result) {
                System.out.println(label);
            }
        } catch (Exception e) {
            throw new RaiseFilterException("Error loading model", e);
        }
    }

    @Override
    public DetectionResult detect(BufferedImage src) throws RaiseFilterException {
        return null;
    }

    @Override
    public String toString() {
        return null;
    }
}
