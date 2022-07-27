<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once '/app/vendor/autoload.php';

class Requester
{
    private const LOCAL_FILE = '/data.json';

    private string $authType;

    private string $authKey;

    private array $data;

    private array $files;

    private string $operationId;

    private array $parameters;

    private string $server;

    public function __construct(
        string $authType,
        string $authKey,
        string $server,
        $jsonSource
    ) {
        $this->authType = strtolower($authType);
        $this->authKey = $authKey;
        $this->server = $server;

        $this->readJsonData($jsonSource);
    }

    public function run()
    {
        try {
            $response = $this->callFromOperationId();

            echo json_encode([
                'body'        => $response[0],
                'status_code' => $response[1],
                'headers'     => $this->getResponseHeaders(
                    $response[2]
                ),
            ], JSON_PRETTY_PRINT);
        } catch (HelloSignSDK\ApiException $e) {
            echo json_encode([
                'body'        => json_decode($e->getResponseBody()),
                'status_code' => json_decode($e->getCode()),
                'headers'     => $this->getResponseHeaders(
                    $e->getResponseHeaders()
                ),
            ], JSON_PRETTY_PRINT);
        }
    }

    private function getConfig(): HelloSignSDK\Configuration
    {
        $config = HelloSignSDK\Configuration::getDefaultConfiguration();
        $config->setHost("https://{$this->server}/v3");

        if ($this->authType === 'apikey') {
            $config->setUsername($this->authKey);
        } elseif ($this->authType === 'oauth') {
            $config->setAccessToken($this->authKey);
        } else {
            throw new Exception(
                'Invalid auth type. Must be "apikey" or "oauth".'
            );
        }

        return $config;
    }

    private function readJsonData($base64Json): void
    {
        if (!empty($base64Json) && is_string($base64Json)) {
            $json = json_decode(base64_decode($base64Json, true), true);

            if (json_last_error() !== JSON_ERROR_NONE || empty($json)) {
                throw new Exception('Invalid base64 JSON data provided.');
            }
        } elseif (file_exists(self::LOCAL_FILE)) {
            $json = json_decode(file_get_contents(self::LOCAL_FILE), true);

            if (json_last_error() !== JSON_ERROR_NONE || empty($json)) {
                throw new Exception('Invalid JSON file provided.');
            }
        }

        $this->operationId = $json['operationId'] ?? '';
        $this->data = $json['data'] ?? [];
        $this->files = $json['files'] ?? [];
        $this->parameters = $json['parameters'] ?? [];
    }

    private function callFromOperationId(): array
    {
        if ($response = $this->accountApi()) {
            return $response;
        }
        if ($response = $this->apiAppApi()) {
            return $response;
        }
        if ($response = $this->bulkSendJobApi()) {
            return $response;
        }
        if ($response = $this->embeddedApi()) {
            return $response;
        }
        if ($response = $this->oauthApi()) {
            return $response;
        }
        if ($response = $this->reportApi()) {
            return $response;
        }
        if ($response = $this->signatureRequestApi()) {
            return $response;
        }
        if ($response = $this->teamApi()) {
            return $response;
        }
        if ($response = $this->templateApi()) {
            return $response;
        }
        if ($response = $this->unclaimedDraftApi()) {
            return $response;
        }

        throw new Exception("Invalid operationId: {$this->operationId}");
    }

    private function getResponseHeaders(array $headers): array
    {
        $formatted = [];

        foreach ($headers as $k => $v) {
            if (count($v) > 1) {
                $formatted[strtolower($k)] = $v;

                continue;
            }

            $formatted[strtolower($k)] = array_pop($v);
        }

        return $formatted;
    }

    private function getFile(string $name): ?SplFileObject
    {
        if (!empty($this->files[$name])) {
            return new SplFileObject(
                "/file_uploads/{$this->files[$name]}",
            );
        }

        return null;
    }

