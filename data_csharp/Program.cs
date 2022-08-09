using System;
using System.Collections.Generic;
using Org.HelloSign.Api;
using Org.HelloSign.Client;
using Org.HelloSign.Model;


class Requester
{
    static void Main(string[] args)
    {
        string authType = args[0];
        string authKey = args[1];
        string apiServer = args[2];
        string jsonData = args[3];
        if (args.Length > 4)
        {
            bool devMode = int.Parse(args[4]) == 1;
        }

        var config = new Configuration();
        // Configure HTTP basic authorization: api_key
        config.Username = authKey;

        // or, configure Bearer (JWT) authorization: oauth2
        // config.AccessToken = "YOUR_BEARER_TOKEN";

        var apiInstance = new SignatureRequestApi(config);

        var accountId = "all";

        try
        {
            var result = apiInstance.SignatureRequestList(accountId);
            Console.WriteLine(result);
            //var header =  apiInstance.SignatureRequestListWithHttpInfo(accountId).Headers;
            //Console.WriteLine(header);

            //var signatureRequestId = "02627ce4985b8b70083c5916e2b2648993bfa4e1";
            //var result2 = apiInstance.SignatureRequestGet(signatureRequestId);
            //Console.WriteLine(result2);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling HelloSign API: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}

