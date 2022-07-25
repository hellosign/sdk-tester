<?php

class SignatureRequestList implements ApiRequesterI
{
    private HelloSignSDK\Api\SignatureRequestApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\SignatureRequestApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        return $this->api->signatureRequestListWithHttpInfo(
            $parameters['account_id'] ?? null,
            $parameters['page'] ?? 1,
            $parameters['page_size'] ?? 20,
            $parameters['query'] ?? null,
        );
    }
}
