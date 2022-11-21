using System;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using HelloSign.Api;
using HelloSign.Client;
using HelloSign.Model;
using JsonSerializer = System.Text.Json.JsonSerializer;


class Requester
{
    private string apiServer;
    private string authType;
    private string authKey;
    private JObject data = new();
    private bool devMode;
    private JObject? files;
    private string? operationId;
    private JObject? parameters;

    private readonly string FILE_UPLOADS_DIR = "/file_uploads";

    public Requester(string authType, string authKey, string apiServer, string jsonData, bool devMode)
    {
        this.authType = authType.ToLower();
        this.authKey = authKey;
        this.apiServer = apiServer;
        this.devMode = devMode;
        ReadJsonData(jsonData);
    }

    public void Run()
    {
        try
        {
            var apiResponse = CallFromOperationId();
            var output = new Dictionary<string, object>
            {
                ["body"] = apiResponse.Content,
                ["status_code"] = (int)apiResponse.StatusCode,
                ["headers"] = apiResponse.Headers
            };

            Console.WriteLine(JsonConvert.SerializeObject(output));
        }
        catch (ApiException e)
        {
            var output = new Dictionary<string, object>
            {
                ["body"] = e.ErrorContent,
                ["status_code"] = e.ErrorCode,
                ["headers"] = e.Headers
            };
            Console.WriteLine(JsonConvert.SerializeObject(output));
        }
    }

    private void ReadJsonData(string base64Json)
    {
        var json = Encoding.UTF8.GetString(Convert.FromBase64String(base64Json));
        var dictionary = JsonConvert.DeserializeObject<Dictionary<string, object>>(json) ?? new Dictionary<string, object>();
        operationId =  dictionary["operationId"] as string;
        dictionary.TryGetValue("data", out var dataObj );
        dictionary.TryGetValue("files", out var filesObj);
        dictionary.TryGetValue("parameters", out var parametersObj);

        data = dataObj as JObject ?? new JObject();
        files = filesObj as JObject;
        parameters = parametersObj as JObject;
    }

    private IApiResponse CallFromOperationId()
    {
        return AccountApi() ??
               ApiAppApi() ??
               BulkSendJobApi() ??
               EmbeddedApi() ??
               OauthApi() ??
               ReportApi() ??
               SignatureRequestApi() ??
               TeamApi() ??
               TemplateApi() ??
               UnclaimedDraftApi() ??
               throw new Exception($"Invalid operationId: {operationId}");

    }

    private IApiResponse? AccountApi()
    {
        var api = new AccountApi(GetConfiguration());
        switch (operationId)
        {
            case "accountCreate":
                var createRequest = JsonConvert.DeserializeObject<AccountCreateRequest>(data.ToString()) ?? new AccountCreateRequest();
                return api.AccountCreateWithHttpInfo(createRequest);
            case "accountGet":
                return api.AccountGetWithHttpInfo(parameters?["account_id"]?.ToString());
            case "accountUpdate":
                var updateRequest = JsonConvert.DeserializeObject<AccountUpdateRequest>(data.ToString()) ?? new AccountUpdateRequest();
                return api.AccountUpdateWithHttpInfo(updateRequest);
            case "accountVerify":
                var verifyRequest = JsonConvert.DeserializeObject<AccountVerifyRequest>(data.ToString()) ?? new AccountVerifyRequest();
                return api.AccountVerifyWithHttpInfo(verifyRequest);
        }

        return null;
    }

    private IApiResponse? ApiAppApi()
    {
        var api = new ApiAppApi(GetConfiguration());
        var customLogoFile = GetFile("custom_logo_file");

        switch (operationId)
        {
            case "apiAppCreate":
                var createRequest = JsonConvert.DeserializeObject<ApiAppCreateRequest>(data.ToString()) ?? new ApiAppCreateRequest();
                if (customLogoFile != null)
                {
                    createRequest.CustomLogoFile = customLogoFile;
                }
                return api.ApiAppCreateWithHttpInfo(createRequest);
            case "apiAppDelete":
                return api.ApiAppDeleteWithHttpInfo(GetParamValue("client_id"));
            case "apiAppGet":
                return api.ApiAppGetWithHttpInfo(GetParamValue("client_id"));
            case "apiAppList":
                return api.ApiAppListWithHttpInfo(
                    int.Parse(GetParamValue("page", "1")),
                    int.Parse(GetParamValue("page_size", "20"))
                    );
            case "apiAppUpdate":
                var updateRequest = JsonConvert.DeserializeObject<ApiAppUpdateRequest>(data.ToString()) ?? new ApiAppUpdateRequest();
                if (customLogoFile != null)
                {
                    updateRequest.CustomLogoFile = customLogoFile;
                }

                return api.ApiAppUpdateWithHttpInfo(GetParamValue("client_id"), updateRequest);
        }

        return null;
    }

