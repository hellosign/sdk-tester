package com.hellosign.sdk;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.hellosign.openapi.*;
import com.hellosign.openapi.api.AccountApi;
import com.hellosign.openapi.auth.HttpBasicAuth;
import com.hellosign.openapi.auth.HttpBearerAuth;
import com.hellosign.openapi.model.AccountGetResponse;

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

    public Requester(String authType, String authKey, String apiServer, String jsonData, boolean devMode) throws Exception {
        this.authType = authType.toLowerCase();
        this.authKey = authKey;
        this.apiServer = apiServer;
        this.devMode = devMode;
        readJsonData(jsonData);
    }

    public void run() throws Exception {
        ApiResponse apiResponse = callFromOperationId();

        ObjectWriter ow = new ObjectMapper().writer().withDefaultPrettyPrinter();
        Map<String, Object> output = Map.of(
        "body", apiResponse.getData(),
        "statusCode", apiResponse.getStatusCode(),
        "headers", apiResponse.getHeaders()
        );
        System.out.println(ow.writeValueAsString(output));
    }

    private void readJsonData(String base64Json) throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
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

    private ApiResponse signatureRequestApi() {
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

    private ApiResponse apiAppApi() {
        return null;
    }

    private ApiResponse accountApi() throws Exception {
        AccountApi api = new AccountApi(getApiClient());
        ApiClient apiClient = getApiClient();
        switch (operationId) {
            case "accountGet":
                return api.accountGetWithHttpInfo(parameters.get("account_id").asText());
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
