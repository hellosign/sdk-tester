<?php

namespace Dropox\Sign\Tester;

use Exception;
use GuzzleHttp;
use Dropbox\Sign as DropboxSign;
use SplFileObject;

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/vendor/autoload.php';

class Requester
{
    private const FILE_UPLOADS_DIR = __DIR__ . '/../file_uploads';

    private string $apiServer;

    private string $authType;

    private string $authKey;

    private array $data;

    private bool $devMode;

    private array $files;

    private string $operationId;

    private array $parameters;

    public function __construct(
        string $authType,
        string $authKey,
        string $apiServer,
        string $jsonData,
        $devMode = null
    ) {
        $this->authType = strtolower($authType);
        $this->authKey = $authKey;
        $this->apiServer = $apiServer;
        $this->devMode = filter_var($devMode, FILTER_VALIDATE_BOOLEAN);

        $this->readJsonData($jsonData);
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
        } catch (DropboxSign\ApiException $e) {
            echo json_encode([
                'body'        => json_decode($e->getResponseBody()),
                'status_code' => json_decode($e->getCode()),
                'headers'     => $this->getResponseHeaders(
                    $e->getResponseHeaders()
                ),
            ], JSON_PRETTY_PRINT);
        }
    }

    private function getConfig(): DropboxSign\Configuration
    {
        $config = DropboxSign\Configuration::getDefaultConfiguration();
        $config->setHost("https://{$this->apiServer}/v3");

        if ($this->authType === 'apikey') {
            $config->setUsername($this->authKey);
        } elseif ($this->authType === 'oauth') {
            $config->setAccessToken($this->authKey);
        } else {
            throw new Exception(
                'Invalid auth type. Must be "apikey" or "oauth".'
            );
        }

        if (!empty($this->devMode)) {
            $cookie = GuzzleHttp\Cookie\CookieJar::fromArray([
                'XDEBUG_SESSION' => 'xdebug',
            ], $this->apiServer);
            $config->setOptions(['cookies' => $cookie]);
        }

        return $config;
    }

    private function readJsonData(string $base64Json): void
    {
        if (!empty($base64Json)) {
            $json = json_decode(base64_decode($base64Json, true), true);

            if (json_last_error() !== JSON_ERROR_NONE || empty($json)) {
                throw new Exception('Invalid base64 JSON data provided.');
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
                self::FILE_UPLOADS_DIR . "/{$this->files[$name]}",
            );
        }

        return null;
    }

    /**
     * @return SplFileObject[]
     */
    private function getFiles(string $name): array
    {
        $files = [];

        foreach ($this->files[$name] ?? [] as $file) {
            $files[] = new SplFileObject(
                self::FILE_UPLOADS_DIR . "/{$file}",
            );
        }

        return $files;
    }

    private function accountApi(): ?array
    {
        $api = new DropboxSign\Api\AccountApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'accountCreate') {
            $obj = DropboxSign\Model\AccountCreateRequest::init(
                $this->data,
            );

            return $api->accountCreateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'accountGet') {
            return $api->accountGetWithHttpInfo(
                $this->parameters['account_id'] ?? null,
                $this->parameters['email_address'] ?? null,
            );
        }

        if ($this->operationId === 'accountUpdate') {
            $obj = DropboxSign\Model\AccountUpdateRequest::init(
                $this->data,
            );

            return $api->accountUpdateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'accountVerify') {
            $obj = DropboxSign\Model\AccountVerifyRequest::init(
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
        $api = new DropboxSign\Api\ApiAppApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'apiAppCreate') {
            $obj = DropboxSign\Model\ApiAppCreateRequest::init(
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
            $obj = DropboxSign\Model\ApiAppUpdateRequest::init(
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
        $api = new DropboxSign\Api\BulkSendJobApi(
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
        $api = new DropboxSign\Api\EmbeddedApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'embeddedEditUrl') {
            $obj = DropboxSign\Model\EmbeddedEditUrlRequest::init(
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
        $api = new DropboxSign\Api\OAuthApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'oauthTokenGenerate') {
            $obj = DropboxSign\Model\OAuthTokenGenerateRequest::init(
                $this->data,
            );

            return $api->oauthTokenGenerateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'oauthTokenRefresh') {
            $obj = DropboxSign\Model\OAuthTokenRefreshRequest::init(
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
        $api = new DropboxSign\Api\ReportApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'reportCreate') {
            $obj = DropboxSign\Model\ReportCreateRequest::init(
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
        $api = new DropboxSign\Api\SignatureRequestApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'signatureRequestBulkCreateEmbeddedWithTemplate') {
            $obj = DropboxSign\Model\SignatureRequestBulkCreateEmbeddedWithTemplateRequest::init(
                $this->data,
            );

            $obj->setSignerFile($this->getFile('signer_file'));

            return $api->signatureRequestBulkCreateEmbeddedWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestBulkSendWithTemplate') {
            $obj = DropboxSign\Model\SignatureRequestBulkSendWithTemplateRequest::init(
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
            $obj = DropboxSign\Model\SignatureRequestCreateEmbeddedRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->signatureRequestCreateEmbeddedWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestCreateEmbeddedWithTemplate') {
            $obj = DropboxSign\Model\SignatureRequestCreateEmbeddedWithTemplateRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->signatureRequestCreateEmbeddedWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestFilesAsFileUrl') {
            return $api->signatureRequestFilesAsFileUrlWithHttpInfo(
                $this->parameters['signature_request_id']
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
            $obj = DropboxSign\Model\SignatureRequestRemindRequest::init(
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
            $obj = DropboxSign\Model\SignatureRequestSendRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->signatureRequestSendWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestSendWithTemplate') {
            $obj = DropboxSign\Model\SignatureRequestSendWithTemplateRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->signatureRequestSendWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'signatureRequestUpdate') {
            $obj = DropboxSign\Model\SignatureRequestUpdateRequest::init(
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
        $api = new DropboxSign\Api\TeamApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'teamAddMember') {
            $obj = DropboxSign\Model\TeamAddMemberRequest::init(
                $this->data,
            );

            return $api->teamAddMemberWithHttpInfo(
                $obj,
                $this->parameters['team_id'] ?? null,
            );
        }

        if ($this->operationId === 'teamCreate') {
            $obj = DropboxSign\Model\TeamCreateRequest::init(
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
            $obj = DropboxSign\Model\TeamRemoveMemberRequest::init(
                $this->data,
            );

            return $api->teamRemoveMemberWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'teamUpdate') {
            $obj = DropboxSign\Model\TeamUpdateRequest::init(
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
        $api = new DropboxSign\Api\TemplateApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'templateAddUser') {
            $obj = DropboxSign\Model\TemplateAddUserRequest::init(
                $this->data,
            );

            return $api->templateAddUserWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        if ($this->operationId === 'templateCreateEmbeddedDraft') {
            $obj = DropboxSign\Model\TemplateCreateEmbeddedDraftRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->templateCreateEmbeddedDraftWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'templateDelete') {
            return $api->templateDeleteWithHttpInfo(
                $this->parameters['template_id'],
            );
        }

        if ($this->operationId === 'templateFilesAsFileUrl') {
            return $api->templateFilesAsFileUrlWithHttpInfo(
                $this->parameters['template_id']
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
            $obj = DropboxSign\Model\TemplateRemoveUserRequest::init(
                $this->data,
            );

            return $api->templateRemoveUserWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        if ($this->operationId === 'templateUpdateFiles') {
            $obj = DropboxSign\Model\TemplateUpdateFilesRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->templateUpdateFilesWithHttpInfo(
                $this->parameters['template_id'],
                $obj,
            );
        }

        return null;
    }

    private function unclaimedDraftApi(): ?array
    {
        $api = new DropboxSign\Api\UnclaimedDraftApi(
            $this->getConfig(),
            new GuzzleHttp\Client(),
        );

        if ($this->operationId === 'unclaimedDraftCreate') {
            $obj = DropboxSign\Model\UnclaimedDraftCreateRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->unclaimedDraftCreateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'unclaimedDraftCreateEmbedded') {
            $obj = DropboxSign\Model\UnclaimedDraftCreateEmbeddedRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->unclaimedDraftCreateEmbeddedWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'unclaimedDraftCreateEmbeddedWithTemplate') {
            $obj = DropboxSign\Model\UnclaimedDraftCreateEmbeddedWithTemplateRequest::init(
                $this->data,
            );
            $obj->setFiles($this->getFiles('files'));

            return $api->unclaimedDraftCreateEmbeddedWithTemplateWithHttpInfo(
                $obj,
            );
        }

        if ($this->operationId === 'unclaimedDraftEditAndResend') {
            $obj = DropboxSign\Model\UnclaimedDraftEditAndResendRequest::init(
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
    getenv('API_SERVER'),
    getenv('JSON_DATA'),
    getenv('DEV_MODE'),
);

$requester->run();