    private IApiResponse? BulkSendJobApi()
    {
        var api = new BulkSendJobApi(GetConfiguration());
        switch (operationId)
        {
            case "bulkSendJobGet":
                return api.BulkSendJobGetWithHttpInfo(GetParamValue("bulk_send_job_id"));
            case "bulkSendJobList":
                return api.BulkSendJobListWithHttpInfo(
                    int.Parse(GetParamValue("page", "1")),
                    int.Parse(GetParamValue("page_size", "20"))
                );
        }
        return null;
    }

    private IApiResponse? EmbeddedApi()
    {
        var api = new EmbeddedApi(GetConfiguration());
        switch (operationId) {
            case "embeddedEditUrl":
                var editUrlRequest = JsonConvert.DeserializeObject<EmbeddedEditUrlRequest>(data.ToString()) ?? new EmbeddedEditUrlRequest();
                return api.EmbeddedEditUrlWithHttpInfo(GetParamValue("template_id"), editUrlRequest);
            case "embeddedSignUrl":
                return api.EmbeddedSignUrlWithHttpInfo(GetParamValue("embeddedSignUrl"));
        }
        return null;
    }

    private IApiResponse? OauthApi()
    {
        var api = new OAuthApi(GetConfiguration());
        switch (operationId) {
            case "oauthTokenGenerate":
                var generateRequest = JsonConvert.DeserializeObject<OAuthTokenGenerateRequest>(data.ToString()) ?? new OAuthTokenGenerateRequest();
                return api.OauthTokenGenerateWithHttpInfo(generateRequest);
            case "oauthTokenRefresh":
                var refreshRequest = JsonConvert.DeserializeObject<OAuthTokenRefreshRequest>(data.ToString()) ?? new OAuthTokenRefreshRequest();
                return api.OauthTokenRefreshWithHttpInfo(refreshRequest);
        }
        return null;
    }

    private IApiResponse? ReportApi()
    {
        var api = new ReportApi(GetConfiguration());
        switch (operationId) {
            case "reportCreate":
                var createRequest = JsonConvert.DeserializeObject<ReportCreateRequest>(data.ToString()) ?? new ReportCreateRequest();
                return api.ReportCreateWithHttpInfo(createRequest);
        }
        return null;
    }

    private IApiResponse? SignatureRequestApi()
    {
        var api = new SignatureRequestApi(GetConfiguration());
        var file = GetFiles("file");
        var signerFile = GetFile("signer_file");
        switch (operationId)
        {
            case "signatureRequestBulkCreateEmbeddedWithTemplate":
                var templateRequest = JsonConvert.DeserializeObject<SignatureRequestBulkCreateEmbeddedWithTemplateRequest>(data.ToString()) ??
                                                                            new SignatureRequestBulkCreateEmbeddedWithTemplateRequest();
                if (signerFile != null)
                {
                    templateRequest.SignerFile = signerFile;
                }

                return api.SignatureRequestBulkCreateEmbeddedWithTemplateWithHttpInfo(templateRequest);
            case "signatureRequestBulkSendWithTemplate":
                var withTemplateRequest =
                    JsonConvert.DeserializeObject<SignatureRequestBulkSendWithTemplateRequest>(data.ToString()) ??
                    new SignatureRequestBulkSendWithTemplateRequest();
                if (signerFile != null)
                {
                    withTemplateRequest.SignerFile = signerFile;
                }

                return api.SignatureRequestBulkSendWithTemplateWithHttpInfo(withTemplateRequest);
            case "signatureRequestCancel":
                return api.SignatureRequestCancelWithHttpInfo(GetParamValue("signature_request_id"));
            case "signatureRequestCreateEmbedded":
                var embeddedRequest = JsonConvert.DeserializeObject<SignatureRequestCreateEmbeddedRequest>(data.ToString()) ??
                                                            new SignatureRequestCreateEmbeddedRequest();
                if (file != null)
                {
                    embeddedRequest.File = file;
                }

                return api.SignatureRequestCreateEmbeddedWithHttpInfo(embeddedRequest);
            case "signatureRequestCreateEmbeddedWithTemplate":
                var embeddedWithTemplateRequest = JsonConvert.DeserializeObject<SignatureRequestCreateEmbeddedWithTemplateRequest>(data.ToString()) ??
                                      new SignatureRequestCreateEmbeddedWithTemplateRequest();
                if (file != null)
                {
                    embeddedWithTemplateRequest.File = file;
                }

                return api.SignatureRequestCreateEmbeddedWithTemplateWithHttpInfo(embeddedWithTemplateRequest);
            case "signatureRequestFilesAsFileUrl":
                return api.SignatureRequestFilesAsFileUrlWithHttpInfo(
                    GetParamValue("signature_request_id")
                );
            case "signatureRequestGet":
                return api.SignatureRequestGetWithHttpInfo(GetParamValue("signature_request_id"));
            case "signatureRequestList":
                return api.SignatureRequestListWithHttpInfo(
                    GetParamValue("account_id"),
                    int.Parse(GetParamValue("page", "1")),
                    int.Parse(GetParamValue("page_size", "20")),
                    GetParamValue("query"));
            case "signatureRequestReleaseHold":
                return api.SignatureRequestReleaseHoldWithHttpInfo(GetParamValue("signature_request_id"));
            case "signatureRequestRemind":
                var remindRequest =
                    JsonConvert.DeserializeObject<SignatureRequestRemindRequest>(data.ToString()) ??
                    new SignatureRequestRemindRequest();
                return api.SignatureRequestRemindWithHttpInfo(GetParamValue("signature_request_id"), remindRequest);
            case "signatureRequestRemove":
                return api.SignatureRequestRemoveWithHttpInfo(GetParamValue("signature_request_id"));
            case "signatureRequestSend":
                var sendRequest = JsonConvert.DeserializeObject<SignatureRequestSendRequest>(data.ToString()) ?? new SignatureRequestSendRequest();
                if (file != null)
                {
                    sendRequest.File = file;
                }
                return api.SignatureRequestSendWithHttpInfo(sendRequest);
            case "signatureRequestSendWithTemplate":
                var sendWithTemplateRequest = JsonConvert.DeserializeObject<SignatureRequestSendWithTemplateRequest>(data.ToString()) ??
                                                              new SignatureRequestSendWithTemplateRequest();
                if (file != null)
                {
                    sendWithTemplateRequest.File = file;
                }
                return api.SignatureRequestSendWithTemplateWithHttpInfo(sendWithTemplateRequest);
            case "signatureRequestUpdate":
                var updateRequest = JsonConvert.DeserializeObject<SignatureRequestUpdateRequest>(data.ToString()) ?? new SignatureRequestUpdateRequest();
                return api.SignatureRequestUpdateWithHttpInfo(GetParamValue("signature_request_id"), updateRequest);
        }

        return null;
    }

