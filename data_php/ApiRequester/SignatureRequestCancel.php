<?php

class SignatureRequestCancel implements ApiRequesterI
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
        return $this->api->signatureRequestCancelWithHttpInfo(
            $parameters['signature_request_id'],
        );
    }
}
