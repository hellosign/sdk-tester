<?php

class SignatureRequestCreateEmbedded implements ApiRequesterI
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
        if (!empty($files['file'])) {
            $data['file'] = [];

            foreach ($files['file'] as $file) {
                $data['file'][] = new SplFileObject(
                    "/file_uploads/{$file}",
                );
            }
        }

        $obj = HelloSignSDK\Model\SignatureRequestCreateEmbeddedRequest::fromArray(
            $data,
        );

        return $this->api->signatureRequestCreateEmbeddedWithHttpInfo(
            $obj,
        );
    }
}
