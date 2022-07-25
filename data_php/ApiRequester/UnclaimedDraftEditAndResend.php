<?php

class UnclaimedDraftEditAndResend implements ApiRequesterI
{
    private HelloSignSDK\Api\UnclaimedDraftApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\UnclaimedDraftApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        $obj = HelloSignSDK\Model\UnclaimedDraftEditAndResendRequest::fromArray(
            $data,
        );

        return $this->api->unclaimedDraftEditAndResendWithHttpInfo(
            $parameters['signature_request_id'],
            $obj,
        );
    }
}
