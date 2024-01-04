package com.sigma.safari.detectors;

import com.raise.image.filter.RaiseFilterException;
import com.raise.image.quality.DetectionResult;
import com.raise.image.quality.RaiseDetector;
import com.raise.services.HelperService;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.glassfish.jersey.media.multipart.file.FileDataBodyPart;
import org.glassfish.jersey.media.multipart.file.StreamDataBodyPart;
import org.json.JSONObject;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.Response;
import java.awt.image.BufferedImage;
import java.io.InputStream;
import java.util.Arrays;

public class ProxyObjectDetector extends RaiseDetector {
    private final InputStream myFront;
    private final InputStream myBack;
    private final InputStream mySide;

    public ProxyObjectDetector(InputStream front, InputStream back, InputStream side) {
        this.myFront = front;
        this.myBack = back;
        this.mySide = side;
    }

    @Override
    public DetectionResult detect(BufferedImage image) throws RaiseFilterException {
        try {
            final Client client = ClientBuilder.newBuilder().register(MultiPartFeature.class).build();

            final StreamDataBodyPart frontPart = new StreamDataBodyPart("front", myFront);
            final StreamDataBodyPart backPart = new StreamDataBodyPart("back", myBack);
            final StreamDataBodyPart sidePart = new StreamDataBodyPart("side", mySide);

            FormDataMultiPart multipart = (FormDataMultiPart) new FormDataMultiPart()
                    .bodyPart(frontPart)
                    .bodyPart(backPart)
                    .bodyPart(sidePart);

            final WebTarget target = client.target("http://predict:8000/images");
            final Response response = target.request().post(Entity.entity(multipart, multipart.getMediaType()));

            multipart.close();

            if (response.getStatus() == 200) {
                JSONObject predictResult = HelperService.parseJsonString(response.readEntity(String.class));

                DetectionResult[] predictions = Arrays.stream(predictResult.keySet().toArray(new String[0]))
                        .map(key -> new DetectionResult(key, predictResult.getDouble(key)))
                        .toArray(DetectionResult[]::new);

                return DetectionResult.combine(predictions);
            } else {
                throw new RaiseFilterException("Http " + response.getStatus() + ": " + response.readEntity(String.class));
            }
        } catch (Exception e) {
            throw new RaiseFilterException(e);
        }
    }

    @Override
    public String toString() {
        return null;
    }
}
