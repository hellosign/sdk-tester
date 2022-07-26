<?php

class TemplateUpdateFiles implements ApiRequesterI
{
    private HelloSignSDK\Api\TemplateApi $api;

    public function __construct(HelloSignSDK\Configuration $config)
    {
        $this->api = new HelloSignSDK\Api\TemplateApi(
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

        $obj = HelloSignSDK\Model\TemplateUpdateFilesRequest::fromArray(
            $data,
        );

        return $this->api->templateUpdateFilesWithHttpInfo(
            $parameters['template_id'],
            $obj,
        );
    }
}