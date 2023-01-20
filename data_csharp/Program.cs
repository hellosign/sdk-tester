using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Dropbox.Sign.Api;
using Dropbox.Sign.Client;
using Dropbox.Sign.Model;

class Requester
{
    private string _apiServer;
    private string _authType;
    private string _authKey;
    private JObject _data = new();
    private bool _devMode;
    private JObject? _files;
    private string? _operationId;
    private JObject? _parameters;

    private readonly string FILE_UPLOADS_DIR = "/file_uploads";

    public Requester(string authType, string authKey, string apiServer, string jsonData, bool devMode)
    {
        this._authType = authType.ToLower();
        this._authKey = authKey;
        this._apiServer = apiServer;
        this._devMode = devMode;
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
        _operationId =  dictionary["operationId"] as string;
        dictionary.TryGetValue("data", out var dataObj );
        dictionary.TryGetValue("files", out var filesObj);
        dictionary.TryGetValue("parameters", out var parametersObj);

        _data = dataObj as JObject ?? new JObject();
        _files = filesObj as JObject;
        _parameters = parametersObj as JObject;
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
               throw new Exception($"Invalid operationId: {_operationId}");
    }

    private static T Init<T>(JObject data)
    {
        var obj = JsonConvert.DeserializeObject<T>(data.ToString());

        if (obj == null)
        {
            throw new Exception("Unable to deserialize object");
        }

        return obj;
    }

    private IApiResponse? AccountApi()
    {
        var api = new AccountApi(GetConfiguration());
        switch (_operationId)
        {
            case "accountCreate":
                var createRequest = Init<AccountCreateRequest>(_data);
                return api.AccountCreateWithHttpInfo(createRequest);
            case "accountGet":
                return api.AccountGetWithHttpInfo(_parameters?["account_id"]?.ToString(), _parameters?["email_address"]?.ToString());
            case "accountUpdate":
                var updateRequest = Init<AccountUpdateRequest>(_data);
                return api.AccountUpdateWithHttpInfo(updateRequest);
            case "accountVerify":
                var verifyRequest = Init<AccountVerifyRequest>(_data);
                return api.AccountVerifyWithHttpInfo(verifyRequest);
        }

        return null;
    }

