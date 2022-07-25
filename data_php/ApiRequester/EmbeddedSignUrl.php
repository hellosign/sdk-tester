<?php

class EmbeddedSignUrl implements ApiRequesterI
{
    private HelloSignSDK\Api\EmbeddedApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\EmbeddedApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        return $this->api->embeddedSignUrlWithHttpInfo(
            $parameters['signature_id'],
        );
    }
}
