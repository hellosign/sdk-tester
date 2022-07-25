<?php

class AccountGet implements ApiRequesterI
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
        return $this->api->accountGetWithHttpInfo(
            $parameters['account_id'] ?? null,
        );
    }
}
