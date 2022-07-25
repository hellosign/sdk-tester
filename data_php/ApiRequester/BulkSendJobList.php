<?php

class BulkSendJobList implements ApiRequesterI
{
    private HelloSignSDK\Api\BulkSendJobApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\BulkSendJobApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        return $this->api->bulkSendJobListWithHttpInfo(
            $parameters['page'] ?? 1,
            $parameters['page_size'] ?? 20,
        );
    }
}
