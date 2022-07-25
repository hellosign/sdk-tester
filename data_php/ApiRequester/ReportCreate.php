<?php

class ReportCreate implements ApiRequesterI
{
    private HelloSignSDK\Api\ReportApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\ReportApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        $obj = HelloSignSDK\Model\ReportCreateRequest::fromArray(
            $data,
        );

        return $this->api->reportCreateWithHttpInfo(
            $obj,
        );
    }
}
