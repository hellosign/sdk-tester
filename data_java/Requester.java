package com.hellosign.sdk;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.hellosign.openapi.*;
import com.hellosign.openapi.api.AccountApi;
import com.hellosign.openapi.api.ApiAppApi;
import com.hellosign.openapi.api.SignatureRequestApi;
import com.hellosign.openapi.auth.HttpBasicAuth;
import com.hellosign.openapi.auth.HttpBearerAuth;
import com.hellosign.openapi.model.*;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Stream;

public class Requester {
    private String apiServer;
    private String authType;
    private String authKey;
    private JsonNode data;
    private boolean devMode;
    private JsonNode files;
    private String operationId;
    private JsonNode parameters;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private final static String FILE_UPLOADS_DIR = "./../file_uploads";

    public Requester(String authType, String authKey, String apiServer, String jsonData, boolean devMode) throws Exception {
        this.authType = authType.toLowerCase();
        this.authKey = authKey;
        this.apiServer = apiServer;
        this.devMode = devMode;
        readJsonData(jsonData);
    }

    public void run() throws Exception {
        ObjectWriter ow = objectMapper.writer().withDefaultPrettyPrinter();
        try {
            ApiResponse apiResponse = callFromOperationId();
            Map<String, Object> output = Map.of(
                    "body", apiResponse.getData(),
                    "status_code", apiResponse.getStatusCode(),
                    "headers", apiResponse.getHeaders()
            );
            System.out.println(ow.writeValueAsString(output));
        } catch (ApiException e) {
            Map<String, Object> output = Map.of(
                    "body", e.getErrorResponse(),
                    "status_code", e.getCode(),
                    "headers", e.getResponseHeaders()
            );
            System.out.println(ow.writeValueAsString(output));
        }
    }

    private void readJsonData(String base64Json) throws Exception {
        JsonNode jsonNode = objectMapper.readTree(Base64.getDecoder().decode(base64Json));
        operationId = jsonNode.get("operationId").asText("");
        data = jsonNode.get("data");
        files = jsonNode.get("files");
        parameters = jsonNode.get("parameters");
    }

    private ApiResponse callFromOperationId() throws Exception{
        return Stream.of(
                accountApi(),
                apiAppApi(),
                bulkSendJobApi(),
                embeddedApi(),
                oauthApi(),
                reportApi(),
                signatureRequestApi(),
                teamApi(),
                templateApi(),
                unclaimedDraftApi()
        ).filter(Objects::nonNull).findFirst().orElseThrow(() -> new Exception("Invalid operationId: " + operationId));
    }

    private ApiResponse unclaimedDraftApi() {
        return null;
    }

    private ApiResponse templateApi() {
        return null;
    }

    private ApiResponse teamApi() {
        return null;
    }

    private ApiResponse signatureRequestApi() throws Exception {
        SignatureRequestApi api = new SignatureRequestApi(getApiClient());
        switch (operationId) {
            case "signatureRequestSend":
                SignatureRequestSendRequest sendRequest = objectMapper.readValue(data.toString(), SignatureRequestSendRequest.class);
                sendRequest.setFile(getFiles("file"));
                return api.signatureRequestSendWithHttpInfo(sendRequest);
        }
        return null;
    }

    private ApiResponse reportApi() {
        return null;
    }

    private ApiResponse oauthApi() {
        return null;
    }

    private ApiResponse embeddedApi() {
        return null;
    }

    private ApiResponse bulkSendJobApi() {
        return null;
    }

    private ApiResponse apiAppApi() throws Exception {
        ApiAppApi api = new ApiAppApi(getApiClient());
        switch (operationId) {
            case "apiAppCreate":
                ApiAppCreateRequest createRequest = objectMapper.readValue(data.toString(), ApiAppCreateRequest.class);
                createRequest.customLogoFile(getFile("custom_logo_file"));
                return api.apiAppCreateWithHttpInfo(createRequest);
        }
        return null;
    }

    private ApiResponse accountApi() throws Exception {
        AccountApi api = new AccountApi(getApiClient());
        switch (operationId) {
            case "accountCreate":
                AccountCreateRequest request = objectMapper.readValue(data.toString(), AccountCreateRequest.class);
                return api.accountCreateWithHttpInfo(request);
            case "accountGet":
                return api.accountGetWithHttpInfo(parameters.get("account_id").asText());
            case "accountUpdate":
                AccountUpdateRequest updateRequest = objectMapper.readValue(data.toString(), AccountUpdateRequest.class);
                return api.accountUpdateWithHttpInfo(updateRequest);
            case "accountVerify":
                AccountVerifyRequest verifyRequest = objectMapper.readValue(data.toString(), AccountVerifyRequest.class);
                return api.accountVerifyWithHttpInfo(verifyRequest);
        }
        return null;
    }

    private ApiClient getApiClient() throws Exception {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        if (apiServer != null && !apiServer.isBlank()) {
            defaultClient.setBasePath("https://" + apiServer + "/v3");
        }
        if ("apikey".equals(authType)) {
            HttpBasicAuth api_key = (HttpBasicAuth) defaultClient
                    .getAuthentication("api_key");
            api_key.setUsername(authKey);
        } else if ("oauth".equals(authType)) {
            HttpBearerAuth oauth2 = (HttpBearerAuth) defaultClient
                    .getAuthentication("oauth2");

            oauth2.setBearerToken(authKey);
        } else {
            throw new Exception(
                    "Invalid auth type. Must be \"apikey\" or \"oauth\""
            );
        }
        return defaultClient;
    }

    private List<File> getFiles(String name) {
        List<File> files = new ArrayList<>();
        this.files.get(name)
                .iterator()
                .forEachRemaining(jsonNode -> files.add(new File(FILE_UPLOADS_DIR + "/" + jsonNode.asText())));
        return files;
    }

    private File getFile(String name) {
        if (!files.get(name).asText().isBlank()) {
            return new File(FILE_UPLOADS_DIR + "/" + files.get(name).asText());
        }
        return null;
    }

    public static void main(String[] args) throws Exception {
        Requester r = new Requester(
                System.getenv("AUTH_TYPE"),
                System.getenv("AUTH_KEY"),
                System.getenv("API_SERVER"),
                System.getenv("JSON_DATA"),
                Boolean.parseBoolean(System.getenv("API_SERVER"))
        );
        r.run();
    }
}
