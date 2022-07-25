<?php

class EmbeddedEditUrl implements ApiRequesterI
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
        $obj = HelloSignSDK\Model\EmbeddedEditUrlRequest::fromArray(
            $data,
        );

        return $this->api->embeddedEditUrlWithHttpInfo(
            $parameters['template_id'],
            $obj,
        );
    }
}
