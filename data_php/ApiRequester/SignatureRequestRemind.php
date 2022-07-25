<?php

class SignatureRequestRemind implements ApiRequesterI
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
        $obj = HelloSignSDK\Model\SignatureRequestRemindRequest::fromArray(
            $data,
        );

        return $this->api->signatureRequestRemindWithHttpInfo(
            $parameters['signature_request_id'],
            $obj,
        );
    }
}
