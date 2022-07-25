<?php

class ApiAppCreate implements ApiRequesterI
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
        if (!empty($files['custom_logo_file'])) {
            $data['custom_logo_file'] = new SplFileObject(
                "/file_uploads/{$files['custom_logo_file']}",
            );
        }

        $obj = HelloSignSDK\Model\ApiAppCreateRequest::fromArray(
            $data,
        );

        return $this->api->apiAppCreateWithHttpInfo(
            $obj,
        );
    }
}
