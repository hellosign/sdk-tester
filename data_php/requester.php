<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once '/app/vendor/autoload.php';

spl_autoload_register(function (string $class) {
    if (!file_exists("/ApiRequester/{$class}.php")) {
        return;
    }

    require_once "/ApiRequester/{$class}.php";
});

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
        $apiRequester = $this->classFromOperationId();

        try {
            $response = $apiRequester->run(
                $this->parameters,
                $this->data,
                $this->files,
            );

            echo json_encode([
                'body'        => $response[0],
                'status_code' => $response[1],
                'headers'     => $response[2],
            ], JSON_PRETTY_PRINT);
        } catch (HelloSignSDK\ApiException $e) {
            echo json_encode([
                'body'        => json_decode($e->getResponseBody()),
                'status_code' => json_decode($e->getCode()),
                'headers'     => $e->getResponseHeaders(),
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

    private function classFromOperationId(): ApiRequesterI
    {
        $config = $this->getConfig();

        switch ($this->operationId) {
            case 'accountCreate':
                return new AccountCreate($config);
            case 'accountGet':
                return new AccountGet($config);
            case 'accountUpdate':
                return new AccountUpdate($config);
            case 'accountVerify':
                return new AccountVerify($config);
            case 'apiAppCreate':
                return new ApiAppCreate($config);
            case 'apiAppGet':
                return new ApiAppGet($config);
            case 'apiAppUpdate':
                return new ApiAppUpdate($config);
            case 'apiAppDelete':
                return new ApiAppDelete($config);
            case 'apiAppList':
                return new ApiAppList($config);
            case 'bulkSendJobGet':
                return new BulkSendJobGet($config);
            case 'bulkSendJobList':
                return new BulkSendJobList($config);
            case 'embeddedEditUrl':
                return new EmbeddedEditUrl($config);
            case 'embeddedSignUrl':
                return new EmbeddedSignUrl($config);
            case 'oauthTokenGenerate':
                return new OauthTokenGenerate($config);
            case 'oauthTokenRefresh':
                return new OauthTokenRefresh($config);
            case 'reportCreate':
                return new ReportCreate($config);
            case 'signatureRequestBulkCreateEmbeddedWithTemplate':
                return new SignatureRequestBulkCreateEmbeddedWithTemplate($config);
            case 'signatureRequestBulkSendWithTemplate':
                return new SignatureRequestBulkSendWithTemplate($config);
            case 'signatureRequestCancel':
                return new SignatureRequestCancel($config);
            case 'signatureRequestCreateEmbedded':
                return new SignatureRequestCreateEmbedded($config);
            case 'signatureRequestCreateEmbeddedWithTemplate':
                return new SignatureRequestCreateEmbeddedWithTemplate($config);
            case 'signatureRequestFiles':
                return new SignatureRequestFiles($config);
            case 'signatureRequestGet':
                return new SignatureRequestGet($config);
            case 'signatureRequestList':
                return new SignatureRequestList($config);
            case 'signatureRequestReleaseHold':
                return new SignatureRequestReleaseHold($config);
            case 'signatureRequestRemind':
                return new SignatureRequestRemind($config);
            case 'signatureRequestRemove':
                return new SignatureRequestRemove($config);
            case 'signatureRequestSend':
                return new SignatureRequestSend($config);
            case 'signatureRequestSendWithTemplate':
                return new SignatureRequestSendWithTemplate($config);
            case 'signatureRequestUpdate':
                return new SignatureRequestUpdate($config);
            case 'teamAddMember':
                return new TeamAddMember($config);
            case 'teamCreate':
                return new TeamCreate($config);
            case 'teamDelete':
                return new TeamDelete($config);
            case 'teamGet':
                return new TeamGet($config);
            case 'teamUpdate':
                return new TeamUpdate($config);
            case 'teamRemoveMember':
                return new TeamRemoveMember($config);
            case 'templateAddUser':
                return new TemplateAddUser($config);
            case 'templateCreateEmbeddedDraft':
                return new TemplateCreateEmbeddedDraft($config);
            case 'templateDelete':
                return new TemplateDelete($config);
            case 'templateFiles':
                return new TemplateFiles($config);
            case 'templateGet':
                return new TemplateGet($config);
            case 'templateList':
                return new TemplateList($config);
            case 'templateRemoveUser':
                return new TemplateRemoveUser($config);
            case 'templateUpdateFiles':
                return new TemplateUpdateFiles($config);
            case 'unclaimedDraftCreate':
                return new UnclaimedDraftCreate($config);
            case 'unclaimedDraftCreateEmbedded':
                return new UnclaimedDraftCreateEmbedded($config);
            case 'unclaimedDraftCreateEmbeddedWithTemplate':
                return new UnclaimedDraftCreateEmbeddedWithTemplate($config);
            case 'unclaimedDraftEditAndResend':
                return new UnclaimedDraftEditAndResend($config);
            default:
                throw new Exception("Invalid operationId: {$this->operationId}");
        }
    }
}

$requester = new Requester(
    getenv('AUTH_TYPE'),
    getenv('AUTH_KEY'),
    getenv('SERVER'),
    getenv('JSON_STRING'),
);

$requester->run();
