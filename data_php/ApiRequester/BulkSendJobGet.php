<?php

class BulkSendJobGet implements ApiRequesterI
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
        return $this->api->bulkSendJobGetWithHttpInfo(
            $parameters['bulk_send_job_id'],
        );
    }
}
