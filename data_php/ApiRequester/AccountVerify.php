<?php

class AccountVerify implements ApiRequesterI
{
    private HelloSignSDK\Api\AccountApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\AccountApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        $obj = HelloSignSDK\Model\AccountVerifyRequest::fromArray(
            $data,
        );

        return $this->api->accountVerifyWithHttpInfo(
            $obj,
        );
    }
}
