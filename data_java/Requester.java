package com.hellosign.sdk;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import org.hellosign.openapi.*;
import org.hellosign.openapi.api.AccountApi;
import org.hellosign.openapi.auth.HttpBasicAuth;
import org.hellosign.openapi.model.AccountGetResponse;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

public class Requester {
    private String apiServer;
    private String authType;
    private String authKey;
    private Map<String, String> data;
    private boolean devMode;
    private Map<String, File> files;
    private String operationId;
    private Map<String, String> parameters;

    public void run() throws Exception {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        HttpBasicAuth api_key = (HttpBasicAuth) defaultClient
                .getAuthentication("api_key");
        api_key.setUsername("f405ae7d0b867fe9881a0ceb41154b6862d535b011ab77a28dbbccd68c70fe0b");
        AccountApi api = new AccountApi(defaultClient);
        ApiResponse<AccountGetResponse> apiResponse = api.accountGetWithHttpInfo(null);

        ObjectWriter ow = new ObjectMapper().writer().withDefaultPrettyPrinter();
        Map<String, Object> output = new HashMap<>();
        output.put("body", apiResponse.getData());
        output.put("statusCode", apiResponse.getStatusCode());
        output.put("headers", apiResponse.getHeaders());
        System.out.println(ow.writeValueAsString(output));
    }

    public static void main(String[] args) throws Exception {
        Requester r = new Requester();
        r.run();
    }
}
