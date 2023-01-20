package com.dropbox.sign.sdk_tester;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.dropbox.sign.*;
import com.dropbox.sign.api.*;
import com.dropbox.sign.auth.HttpBasicAuth;
import com.dropbox.sign.auth.HttpBearerAuth;
import com.dropbox.sign.model.*;

import java.io.File;
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
            ApiResponse<?> apiResponse = callFromOperationId();
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

    private ApiResponse<?> callFromOperationId() throws Exception{
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

    private ApiResponse<?> unclaimedDraftApi() throws Exception {
        UnclaimedDraftApi api = new UnclaimedDraftApi(getApiClient());
        switch (operationId) {
            case "unclaimedDraftCreate":
                UnclaimedDraftCreateRequest createRequest = objectMapper.readValue(data.toString(), UnclaimedDraftCreateRequest.class);
                createRequest.setFiles(getFiles("files"));
                return api.unclaimedDraftCreateWithHttpInfo(createRequest);
            case "unclaimedDraftCreateEmbedded":
                UnclaimedDraftCreateEmbeddedRequest createEmbeddedRequest =
                        objectMapper.readValue(data.toString(), UnclaimedDraftCreateEmbeddedRequest.class);
                createEmbeddedRequest.setFiles(getFiles("files"));
                return api.unclaimedDraftCreateEmbeddedWithHttpInfo(createEmbeddedRequest);
            case "unclaimedDraftCreateEmbeddedWithTemplate":
                UnclaimedDraftCreateEmbeddedWithTemplateRequest embeddedWithTemplateRequest =
                        objectMapper.readValue(data.toString(), UnclaimedDraftCreateEmbeddedWithTemplateRequest.class);
                embeddedWithTemplateRequest.setFiles(getFiles("files"));
                return api.unclaimedDraftCreateEmbeddedWithTemplateWithHttpInfo(embeddedWithTemplateRequest);
            case "unclaimedDraftEditAndResend":
                UnclaimedDraftEditAndResendRequest resendRequest =
                        objectMapper.readValue(data.toString(), UnclaimedDraftEditAndResendRequest.class);
                return api.unclaimedDraftEditAndResendWithHttpInfo(parameters.get("signature_request_id").asText(), resendRequest);
        }
        return null;
    }

    private ApiResponse<?> templateApi() throws Exception {
        TemplateApi api = new TemplateApi(getApiClient());
        switch (operationId) {
            case "templateAddUser":
                TemplateAddUserRequest addUserRequest = objectMapper.readValue(data.toString(), TemplateAddUserRequest.class);
                return api.templateAddUserWithHttpInfo(parameters.get("template_id").asText(), addUserRequest);
            case "templateCreateEmbeddedDraft":
                TemplateCreateEmbeddedDraftRequest embeddedDraftRequest
                        = objectMapper.readValue(data.toString(), TemplateCreateEmbeddedDraftRequest.class);
                return api.templateCreateEmbeddedDraftWithHttpInfo(embeddedDraftRequest);
            case "templateDelete":
                return api.templateDeleteWithHttpInfo(parameters.get("template_id").asText());
            case "templateFilesAsFileUrl":
                return api.templateFilesAsFileUrlWithHttpInfo(
                        parameters.get("template_id").asText()
                );
            case "templateGet":
                return api.templateGetWithHttpInfo(parameters.get("template_id").asText());
            case "templateList":
                return api.templateListWithHttpInfo(
                        parameters.get("account_id").asText(),
                        parameters.get("page").asInt(1),
                        parameters.get("page_size").asInt(20),
                        parameters.get("query").asText()
                );
            case "templateRemoveUser":
                TemplateRemoveUserRequest removeUserRequest = objectMapper.readValue(data.toString(), TemplateRemoveUserRequest.class);
                return api.templateRemoveUserWithHttpInfo(parameters.get("template_id").asText(), removeUserRequest);
            case "templateUpdateFiles":
                TemplateUpdateFilesRequest updateFilesRequest = objectMapper.readValue(data.toString(), TemplateUpdateFilesRequest.class);
                updateFilesRequest.setFiles(getFiles("files"));
                return api.templateUpdateFilesWithHttpInfo(parameters.get("template_id").asText(), updateFilesRequest);
        }
        return null;
    }

    private ApiResponse<?> teamApi() throws Exception {
        TeamApi api = new TeamApi(getApiClient());
        switch (operationId) {
            case "teamAddMember":
                TeamAddMemberRequest addMemberRequest = objectMapper.readValue(data.toString(), TeamAddMemberRequest.class);
                return api.teamAddMemberWithHttpInfo(addMemberRequest, parameters.get("team_id").asText());
            case "teamCreate":
                TeamCreateRequest createRequest = objectMapper.readValue(data.toString(), TeamCreateRequest.class);
                return api.teamCreateWithHttpInfo(createRequest);
            case "teamDelete":
                return api.teamDeleteWithHttpInfo();
            case "teamGet":
                return api.teamGetWithHttpInfo();
            case "teamRemoveMember":
                TeamRemoveMemberRequest removeMemberRequest = objectMapper.readValue(data.toString(), TeamRemoveMemberRequest.class);
                return api.teamRemoveMemberWithHttpInfo(removeMemberRequest);
            case "teamUpdate":
                TeamUpdateRequest updateRequest = objectMapper.readValue(data.toString(), TeamUpdateRequest.class);
                return api.teamUpdateWithHttpInfo(updateRequest);
        }
        return null;
    }

    private ApiResponse<?> signatureRequestApi() throws Exception {
        SignatureRequestApi api = new SignatureRequestApi(getApiClient());
        switch (operationId) {
            case "signatureRequestBulkCreateEmbeddedWithTemplate":
                SignatureRequestBulkCreateEmbeddedWithTemplateRequest templateRequest =
                        objectMapper.readValue(data.toString(), SignatureRequestBulkCreateEmbeddedWithTemplateRequest.class);
                templateRequest.setSignerFile(getFile("signer_file"));
                return api.signatureRequestBulkCreateEmbeddedWithTemplateWithHttpInfo(templateRequest);
            case "signatureRequestBulkSendWithTemplate":
                SignatureRequestBulkSendWithTemplateRequest withTemplateRequest =
                        objectMapper.readValue(data.toString(), SignatureRequestBulkSendWithTemplateRequest.class);
                withTemplateRequest.setSignerFile(getFile("signer_file"));
                return api.signatureRequestBulkSendWithTemplateWithHttpInfo(withTemplateRequest);
            case "signatureRequestCancel":
                return api.signatureRequestCancelWithHttpInfo(parameters.get("signature_request_id").asText());
            case "signatureRequestCreateEmbedded":
                SignatureRequestCreateEmbeddedRequest embeddedRequest = objectMapper.readValue(data.toString(), SignatureRequestCreateEmbeddedRequest.class);
                embeddedRequest.setFiles(getFiles("files"));
                return api.signatureRequestCreateEmbeddedWithHttpInfo(embeddedRequest);
            case "signatureRequestCreateEmbeddedWithTemplate":
                SignatureRequestCreateEmbeddedWithTemplateRequest embeddedWithTemplateRequest =
                        objectMapper.readValue(data.toString(), SignatureRequestCreateEmbeddedWithTemplateRequest.class);
                embeddedWithTemplateRequest.setFiles(getFiles("files"));
                return api.signatureRequestCreateEmbeddedWithTemplateWithHttpInfo(embeddedWithTemplateRequest);
            case "signatureRequestFilesAsFileUrl":
                return api.signatureRequestFilesAsFileUrlWithHttpInfo(
                        parameters.get("signature_request_id").asText()
                );
            case "signatureRequestGet":
                return api.signatureRequestGetWithHttpInfo(parameters.get("signature_request_id").asText());
            case "signatureRequestList":
                return api.signatureRequestListWithHttpInfo(
                        parameters.get("account_id").asText(),
                        parameters.get("page").asInt(1),
                        parameters.get("page_size").asInt(20),
                        parameters.get("query").asText()
                );
            case "signatureRequestReleaseHold":
                return api.signatureRequestReleaseHoldWithHttpInfo(parameters.get("signature_request_id").asText());
            case "signatureRequestRemind":
                SignatureRequestRemindRequest remindRequest = objectMapper.readValue(data.toString(), SignatureRequestRemindRequest.class);
                return api.signatureRequestRemindWithHttpInfo(parameters.get("signature_request_id").asText(), remindRequest);
            case "signatureRequestRemove":
                return api.signatureRequestRemoveWithHttpInfo(parameters.get("signature_request_id").asText());
            case "signatureRequestSend":
                SignatureRequestSendRequest sendRequest = objectMapper.readValue(data.toString(), SignatureRequestSendRequest.class);
                sendRequest.setFiles(getFiles("files"));
                return api.signatureRequestSendWithHttpInfo(sendRequest);
            case "signatureRequestSendWithTemplate":
                SignatureRequestSendWithTemplateRequest sendWithTemplateRequest =
                        objectMapper.readValue(data.toString(), SignatureRequestSendWithTemplateRequest.class);
                sendWithTemplateRequest.setFiles(getFiles("files"));
                return api.signatureRequestSendWithTemplateWithHttpInfo(sendWithTemplateRequest);
            case "signatureRequestUpdate":
                SignatureRequestUpdateRequest updateRequest = objectMapper.readValue(data.toString(), SignatureRequestUpdateRequest.class);
                return api.signatureRequestUpdateWithHttpInfo(parameters.get("signature_request_id").asText(), updateRequest);

        }
        return null;
    }

    private ApiResponse<?> reportApi() throws Exception {
        ReportApi api = new ReportApi(getApiClient());
        switch (operationId) {
            case "reportCreate":
                ReportCreateRequest createRequest = objectMapper.readValue(data.toString(), ReportCreateRequest.class);
                return api.reportCreateWithHttpInfo(createRequest);
        }
        return null;
    }

    private ApiResponse<?> oauthApi() throws Exception {
        OAuthApi api = new OAuthApi(getApiClient());
        switch (operationId) {
            case "oauthTokenGenerate":
                OAuthTokenGenerateRequest generateRequest = objectMapper.readValue(data.toString(), OAuthTokenGenerateRequest.class);
                return api.oauthTokenGenerateWithHttpInfo(generateRequest);
            case "oauthTokenRefresh":
                OAuthTokenRefreshRequest refreshRequest = objectMapper.readValue(data.toString(), OAuthTokenRefreshRequest.class);
                return api.oauthTokenRefreshWithHttpInfo(refreshRequest);
        }
        return null;
    }

    private ApiResponse<?> embeddedApi() throws Exception {
        EmbeddedApi api = new EmbeddedApi(getApiClient());
        switch (operationId) {
            case "embeddedEditUrl":
                EmbeddedEditUrlRequest editUrlRequest = objectMapper.readValue(data.toString(), EmbeddedEditUrlRequest.class);
                return api.embeddedEditUrlWithHttpInfo(parameters.get("template_id").asText(), editUrlRequest);
            case "embeddedSignUrl":
                return api.embeddedSignUrlWithHttpInfo(parameters.get("embeddedSignUrl").asText());
        }
        return null;
    }

    private ApiResponse<?> bulkSendJobApi() throws Exception {
        BulkSendJobApi api = new BulkSendJobApi(getApiClient());
        switch (operationId) {
            case "bulkSendJobGet":
                return api.bulkSendJobGetWithHttpInfo(parameters.get("bulk_send_job_id").asText());
            case "bulkSendJobList":
                int page = parameters.get("page").asInt(1);
                int pageSize = parameters.get("page_size").asInt(20);
                return api.bulkSendJobListWithHttpInfo(page, pageSize);
        }
        return null;
    }

    private ApiResponse<?> apiAppApi() throws Exception {
        ApiAppApi api = new ApiAppApi(getApiClient());
        switch (operationId) {
            case "apiAppCreate":
                ApiAppCreateRequest createRequest = objectMapper.readValue(data.toString(), ApiAppCreateRequest.class);
                createRequest.customLogoFile(getFile("custom_logo_file"));
                return api.apiAppCreateWithHttpInfo(createRequest);
            case "apiAppDelete":
                return api.apiAppDeleteWithHttpInfo(parameters.get("client_id").asText());
            case "apiAppGet":
                return api.apiAppGetWithHttpInfo(parameters.get("client_id").asText());
            case "apiAppList":
                int page = parameters.get("page").asInt(1);
                int pageSize = parameters.get("page_size").asInt(20);
                return api.apiAppListWithHttpInfo(page, pageSize);
            case "apiAppUpdate":
                ApiAppUpdateRequest updateRequest = objectMapper.readValue(data.toString(), ApiAppUpdateRequest.class);
                updateRequest.customLogoFile(getFile("custom_logo_file"));
                return api.apiAppUpdateWithHttpInfo(parameters.get("client_id").asText(), updateRequest);
        }
        return null;
    }

    private ApiResponse<?> accountApi() throws Exception {
        AccountApi api = new AccountApi(getApiClient());
        switch (operationId) {
            case "accountCreate":
                AccountCreateRequest request = objectMapper.readValue(data.toString(), AccountCreateRequest.class);
                return api.accountCreateWithHttpInfo(request);
            case "accountGet":
                return api.accountGetWithHttpInfo(
                        Optional.ofNullable(parameters.get("account_id")).map(JsonNode::asText).orElse(null),
                        Optional.ofNullable(parameters.get("email_address")).map(JsonNode::asText).orElse(null)
                );
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
        if (devMode) {
            defaultClient.addDefaultHeader("Cookie", "XDEBUG_SESSION=xdebug");
        }
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
                Boolean.parseBoolean(System.getenv("DEV_MODE"))
        );
        r.run();
    }
}
