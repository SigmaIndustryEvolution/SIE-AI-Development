package com.sigma.safari.filter.tools;

import com.raise.image.filter.RaiseFilterException;
import com.raise.image.filter.tools.AbstractFilter;
import com.raise.image.models.MatchAreaResult;
import com.raise.image.models.MatchPixelResult;
import com.raise.image.tools.PixelHelper;
import com.sigma.safari.filter.parameters.FeatureDetectionParameters;

import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

import static java.awt.image.BufferedImage.TYPE_BYTE_BINARY;

public class FeatureDetectionScanOp extends AbstractFilter {
	FeatureDetectionParameters p;

	public FeatureDetectionScanOp(FeatureDetectionParameters parameters) {
		this.p = parameters;
	}

	public double distance(int x1, int y1, int x2, int y2) {
		return Math.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1));
	}

	public boolean isAlreadyMatched(int x, int y, List<MatchAreaResult> others, int threshold) {
		for(var other : others) {
			if (distance(x, y, other.x, other.y) < threshold) {
				return true;
			}
		}

		return false;
	}

	private MatchAreaResult[] getMatches(BufferedImage image, int startX, int startY, int finishX, int finishY, int roughness) throws RaiseFilterException {
		int side = this.p.featureMatrix.length;

		List<MatchAreaResult> results = new ArrayList<>();

		for(int y = startX; y < finishX; y += roughness) {
			for(int x = startY; x < finishY; x+= roughness) {
				boolean sample[][] = PixelHelper.getBwPixels(image, x, y, side, side);
				MatchPixelResult match = getMatrixMatch(this.p.featureMatrix, sample);

				if (!isAlreadyMatched(x, y, results, side)) {
					results.add(new MatchAreaResult(x, y, match));
				}
			}
		}

		return results.toArray(MatchAreaResult[]::new);
	}

	@Override
	public BufferedImage filter(BufferedImage rawSrc, BufferedImage dst) {
		BufferedImage image = new BufferedImage(rawSrc.getWidth(), rawSrc.getHeight(), TYPE_BYTE_BINARY);
		image.getGraphics().drawImage(rawSrc, 0, 0, null);
		if (dst == null) {
			dst = createCompatibleDestImage(image, null);
		}

		int[] destPixels = new int[ image.getWidth() * image.getHeight() ];

		int side = this.p.featureMatrix.length;

		try {
			long start = System.currentTimeMillis();
			System.err.println("Finding matches...");
			var matches = Arrays.stream(getMatches(image, 0, 0, image.getWidth() - side, image.getHeight() - side, 1))
					.sorted(Collections.reverseOrder())
					.filter(p -> p.getCorrelation() > 0.55)
					.collect(Collectors.toList());
			long end = System.currentTimeMillis();
			System.err.println("Found matches in " + (end - start)/1000 + "s");

			Collections.sort(matches, Collections.reverseOrder());
			System.err.println("Found " + matches.size() + " real matches");
			for(var match : matches) {
				System.err.println("Match: " + match);
			}


		/*
			for(int y = 0; y < image.getHeight() - side; y += side/2) {
				for(int x = 0; x < image.getWidth() - side; x+= side/2) {
					boolean sample[][] = PixelHelper.getBwPixels(image, x, y, side, side);
					MatchPixelResult match = getMatrixMatch(this.p.featureMatrix, sample);

					if (match.getHighMatch() > 0.50) {
						System.err.println("Match at " + x + "x" + y + ": (" + Math.round(match.getHighMatch() * 100.0) + "%)" + match.toString());
					}
					destPixels[x + y * rawSrc.getWidth()] = 0;
					System.err.print(Math.round(match.getHighMatch() * 100.0) + "%, ");
				}
				System.err.print(".");
				if ((y % 10) == 0) {
					System.err.print(y);
				}
				if ((y % 100) == 0) {
					System.err.println();
				}
//				System.err.println();
			}
		 */

			PixelHelper.setPixels(dst, 0, 0, rawSrc.getWidth(), rawSrc.getHeight(), destPixels);
		} catch (RaiseFilterException rfe) {
			throw new Error(rfe);
		}

		return dst;
	}

	public MatchPixelResult getMatrixMatch(boolean[][] templatePixels, boolean[][] samplePixels) {
		int width = templatePixels.length;
		int height = templatePixels[0].length;

		MatchPixelResult match = new MatchPixelResult(width, height);

		for(int x = 0; x < width; x++) {
			for(int y = 0; y < height; y++) {
				boolean pixel1 = templatePixels[x][y];
				boolean pixel2 = samplePixels[x][y];

				match.compare(x, y, pixel1, pixel2);
			}
		}

		return match;
	}
}