    private IApiResponse? TeamApi()
    {
        var api = new TeamApi(GetConfiguration());
        switch (operationId) {
            case "teamAddMember":
                var addMemberRequest =
                    JsonConvert.DeserializeObject<TeamAddMemberRequest>(data.ToString()) ?? new TeamAddMemberRequest();
                return api.TeamAddMemberWithHttpInfo(addMemberRequest, GetParamValue("team_id"));
            case "teamCreate":
                var createRequest = JsonConvert.DeserializeObject<TeamCreateRequest>(data.ToString()) ??
                                    new TeamCreateRequest();
                return api.TeamCreateWithHttpInfo(createRequest);
            case "teamDelete":
                return api.TeamDeleteWithHttpInfo();
            case "teamGet":
                return api.TeamGetWithHttpInfo();
            case "teamRemoveMember":
                var removeMemberRequest =
                    JsonConvert.DeserializeObject<TeamRemoveMemberRequest>(data.ToString()) ??
                    new TeamRemoveMemberRequest();
                return api.TeamRemoveMemberWithHttpInfo(removeMemberRequest);
            case "teamUpdate":
                var updateRequest = JsonConvert.DeserializeObject<TeamUpdateRequest>(data.ToString()) ??
                                    new TeamUpdateRequest();
                return api.TeamUpdateWithHttpInfo(updateRequest);
        }
        return null;
    }

