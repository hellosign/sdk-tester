<?php

class TemplateList implements ApiRequesterI
{
    private HelloSignSDK\Api\TemplateApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\TemplateApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        return $this->api->templateListWithHttpInfo(
            $parameters['account_id'] ?? null,
            $parameters['page'] ?? 1,
            $parameters['page_size'] ?? 20,
            $parameters['query'] ?? null,
        );
    }
}