    private function getFiles(string $name): array
    {
        $files = [];

        foreach ($this->files[$name] ?? [] as $file) {
            $files[] = new SplFileObject(
                "/file_uploads/{$file}",
            );
        }

        return $files;
    }

    private function accountApi(): ?array
    {
        $api = new HelloSignSDK\Api\AccountApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'accountCreate') {
            $obj = HelloSignSDK\Model\AccountCreateRequest::fromArray(
                $this->data,
            );

            return $api->accountCreateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'accountGet') {
            return $api->accountGetWithHttpInfo(
                $this->parameters['account_id'] ?? null,
            );
        }

        if ($this->operationId === 'accountUpdate') {
            $obj = HelloSignSDK\Model\AccountUpdateRequest::fromArray(
                $this->data,
            );

            return $api->accountUpdateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'accountVerify') {
            $obj = HelloSignSDK\Model\AccountVerifyRequest::fromArray(
                $this->data,
            );

            return $api->accountVerifyWithHttpInfo(
                $obj,
            );
        }

        return null;
    }

    private function apiAppApi(): ?array
    {
        $api = new HelloSignSDK\Api\ApiAppApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'apiAppCreate') {
            $obj = HelloSignSDK\Model\ApiAppCreateRequest::fromArray(
                $this->data,
            );

            $obj->setCustomLogoFile($this->getFile('custom_logo_file'));

            return $api->apiAppCreateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'apiAppDelete') {
            return $api->apiAppDeleteWithHttpInfo(
                $this->parameters['client_id'],
            );
        }

        if ($this->operationId === 'apiAppGet') {
            return $api->apiAppGetWithHttpInfo(
                $this->parameters['client_id'],
            );
        }

        if ($this->operationId === 'apiAppList') {
            return $api->apiAppListWithHttpInfo(
                $this->parameters['page'] ?? 1,
                $this->parameters['page_size'] ?? 20,
            );
        }

        if ($this->operationId === 'apiAppUpdate') {
            $obj = HelloSignSDK\Model\ApiAppUpdateRequest::fromArray(
                $this->data,
            );

            $obj->setCustomLogoFile($this->getFile('custom_logo_file'));

            return $api->apiAppUpdateWithHttpInfo(
                $this->parameters['client_id'],
                $obj,
            );
        }

        return null;
    }

    private function bulkSendJobApi(): ?array
    {
        $api = new HelloSignSDK\Api\BulkSendJobApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'bulkSendJobGet') {
            return $api->bulkSendJobGetWithHttpInfo(
                $this->parameters['bulk_send_job_id'],
            );
        }

        if ($this->operationId === 'bulkSendJobList') {
            return $api->bulkSendJobListWithHttpInfo(
                $this->parameters['page'] ?? 1,
                $this->parameters['page_size'] ?? 20,
            );
        }

        return null;
    }

    private function embeddedApi(): ?array
    {
        $api = new HelloSignSDK\Api\EmbeddedApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'embeddedEditUrl') {
            $obj = HelloSignSDK\Model\EmbeddedEditUrlRequest::fromArray(
                $this->data,
            );

            return $api->embeddedEditUrlWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        if ($this->operationId === 'embeddedSignUrl') {
            return $api->embeddedSignUrlWithHttpInfo(
                $this->parameters['signature_id'],
            );
        }

        return null;
    }

    private function oauthApi(): ?array
    {
        $api = new HelloSignSDK\Api\OAuthApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'oauthTokenGenerate') {
            $obj = HelloSignSDK\Model\OAuthTokenGenerateRequest::fromArray(
                $this->data,
            );

            return $api->oauthTokenGenerateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'oauthTokenRefresh') {
            $obj = HelloSignSDK\Model\OAuthTokenRefreshRequest::fromArray(
                $this->data,
            );

            return $api->oauthTokenRefreshWithHttpInfo(
                $obj,
            );
        }

        return null;
    }

    private function reportApi(): ?array
    {
        $api = new HelloSignSDK\Api\ReportApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'reportCreate') {
            $obj = HelloSignSDK\Model\ReportCreateRequest::fromArray(
                $this->data,
            );

            return $api->reportCreateWithHttpInfo(
                $obj,
            );
        }

        return null;
    }

    private function signatureRequestApi(): ?array
    {
        $api = new HelloSignSDK\Api\SignatureRequestApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'signatureRequestBulkCreateEmbeddedWithTemplate') {
            $obj = HelloSignSDK\Model\SignatureRequestBulkCreateEmbeddedWithTemplateRequest::fromArray(
                $this->data,
            );

            $obj->setSignerFile($this->getFile('signer_file'));

            return $api->signatureRequestBulkCreateEmbeddedWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestBulkSendWithTemplate') {
            $obj = HelloSignSDK\Model\SignatureRequestBulkSendWithTemplateRequest::fromArray(
                $this->data,
            );

            $obj->setSignerFile($this->getFile('signer_file'));

            return $api->signatureRequestBulkSendWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestCancel') {
            return $api->signatureRequestCancelWithHttpInfo(
                $this->parameters['signature_request_id'],
            );
        }

        if ($this->operationId === 'signatureRequestCreateEmbedded') {
            $obj = HelloSignSDK\Model\SignatureRequestCreateEmbeddedRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->signatureRequestCreateEmbeddedWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestCreateEmbeddedWithTemplate') {
            $obj = HelloSignSDK\Model\SignatureRequestCreateEmbeddedWithTemplateRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->signatureRequestCreateEmbeddedWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestFiles') {
            return $api->signatureRequestFilesWithHttpInfo(
                $this->parameters['signature_request_id'],
                $this->parameters['file_type'] ?? 'pdf',
                $this->parameters['get_url'] ?? false,
                $this->parameters['get_data_uri'] ?? false,
            );
        }

        if ($this->operationId === 'signatureRequestGet') {
            return $api->signatureRequestGetWithHttpInfo(
                $this->parameters['signature_request_id'],
            );
        }

        if ($this->operationId === 'signatureRequestList') {
            return $api->signatureRequestListWithHttpInfo(
                $this->parameters['account_id'] ?? null,
                $this->parameters['page'] ?? 1,
                $this->parameters['page_size'] ?? 20,
                $this->parameters['query'] ?? null,
            );
        }

        if ($this->operationId === 'signatureRequestReleaseHold') {
            return $api->signatureRequestReleaseHoldWithHttpInfo(
                $this->parameters['signature_request_id'],
            );
        }

        if ($this->operationId === 'signatureRequestRemind') {
            $obj = HelloSignSDK\Model\SignatureRequestRemindRequest::fromArray(
                $this->data,
            );

            return $api->signatureRequestRemindWithHttpInfo(
                $this->parameters['signature_request_id'],
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestRemove') {
            return $api->signatureRequestRemoveWithHttpInfo(
                $this->parameters['signature_request_id'],
            );
        }

        if ($this->operationId === 'signatureRequestSend') {
            $obj = HelloSignSDK\Model\SignatureRequestSendRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->signatureRequestSendWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestSendWithTemplate') {
            $obj = HelloSignSDK\Model\SignatureRequestSendWithTemplateRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->signatureRequestSendWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestUpdate') {
            $obj = HelloSignSDK\Model\SignatureRequestUpdateRequest::fromArray(
                $this->data,
            );

            return $api->signatureRequestUpdateWithHttpInfo(
                $this->parameters['signature_request_id'],
                $obj,
            );
        }

        return null;
    }

    private function teamApi(): ?array
    {
        $api = new HelloSignSDK\Api\TeamApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'teamAddMember') {
            $obj = HelloSignSDK\Model\TeamAddMemberRequest::fromArray(
                $this->data,
            );

            return $api->teamAddMemberWithHttpInfo(
                $obj,
                $this->parameters['team_id'] ?? null,
            );
        }

        if ($this->operationId === 'teamCreate') {
            $obj = HelloSignSDK\Model\TeamCreateRequest::fromArray(
                $this->data,
            );

            return $api->teamCreateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'teamDelete') {
            return $api->teamDeleteWithHttpInfo();
        }

        if ($this->operationId === 'teamGet') {
            return $api->teamGetWithHttpInfo();
        }

        if ($this->operationId === 'teamRemoveMember') {
            $obj = HelloSignSDK\Model\TeamRemoveMemberRequest::fromArray(
                $this->data,
            );

            return $api->teamRemoveMemberWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'teamUpdate') {
            $obj = HelloSignSDK\Model\TeamUpdateRequest::fromArray(
                $this->data,
            );

            return $api->teamUpdateWithHttpInfo(
                $obj,
            );
        }

        return null;
    }

    private function templateApi(): ?array
    {
        $api = new HelloSignSDK\Api\TemplateApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'templateAddUser') {
            $obj = HelloSignSDK\Model\TemplateAddUserRequest::fromArray(
                $this->data,
            );

            return $api->templateAddUserWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        if ($this->operationId === 'templateCreateEmbeddedDraft') {
            $obj = HelloSignSDK\Model\TemplateCreateEmbeddedDraftRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->templateCreateEmbeddedDraftWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'templateDelete') {
            return $api->templateDeleteWithHttpInfo(
                $this->parameters['template_id'],
            );
        }

        if ($this->operationId === 'templateFiles') {
            return $api->templateFilesWithHttpInfo(
                $this->parameters['template_id'],
                $this->parameters['file_type'] ?? null,
                $this->parameters['get_url'] ?? false,
                $this->parameters['get_data_uri'] ?? false,
            );
        }

        if ($this->operationId === 'templateGet') {
            return $api->templateGetWithHttpInfo(
                $this->parameters['template_id'],
            );
        }

        if ($this->operationId === 'templateList') {
            return $api->templateListWithHttpInfo(
                $this->parameters['account_id'] ?? null,
                $this->parameters['page'] ?? 1,
                $this->parameters['page_size'] ?? 20,
                $this->parameters['query'] ?? null,
            );
        }

        if ($this->operationId === 'templateRemoveUser') {
            $obj = HelloSignSDK\Model\TemplateRemoveUserRequest::fromArray(
                $this->data,
            );

            return $api->templateRemoveUserWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        if ($this->operationId === 'templateUpdateFiles') {
            $obj = HelloSignSDK\Model\TemplateUpdateFilesRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->templateUpdateFilesWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        return null;
    }

    private function unclaimedDraftApi(): ?array
    {
        $api = new HelloSignSDK\Api\UnclaimedDraftApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'unclaimedDraftCreate') {
            $obj = HelloSignSDK\Model\UnclaimedDraftCreateRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->unclaimedDraftCreateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'unclaimedDraftCreateEmbedded') {
            $obj = HelloSignSDK\Model\UnclaimedDraftCreateEmbeddedRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->unclaimedDraftCreateEmbeddedWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'unclaimedDraftCreateEmbeddedWithTemplate') {
            $obj = HelloSignSDK\Model\UnclaimedDraftCreateEmbeddedWithTemplateRequest::fromArray(
                $this->data,
            );

            $obj->setFile($this->getFiles('file'));

            return $api->unclaimedDraftCreateEmbeddedWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'unclaimedDraftEditAndResend') {
            $obj = HelloSignSDK\Model\UnclaimedDraftEditAndResendRequest::fromArray(
                $this->data,
            );

            return $api->unclaimedDraftEditAndResendWithHttpInfo(
                $this->parameters['signature_request_id'],
                $obj,
            );
        }

        return null;
    }
}

$requester = new Requester(
    getenv('AUTH_TYPE'),
    getenv('AUTH_KEY'),
    getenv('SERVER'),
    getenv('JSON_STRING'),
);

$requester->run();
