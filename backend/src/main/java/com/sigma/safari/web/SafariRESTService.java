package com.sigma.safari.web;

import com.raise.image.filter.RaiseFilterException;
import com.raise.services.FilterServiceException;
import com.raise.services.Result;
import com.raise.services.ResultCode;
import com.raise.services.web.AbstractRESTService;
import com.raise.services.RaiseException;
import com.raise.services.web.RaiseSecurityException;
import com.raise.services.web.filters.Secured;
import com.sigma.safari.service.SafariService;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.FormDataParam;
import org.json.JSONArray;
import org.json.JSONObject;

import javax.security.auth.Subject;
import javax.servlet.ServletContext;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import java.io.InputStream;
import java.security.Principal;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

@Path("/")
public class SafariRESTService extends AbstractRESTService {
    private final boolean myDebug = false;

    private JSONObject[] myCredentials = new JSONObject[] {
            new JSONObject()
                    .put("username", "joakimahlen")
                    .put("password", "zxc123!")
                    .put("id", 123)
                    .put("name", "Joakim Ahlén")
                    .put("roles", new JSONArray().put("group1").put("group2"))
    };

    private SafariService mySafariService = SafariService.getInstance();

    public SafariRESTService(@Context ServletContext context) {
        super(context);
    }

    public Subject authenticate(JSONObject requestBody) throws RaiseSecurityException {
        Optional<JSONObject> user = Arrays.stream(myCredentials)
                .filter(credential ->
                        credential.getString("username")
                                .equals(requestBody.getString("username")) &&
                                credential.getString("password")
                                        .equals(requestBody.getString("password")))
                .findFirst();

        if (!user.isPresent()) {
            throw new RaiseSecurityException(RaiseException.FORBIDDEN, "Credentials invalid");
        }

        Set<Principal> principals = new HashSet<>();
        principals.add(() -> user.get().getString("username"));

        JSONObject privateObject = new JSONObject();
        user.get().keySet().stream()
                .filter(key -> key.equals("password"))
                .forEach(key -> {
                    privateObject.put(key, user.get().get(key));
                });

        JSONObject publicObject = new JSONObject();
        user.get().keySet().stream()
                .filter(key -> !key.equals("username"))
                .filter(key -> !key.equals("password"))
                .forEach(key -> {
                    publicObject.put(key, user.get().get(key));
                });

        Set<JSONObject> privateCredentials = new HashSet<>();
        privateCredentials.add(privateObject);

        Set<JSONObject> publicCredentials = new HashSet<>();
        publicCredentials.add(publicObject);

        return new Subject(false, principals, publicCredentials, privateCredentials);
    }

    @Secured
    @GET
    @Path("/hello")
    public Response verify(@Context SecurityContext sc) {
        JSONObject json;
        if (sc.getUserPrincipal() == null) {
            json = new Result(ResultCode.UNAUTHORIZED, "Safari hello world, no token");
        } else {
            json = Arrays.stream(myCredentials)
                    .filter(credential -> credential.getString("username").equals(sc.getUserPrincipal().getName()))
                    .findFirst()
                    .get();
        }

        return returnJson(Response.Status.OK, json);
    }

    @Secured
    @POST
    @Path("/predict")
    @Consumes(MediaType.MULTIPART_FORM_DATA)
    @Produces(MediaType.APPLICATION_JSON)
    public Response predict(@Context HttpHeaders headers,
                            @FormDataParam("front") InputStream frontInputStream,
                            @FormDataParam("front") FormDataContentDisposition frontFileDetails,
                            @FormDataParam("back") InputStream backInputStream,
                            @FormDataParam("back") FormDataContentDisposition backFileDetails,
                            @FormDataParam("side") InputStream sideInputStream,
                            @FormDataParam("side") FormDataContentDisposition sideFileDetails) {
        try {
            if (this.myDebug) {
                headers.getRequestHeaders().keySet().forEach(key -> {
                    System.err.println("== HTTP HEADER: " + key + ": " + headers.getRequestHeader(key));
                });
            }

            JSONObject imgQuality = mySafariService.predict(frontInputStream, backInputStream, sideInputStream);

            return returnJson(Response.Status.OK, imgQuality);
        } catch (RaiseFilterException rfe) {
            System.err.println("-- Error in 'imageQuality' call: " + rfe);
            rfe.printStackTrace();
            FilterServiceException fse = new FilterServiceException(rfe);
            return returnJson(Response.Status.OK, fse.getResult());
        }
    }
}
