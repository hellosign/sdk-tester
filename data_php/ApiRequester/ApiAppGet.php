<?php

class ApiAppGet implements ApiRequesterI
{
    private HelloSignSDK\Api\ApiAppApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\ApiAppApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        return $this->api->apiAppGetWithHttpInfo(
            $parameters['client_id'],
        );
    }
}