using System;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Org.HelloSign.Api;
using Org.HelloSign.Client;
using Org.HelloSign.Model;
using JsonSerializer = System.Text.Json.JsonSerializer;


class Requester
{
    private string apiServer;
    private string authType;
    private string authKey;
    private JObject data = new();
    private bool devMode;
    private JObject files = new();
    private string? operationId;
    private JObject parameters = new();

    private readonly string FILE_UPLOADS_DIR =
         "/file_uploads"
        /*"/Users/fenghao/PhpstormProjects/openapi/hellosign-dotnet-sdk/RunSDK/file_uploads"*/;


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
            Console.WriteLine(JsonSerializer.Serialize(output));
        }
        catch (ApiException e)
        {
            var output = new Dictionary<string, object>
            {
                ["body"] = e.ErrorContent,
                ["status_code"] = e.ErrorCode,
                ["headers"] = e.Headers
            };
            Console.WriteLine(JsonSerializer.Serialize(output));
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
        files = filesObj as JObject ?? new JObject();
        parameters = parametersObj as JObject ??  new JObject();
    }

    private IApiResponse CallFromOperationId()
    {
        return ApiAppApi();
        //return SignatureRequestApi();
    }

    private IApiResponse AccountApi()
    {
        var accountApi = new AccountApi(GetConfiguration());
        parameters.TryGetValue("account_id", out var accountId);
        return accountApi.AccountGetWithHttpInfo(accountId?.ToString());
    }

    private IApiResponse ApiAppApi()
    {
        var api = new ApiAppApi(GetConfiguration());
        var apiAppCreateRequest = JsonConvert.DeserializeObject<ApiAppCreateRequest>(data.ToString()) ?? new ApiAppCreateRequest();
        var customLogoFile = GetFile("custom_logo_file");
        if (customLogoFile != null)
        {
            apiAppCreateRequest.CustomLogoFile = customLogoFile;
        }
        return api.ApiAppCreateWithHttpInfo(apiAppCreateRequest);
    }

    private IApiResponse SignatureRequestApi()
    {
        var api = new SignatureRequestApi(GetConfiguration());
        var sendRequest = JsonConvert.DeserializeObject<SignatureRequestSendRequest>(data.ToString()) ?? new SignatureRequestSendRequest();
        var file = GetFiles("file");
        if (file != null)
        {
            sendRequest.File = file;
        }
        return api.SignatureRequestSendWithHttpInfo(sendRequest);
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
        var filename = files[name]?.ToString();
        return filename == null ? null : new StreamReader(FILE_UPLOADS_DIR + $"/{filename}").BaseStream;
    }

    private List<Stream>? GetFiles(string name)
    {
        var jToken = files[name];
        return jToken?.Select(filename => new StreamReader(FILE_UPLOADS_DIR + $"/{filename}").BaseStream).ToList();
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

