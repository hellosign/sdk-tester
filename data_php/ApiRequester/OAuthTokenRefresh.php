<?php

class OAuthTokenRefresh implements ApiRequesterI
{
    private HelloSignSDK\Api\OAuthApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\OAuthApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        $obj = HelloSignSDK\Model\OAuthTokenRefreshRequest::fromArray(
            $data,
        );

        return $this->api->oauthTokenRefreshWithHttpInfo(
            $obj,
        );
    }
}
