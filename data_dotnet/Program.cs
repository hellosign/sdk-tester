using System;
using System.Collections.Generic;
using Org.HelloSign.Api;
using Org.HelloSign.Client;
using Org.HelloSign.Model;

var config = new Configuration();
// Configure HTTP basic authorization: api_key
config.Username = "f405ae7d0b867fe9881a0ceb41154b6862d535b011ab77a28dbbccd68c70fe0b";

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