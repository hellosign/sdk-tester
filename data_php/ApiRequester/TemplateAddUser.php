<?php

class TemplateAddUser implements ApiRequesterI
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
        $obj = HelloSignSDK\Model\TemplateAddUserRequest::fromArray(
            $data,
        );

        return $this->api->templateAddUserWithHttpInfo(
            $parameters['template_id'] ?? null,
            $obj,
        );
    }
}
