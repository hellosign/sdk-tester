<?php

class SignatureRequestFiles implements ApiRequesterI
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
        return $this->api->signatureRequestBulkSendWithTemplateWithHttpInfo(
            $parameters['signature_request_id'],
            $parameters['file_type'] ?? 'pdf',
            $parameters['get_url'] ?? false,
            $parameters['get_data_uri'] ?? false,
        );
    }
}
