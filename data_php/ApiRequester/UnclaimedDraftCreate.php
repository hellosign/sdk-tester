<?php

class UnclaimedDraftCreate implements ApiRequesterI
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
        if (!empty($files['file'])) {
            $data['file'] = [];

            foreach ($files['file'] as $file) {
                $data['file'][] = new SplFileObject(
                    "/file_uploads/{$file}",
                );
            }
        }

        $obj = HelloSignSDK\Model\UnclaimedDraftCreateRequest::fromArray(
            $data,
        );

        return $this->api->unclaimedDraftCreateWithHttpInfo(
            $obj,
        );
    }
}