    private IApiResponse? ApiAppApi()
    {
        var api = new ApiAppApi(GetConfiguration());
        var customLogoFile = GetFile("custom_logo_file");

        switch (_operationId)
        {
            case "apiAppCreate":
                var createRequest = Init<ApiAppCreateRequest>(_data);
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
                var updateRequest = Init<ApiAppUpdateRequest>(_data);
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
        switch (_operationId)
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
        switch (_operationId) {
            case "embeddedEditUrl":
                var editUrlRequest = Init<EmbeddedEditUrlRequest>(_data);
                return api.EmbeddedEditUrlWithHttpInfo(GetParamValue("template_id"), editUrlRequest);
            case "embeddedSignUrl":
                return api.EmbeddedSignUrlWithHttpInfo(GetParamValue("embeddedSignUrl"));
        }
        return null;
    }

    private IApiResponse? OauthApi()
    {
        var api = new OAuthApi(GetConfiguration());
        switch (_operationId) {
            case "oauthTokenGenerate":
                var generateRequest = Init<OAuthTokenGenerateRequest>(_data);
                return api.OauthTokenGenerateWithHttpInfo(generateRequest);
            case "oauthTokenRefresh":
                var refreshRequest = Init<OAuthTokenRefreshRequest>(_data);
                return api.OauthTokenRefreshWithHttpInfo(refreshRequest);
        }
        return null;
    }

    private IApiResponse? ReportApi()
    {
        var api = new ReportApi(GetConfiguration());
        switch (_operationId) {
            case "reportCreate":
                var createRequest = Init<ReportCreateRequest>(_data);
                return api.ReportCreateWithHttpInfo(createRequest);
        }
        return null;
    }

    private IApiResponse? SignatureRequestApi()
    {
        var api = new SignatureRequestApi(GetConfiguration());
        var files = GetFiles("files");
        var signerFile = GetFile("signer_file");
        switch (_operationId)
        {
            case "signatureRequestBulkCreateEmbeddedWithTemplate":
                var templateRequest = Init<SignatureRequestBulkCreateEmbeddedWithTemplateRequest>(_data);
                if (signerFile != null)
                {
                    templateRequest.SignerFile = signerFile;
                }

                return api.SignatureRequestBulkCreateEmbeddedWithTemplateWithHttpInfo(templateRequest);
            case "signatureRequestBulkSendWithTemplate":
                var withTemplateRequest = Init<SignatureRequestBulkSendWithTemplateRequest>(_data);
                if (signerFile != null)
                {
                    withTemplateRequest.SignerFile = signerFile;
                }

                return api.SignatureRequestBulkSendWithTemplateWithHttpInfo(withTemplateRequest);
            case "signatureRequestCancel":
                return api.SignatureRequestCancelWithHttpInfo(GetParamValue("signature_request_id"));
            case "signatureRequestCreateEmbedded":
                var embeddedRequest = Init<SignatureRequestCreateEmbeddedRequest>(_data);
                if (files != null)
                {
                    embeddedRequest.Files = files;
                }

                return api.SignatureRequestCreateEmbeddedWithHttpInfo(embeddedRequest);
            case "signatureRequestCreateEmbeddedWithTemplate":
                var embeddedWithTemplateRequest = Init<SignatureRequestCreateEmbeddedWithTemplateRequest>(_data);
                if (files != null)
                {
                    embeddedWithTemplateRequest.Files = files;
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
                var remindRequest = Init<SignatureRequestRemindRequest>(_data);
                return api.SignatureRequestRemindWithHttpInfo(GetParamValue("signature_request_id"), remindRequest);
            case "signatureRequestRemove":
                return api.SignatureRequestRemoveWithHttpInfo(GetParamValue("signature_request_id"));
            case "signatureRequestSend":
                var sendRequest = Init<SignatureRequestSendRequest>(_data);
                if (files != null)
                {
                    sendRequest.Files = files;
                }
                return api.SignatureRequestSendWithHttpInfo(sendRequest);
            case "signatureRequestSendWithTemplate":
                var sendWithTemplateRequest = Init<SignatureRequestSendWithTemplateRequest>(_data);
                if (files != null)
                {
                    sendWithTemplateRequest.Files = files;
                }
                return api.SignatureRequestSendWithTemplateWithHttpInfo(sendWithTemplateRequest);
            case "signatureRequestUpdate":
                var updateRequest = Init<SignatureRequestUpdateRequest>(_data);
                return api.SignatureRequestUpdateWithHttpInfo(GetParamValue("signature_request_id"), updateRequest);
        }

        return null;
    }

    private IApiResponse? TeamApi()
    {
        var api = new TeamApi(GetConfiguration());
        switch (_operationId) {
            case "teamAddMember":
                var addMemberRequest = Init<TeamAddMemberRequest>(_data);
                return api.TeamAddMemberWithHttpInfo(addMemberRequest, GetParamValue("team_id"));
            case "teamCreate":
                var createRequest = Init<TeamCreateRequest>(_data);
                return api.TeamCreateWithHttpInfo(createRequest);
            case "teamDelete":
                return api.TeamDeleteWithHttpInfo();
            case "teamGet":
                return api.TeamGetWithHttpInfo();
            case "teamRemoveMember":
                var removeMemberRequest = Init<TeamRemoveMemberRequest>(_data);
                return api.TeamRemoveMemberWithHttpInfo(removeMemberRequest);
            case "teamUpdate":
                var updateRequest = Init<TeamUpdateRequest>(_data);
                return api.TeamUpdateWithHttpInfo(updateRequest);
        }
        return null;
    }

    private IApiResponse? TemplateApi()
    {
        var api = new TemplateApi(GetConfiguration());
        var files = GetFiles("files");

        switch (_operationId) {
            case "templateAddUser":
                var addUserRequest = Init<TemplateAddUserRequest>(_data);
                return api.TemplateAddUserWithHttpInfo(GetParamValue("template_id"), addUserRequest);
            case "templateCreateEmbeddedDraft":
                var embeddedDraftRequest = Init<TemplateCreateEmbeddedDraftRequest>(_data);
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
                var removeUserRequest = Init<TemplateRemoveUserRequest>(_data);
                return api.TemplateRemoveUserWithHttpInfo(GetParamValue("template_id"), removeUserRequest);
            case "templateUpdateFiles":
                var updateFilesRequest = Init<TemplateUpdateFilesRequest>(_data);
                if (files != null)
                {
                    updateFilesRequest.Files = files;
                }
                return api.TemplateUpdateFilesWithHttpInfo(GetParamValue("template_id"), updateFilesRequest);
        }
        return null;
    }

    private IApiResponse? UnclaimedDraftApi()
    {
        var api = new UnclaimedDraftApi(GetConfiguration());
        var files = GetFiles("files");

        switch (_operationId) {
            case "unclaimedDraftCreate":
                var createRequest = Init<UnclaimedDraftCreateRequest>(_data);
                if (files != null)
                {
                    createRequest.Files = files;
                }
                return api.UnclaimedDraftCreateWithHttpInfo(createRequest);
            case "unclaimedDraftCreateEmbedded":
                var createEmbeddedRequest = Init<UnclaimedDraftCreateEmbeddedRequest>(_data);
                if (files != null)
                {
                    createEmbeddedRequest.Files = files;
                }
                return api.UnclaimedDraftCreateEmbeddedWithHttpInfo(createEmbeddedRequest);
            case "unclaimedDraftCreateEmbeddedWithTemplate":
                var embeddedWithTemplateRequest = Init<UnclaimedDraftCreateEmbeddedWithTemplateRequest>(_data);
                if (files != null)
                {
                    embeddedWithTemplateRequest.Files = files;
                }
                return api.UnclaimedDraftCreateEmbeddedWithTemplateWithHttpInfo(embeddedWithTemplateRequest);
            case "unclaimedDraftEditAndResend":
                var resendRequest = Init<UnclaimedDraftEditAndResendRequest>(_data);
                return api.UnclaimedDraftEditAndResendWithHttpInfo(GetParamValue("signature_request_id"), resendRequest);
        }
        return null;
    }

    private Configuration GetConfiguration()
    {
        var config = new Configuration();
        if (!string.IsNullOrEmpty(_apiServer))
        {
            config.BasePath = "https://" + _apiServer + "/v3";
        }

        if (_devMode)
        {
            config.DefaultHeaders.Add(new KeyValuePair<string, string>("Cookie", "XDEBUG_SESSION=xdebug"));
        }

        switch (_authType)
        {
            case "apikey":
                config.Username = _authKey;
                break;
            case "oauth":
                config.AccessToken = _authKey;
                break;
            default:
                throw new Exception("Invalid auth type. Must be \"apikey\" or \"oauth\"");
        }

        return config;
    }

    private Stream? GetFile(string name)
    {
        var filename = _files?[name]?.ToString();
        return filename == null ? null : new StreamReader(FILE_UPLOADS_DIR + $"/{filename}").BaseStream;
    }

    private List<Stream>? GetFiles(string name)
    {
        var jToken = _files?[name];
        return jToken?.Select(filename => new StreamReader(FILE_UPLOADS_DIR + $"/{filename}").BaseStream).ToList();
    }

    private string GetParamValue(string parameterName, string defaultValue = "")
    {
        return _parameters?[parameterName]?.ToString() ?? defaultValue;
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