    private IApiResponse? TemplateApi()
    {
        var api = new TemplateApi(GetConfiguration());
        var file = GetFiles("file");

        switch (operationId) {
            case "templateAddUser":
                var addUserRequest =
                    JsonConvert.DeserializeObject<TemplateAddUserRequest>(data.ToString()) ??
                    new TemplateAddUserRequest();
                return api.TemplateAddUserWithHttpInfo(GetParamValue("template_id"), addUserRequest);
            case "templateCreateEmbeddedDraft":
                var embeddedDraftRequest
                        = JsonConvert.DeserializeObject<TemplateCreateEmbeddedDraftRequest>(data.ToString()) ??
                          new TemplateCreateEmbeddedDraftRequest();
                return api.TemplateCreateEmbeddedDraftWithHttpInfo(embeddedDraftRequest);
            case "templateDelete":
                return api.TemplateDeleteWithHttpInfo(GetParamValue("template_id"));
            case "templateFilesAsFileUrl":
                return api.TemplateFilesAsFileUrlWithHttpInfo(
                    GetParamValue("template_id")
                );
            case "templateGet":
                return api.TemplateGetWithHttpInfo(GetParamValue("template_id"));
            case "templateList":
                return api.TemplateListWithHttpInfo(
                    GetParamValue("account_id"),
                    int.Parse(GetParamValue("page", "1")),
                        int.Parse(GetParamValue("page_size","20")),
                    GetParamValue("query")
                );
            case "templateRemoveUser":
                var removeUserRequest =
                    JsonConvert.DeserializeObject<TemplateRemoveUserRequest>(data.ToString()) ??
                    new TemplateRemoveUserRequest();
                return api.TemplateRemoveUserWithHttpInfo(GetParamValue("template_id"), removeUserRequest);
            case "templateUpdateFiles":
                var updateFilesRequest =
                    JsonConvert.DeserializeObject<TemplateUpdateFilesRequest>(data.ToString()) ??
                    new TemplateUpdateFilesRequest();
                if (file != null)
                {
                    updateFilesRequest.File = file;
                }
                return api.TemplateUpdateFilesWithHttpInfo(GetParamValue("template_id"), updateFilesRequest);
        }
        return null;
    }

    private IApiResponse? UnclaimedDraftApi()
    {
        var api = new UnclaimedDraftApi(GetConfiguration());
        var file = GetFiles("file");

        switch (operationId) {
            case "unclaimedDraftCreate":
                var createRequest =
                    JsonConvert.DeserializeObject<UnclaimedDraftCreateRequest>(data.ToString()) ??
                    new UnclaimedDraftCreateRequest();
                if (file != null)
                {
                    createRequest.File = file;
                }
                return api.UnclaimedDraftCreateWithHttpInfo(createRequest);
            case "unclaimedDraftCreateEmbedded":
                var createEmbeddedRequest =
                    JsonConvert.DeserializeObject<UnclaimedDraftCreateEmbeddedRequest>(data.ToString()) ??
                    new UnclaimedDraftCreateEmbeddedRequest();
                if (file != null)
                {
                    createEmbeddedRequest.File = file;
                }
                return api.UnclaimedDraftCreateEmbeddedWithHttpInfo(createEmbeddedRequest);
            case "unclaimedDraftCreateEmbeddedWithTemplate":
                var embeddedWithTemplateRequest =
                    JsonConvert.DeserializeObject<UnclaimedDraftCreateEmbeddedWithTemplateRequest>(data.ToString()) ??
                    new UnclaimedDraftCreateEmbeddedWithTemplateRequest();
                if (file != null)
                {
                    embeddedWithTemplateRequest.File = file;
                }
                return api.UnclaimedDraftCreateEmbeddedWithTemplateWithHttpInfo(embeddedWithTemplateRequest);
            case "unclaimedDraftEditAndResend":
                var resendRequest =
                    JsonConvert.DeserializeObject<UnclaimedDraftEditAndResendRequest>(data.ToString()) ??
                    new UnclaimedDraftEditAndResendRequest();
                return api.UnclaimedDraftEditAndResendWithHttpInfo(GetParamValue("signature_request_id"), resendRequest);
        }
        return null;
    }

    private Configuration GetConfiguration()
    {
        var config = new Configuration();
        if (!string.IsNullOrEmpty(apiServer))
        {
            config.BasePath = "https://" + apiServer + "/v3";
        }

        if (devMode)
        {
            config.DefaultHeaders.Add(new KeyValuePair<string, string>("Cookie", "XDEBUG_SESSION=xdebug"));
        }

        switch (authType)
        {
            case "apikey":
                config.Username = authKey;
                break;
            case "oauth":
                config.AccessToken = authKey;
                break;
            default:
                throw new Exception("Invalid auth type. Must be \"apikey\" or \"oauth\"");
        }

        return config;
    }

    private Stream? GetFile(string name)
    {
        var filename = files?[name]?.ToString();
        return filename == null ? null : new StreamReader(FILE_UPLOADS_DIR + $"/{filename}").BaseStream;
    }

    private List<Stream>? GetFiles(string name)
    {
        var jToken = files?[name];
        return jToken?.Select(filename => new StreamReader(FILE_UPLOADS_DIR + $"/{filename}").BaseStream).ToList();
    }

    private string GetParamValue(string parameterName, string defaultValue = "")
    {
        return parameters?[parameterName]?.ToString() ?? defaultValue;
    }

    static void Main(string[] args)
    {
        var authType = args[0];
        var authKey = args[1];
        var apiServer = args[2];
        var jsonData = args[3];
        var devMode = false;
        if (args.Length > 4)
        {
            devMode = int.Parse(args[4]) == 1;
        }

        var requester = new Requester(authType, authKey, apiServer, jsonData, devMode);
        requester.Run();
    }
}

