<?php

class AccountUpdate implements ApiRequesterI
{
    private HelloSignSDK\Api\AccountApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\AccountApi(
            $config,
            new GuzzleHttp\Client(),
        );
    }

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array {
        $obj = HelloSignSDK\Model\AccountUpdateRequest::fromArray(
            $data,
        );

        return $this->api->accountUpdateWithHttpInfo(
            $obj,
        );
    }
}
