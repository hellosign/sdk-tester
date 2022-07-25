<?php

class TemplateFiles implements ApiRequesterI
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
        return $this->api->templateFilesWithHttpInfo(
            $parameters['template_id'],
            $parameters['file_type'] ?? null,
            $parameters['get_url'] ?? false,
            $parameters['get_data_uri'] ?? false,
        );
    }
}
