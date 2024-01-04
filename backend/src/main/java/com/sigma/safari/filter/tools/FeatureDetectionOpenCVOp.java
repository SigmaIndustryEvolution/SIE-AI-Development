package com.sigma.safari.filter.tools;

import com.raise.image.filter.tools.AbstractFilter;
import com.sigma.safari.filter.parameters.FeatureDetectionParameters;
import nu.pattern.OpenCV;
import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.awt.image.BufferedImage;
import java.util.List;

public class FeatureDetectionOpenCVOp extends AbstractFilter {
	FeatureDetectionParameters p;

	static {
		OpenCV.loadLocally();
	}

	public FeatureDetectionOpenCVOp(FeatureDetectionParameters parameters) {
		this.p = parameters;
	}

	@Override
	public BufferedImage filter(BufferedImage rawSrc, BufferedImage dst) {
		/*
		BufferedImage image = new BufferedImage(rawSrc.getWidth(), rawSrc.getHeight(), TYPE_BYTE_BINARY);
		image.getGraphics().drawImage(rawSrc, 0, 0, null);
		if (dst == null) {
			dst = createCompatibleDestImage(image, null);
		}

		int[] destPixels = new int[ image.getWidth() * image.getHeight() ];

		Mat currentImage = new Mat();
		byte[] pixels = ((DataBufferByte) rawSrc.getRaster().getDataBuffer()).getData();
		currentImage.put(0, 0, pixels);
		*/

		Mat currentImage = Imgcodecs.imread("/Users/joakimahlen/Dropbox/git/Safari/CondoorST3V-2 resample 512 gauss edge BW.tif");
		System.err.println("Image: " + currentImage.toString());

		CascadeClassifier screwsCascade = new CascadeClassifier();
		if (!screwsCascade.load(this.p.file.getAbsolutePath())) {
			throw new Error("-- Error loading screws cascade: " + this.p.file.getAbsolutePath());
		}

		System.err.println("Detecting features...");
		long start = System.currentTimeMillis();
		MatOfRect faces = new MatOfRect();
		screwsCascade.detectMultiScale(currentImage, faces);

		List<Rect> hits = faces.toList();
		long end = System.currentTimeMillis();
		System.err.println("Detected " + hits.size() + " screws in image in " + (end - start) + "ms");

		for(var hit : hits) {
			Point center = new Point(hit.x + hit.width / 2, hit.y + hit.height / 2);
			Imgproc.ellipse(currentImage, center, new Size(hit.width / 2, hit.height / 2), 0, 0, 360,
					new Scalar(255, 0, 255));
			System.err.println("Screw hit: " + hit.toString() + " (" + center.toString() + ")");
		}

		Imgcodecs.imwrite("out.jpg", currentImage);

		return rawSrc;
	}
}
