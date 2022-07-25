<?php

class SignatureRequestBulkCreateEmbeddedWithTemplate implements ApiRequesterI
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
        if (!empty($files['signer_file'])) {
            $data['signer_file'] = [];

            foreach ($files['signer_file'] as $file) {
                $data['signer_file'][] = new SplFileObject(
                    "/file_uploads/{$file}",
                );
            }
        }

        $obj = HelloSignSDK\Model\SignatureRequestBulkCreateEmbeddedWithTemplateRequest::fromArray(
            $data,
        );

        return $this->api->signatureRequestBulkCreateEmbeddedWithTemplateWithHttpInfo(
            $obj,
        );
    }
}
