import fs from 'fs';
import * as HelloSignSDK from 'hellosign-sdk';

interface JsonDataI {
    operationId: string,
    parameters: { [key: string]: string },
    data: { [key: string]: any },
    files: { [key: string]: string },
}

interface ApiI {
    basePath: string | (() => string),
    username: string | (() => string),
    accessToken: string | (() => string),
    defaultHeaders: { [key: string]: string } | (() => { [key: string]: string }),
}

type ApiResponseT = Promise<HelloSignSDK.returnTypeT<any>>
    | Promise<HelloSignSDK.returnTypeI>;

class Requester
{
    private FILE_UPLOADS_DIR = './../file_uploads';

    private readonly apiServer: string;

    private readonly authType: string;

    private readonly authKey: string;

    private data: { [key: string]: any } = {};

    private readonly devMode: boolean;

    private files: { [key: string]: any } = {};

    private operationId: string = '';

    private parameters: { [key: string]: any } = {};

    public constructor(
        authType: string,
        authKey: string,
        apiServer: string,
        jsonData: string,
        devMode: string | null = null,
    ) {
        this.authType = authType;
        this.authKey = authKey;
        this.apiServer = apiServer;
        this.devMode = Boolean(devMode).valueOf();

        this.readJsonData(jsonData);
    }

    public run()
    {
        const result = this.callFromOperationId();

        // @ts-ignore
        result.then(response => {
            console.log(JSON.stringify({
                body: HelloSignSDK.ObjectSerializer.serialize(
                    response.body,
                    response.body.constructor.name,
                ),
                status_code: response.response.status,
                headers: response.response.headers,
            }, null, 4));

            process.exit(0);
        }).catch(e => {
            if (e instanceof HelloSignSDK.HttpError) {
                console.log(JSON.stringify({
                    body: HelloSignSDK.ObjectSerializer.serialize(
                        e.body,
                        e.body.constructor.name,
                    ),
                    status_code: e.statusCode,
                    headers: e.response.headers,
                }, null, 4));

                process.exit(0);
            }

            throw e;
        });
    }

    private getApi<T extends ApiI>(api: T): T
    {
        api.basePath = `https://${this.apiServer}/v3`

        if (this.authType === 'apikey') {
            api.username = this.authKey;
        } else if (this.authType === 'oauth') {
            api.accessToken = this.authKey;
        } else {
            throw new Error(
                'Invalid auth type. Must be "apikey" or "oauth".'
            );
        }

        if (this.devMode) {
            api.defaultHeaders = {
                Cookie: 'XDEBUG_SESSION=xdebug',
            }
        }

        return api;
    }

    private readJsonData(base64Json: string): void
    {
        let json: JsonDataI;

        if (base64Json) {
            try {
                json = JSON.parse(
                    Buffer.from(base64Json, 'base64').toString()
                );
            } catch (e) {
                throw new Error('Invalid base64 JSON data provided.');
            }
        } else {
            throw Error('A JSON file or base64 JSON string must be provided.');
        }

        this.operationId = json.operationId;
        this.data = json.data;
        this.files = json.files;
        this.parameters = json.parameters;
    }

    private callFromOperationId(): ApiResponseT
    {
        let response;

        response = this.accountApi();
        if (response) {
            return response;
        }

        response = this.apiAppApi();
        if (response) {
            return response;
        }

        response = this.bulkSendJobApi();
        if (response) {
            return response;
        }

        response = this.embeddedApi();
        if (response) {
            return response;
        }

        response = this.oauthApi();
        if (response) {
            return response;
        }

        response = this.reportApi();
        if (response) {
            return response;
        }

        response = this.signatureRequestApi();
        if (response) {
            return response;
        }

        response = this.teamApi();
        if (response) {
            return response;
        }

        response = this.templateApi();
        if (response) {
            return response;
        }

        response = this.unclaimedDraftApi();
        if (response) {
            return response;
        }

        throw new Error(`Invalid operationId: ${this.operationId}`)
    }

    private getFile(name: string): HelloSignSDK.RequestFile | undefined
    {
        if (this.parameters.hasOwnProperty(name)) {
            return fs.createReadStream(
                `${this.FILE_UPLOADS_DIR}/${this.parameters[name]}`
            );
        }

        return undefined;
    }

    private getFiles(name: string): HelloSignSDK.RequestFile[] | undefined
    {
        if (this.parameters.hasOwnProperty(name)) {
            let files: HelloSignSDK.RequestFile[] = [];

            for (let file of this.parameters[name]) {
                files.push(fs.createReadStream(
                    `${this.FILE_UPLOADS_DIR}/${file}`
                ));
            }

            return files;
        }

        return undefined;
    }

    private accountApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.AccountApi());

        if (this.operationId === 'accountCreate') {
            let obj: HelloSignSDK.AccountCreateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'AccountCreateRequest',
            );

            return api.accountCreate(
                obj,
            );
        }

        if (this.operationId === 'accountGet') {
            return api.accountGet(
                this.parameters['account_id'] ?? null
            );
        }

        if (this.operationId === 'accountUpdate') {
            let obj: HelloSignSDK.AccountUpdateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'AccountUpdateRequest',
            );

            return api.accountUpdate(
                obj,
            );
        }

        if (this.operationId === 'accountVerify') {
            let obj: HelloSignSDK.AccountVerifyRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'AccountVerifyRequest',
            );

            return api.accountVerify(
                obj,
            );
        }

        return null;
    }

    private apiAppApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.ApiAppApi());

        if (this.operationId === 'apiAppCreate') {
            let obj: HelloSignSDK.ApiAppCreateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'ApiAppCreateRequest',
            );

            obj.customLogoFile = this.getFile('custom_logo_file');

            return api.apiAppCreate(
                obj,
            );
        }

        if (this.operationId === 'apiAppDelete') {
            return api.apiAppDelete(
                this.parameters['client_id'],
            );
        }

        if (this.operationId === 'apiAppGet') {
            return api.apiAppGet(
                this.parameters['client_id'],
            );
        }

        if (this.operationId === 'apiAppList') {
            return api.apiAppList(
                this.parameters['page'] ?? 1,
                this.parameters['page_size'] ?? 20,
            );
        }

        if (this.operationId === 'apiAppUpdate') {
            let obj: HelloSignSDK.ApiAppUpdateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'ApiAppUpdateRequest',
            );

            obj.customLogoFile = this.getFile('custom_logo_file');

            return api.apiAppUpdate(
                this.parameters['client_id'],
                obj,
            );
        }

        return null;
    }

    private bulkSendJobApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.BulkSendJobApi());

        if (this.operationId === 'bulkSendJobGet') {
            return api.bulkSendJobGet(
                this.parameters['bulk_send_job_id'],
            );
        }

        if (this.operationId === 'bulkSendJobList') {
            return api.bulkSendJobGet(
                this.parameters['page'] ?? 1,
                this.parameters['page_size'] ?? 20,
            );
        }

        return null;
    }

    private embeddedApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.EmbeddedApi());

        if (this.operationId === 'embeddedEditUrl') {
            let obj: HelloSignSDK.EmbeddedEditUrlRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'EmbeddedEditUrlRequest',
            );

            return api.embeddedEditUrl(
                this.parameters['template_id'],
                obj,
            );
        }

        if (this.operationId === 'embeddedSignUrl') {
            return api.embeddedSignUrl(
                this.parameters['signature_id'],
            );
        }

        return null;
    }

    private oauthApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.OAuthApi());

        if (this.operationId === 'oauthTokenGenerate') {
            let obj: HelloSignSDK.OAuthTokenGenerateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'OAuthTokenGenerateRequest',
            );

            return api.oauthTokenGenerate(
                obj,
            );
        }

        if (this.operationId === 'oauthTokenRefresh') {
            let obj: HelloSignSDK.OAuthTokenRefreshRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'OAuthTokenRefreshRequest',
            );

            return api.oauthTokenRefresh(
                obj,
            );
        }

        return null;
    }

    private reportApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.ReportApi());

        if (this.operationId === 'reportCreate') {
            let obj: HelloSignSDK.ReportCreateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'ReportCreateRequest',
            );

            return api.reportCreate(
                obj,
            );
        }

        return null;
    }

    private signatureRequestApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.SignatureRequestApi());

        if (this.operationId === 'signatureRequestBulkCreateEmbeddedWithTemplate') {
            let obj: HelloSignSDK.SignatureRequestBulkCreateEmbeddedWithTemplateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestBulkCreateEmbeddedWithTemplateRequest',
            );

            obj.signerFile = this.getFile('signer_file');

            return api.signatureRequestBulkCreateEmbeddedWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestBulkSendWithTemplate') {
            let obj: HelloSignSDK.SignatureRequestBulkSendWithTemplateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestBulkSendWithTemplateRequest',
            );

            obj.signerFile = this.getFile('signer_file');

            return api.signatureRequestBulkSendWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestCancel') {
            return api.signatureRequestCancel(
                this.parameters['signature_request_id'],
            );
        }

        if (this.operationId === 'signatureRequestCreateEmbedded') {
            let obj: HelloSignSDK.SignatureRequestCreateEmbeddedRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestCreateEmbeddedRequest',
            );

            obj.file = this.getFiles('file');

            return api.signatureRequestCreateEmbedded(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestCreateEmbeddedWithTemplate') {
            let obj: HelloSignSDK.SignatureRequestCreateEmbeddedWithTemplateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestCreateEmbeddedWithTemplateRequest',
            );

            obj.file = this.getFiles('file');

            return api.signatureRequestCreateEmbeddedWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestFiles') {
            return api.signatureRequestFiles(
                this.parameters['signature_request_id'],
                this.parameters['file_type'] ?? 'pdf',
                this.parameters['get_url'] ?? false,
                this.parameters['get_data_uri'] ?? false,
            );
        }

        if (this.operationId === 'signatureRequestGet') {
            return api.signatureRequestGet(
                this.parameters['signature_request_id'],
            );
        }

        if (this.operationId === 'signatureRequestList') {
            return api.signatureRequestList(
                this.parameters['account_id'] ?? null,
                this.parameters['page'] ?? 1,
                this.parameters['page_size'] ?? 20,
                this.parameters['query'] ?? null,
            );
        }

        if (this.operationId === 'signatureRequestReleaseHold') {
            return api.signatureRequestReleaseHold(
                this.parameters['signature_request_id'],
            );
        }

        if (this.operationId === 'signatureRequestRemind') {
            let obj: HelloSignSDK.SignatureRequestRemindRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestRemindRequest',
            );

            return api.signatureRequestRemind(
                this.parameters['signature_request_id'],
                obj,
            );
        }

        if (this.operationId === 'signatureRequestRemove') {
            return api.signatureRequestRemove(
                this.parameters['signature_request_id'],
            );
        }

        if (this.operationId === 'signatureRequestSend') {
            let obj: HelloSignSDK.SignatureRequestSendRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestSendRequest',
            );

            obj.file = this.getFiles('file');

            return api.signatureRequestSend(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestSendWithTemplate') {
            let obj: HelloSignSDK.SignatureRequestSendWithTemplateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestSendWithTemplateRequest',
            );

            obj.file = this.getFiles('file');

            return api.signatureRequestSendWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestUpdate') {
            let obj: HelloSignSDK.SignatureRequestUpdateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'SignatureRequestUpdateRequest',
            );

            return api.signatureRequestUpdate(
                this.parameters['signature_request_id'],
                obj,
            );
        }

        return null;
    }

    private teamApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.TeamApi());

        if (this.operationId === 'teamAddMember') {
            let obj: HelloSignSDK.TeamAddMemberRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TeamAddMemberRequest',
            );

            return api.teamAddMember(
                obj,
                this.parameters['team_id'] ?? null,
            );
        }

        if (this.operationId === 'teamCreate') {
            let obj: HelloSignSDK.TeamCreateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TeamCreateRequest',
            );

            return api.teamCreate(
                obj,
            );
        }

        if (this.operationId === 'teamDelete') {
            return api.teamDelete();
        }

        if (this.operationId === 'teamGet') {
            return api.teamGet();
        }

        if (this.operationId === 'teamRemoveMember') {
            let obj: HelloSignSDK.TeamRemoveMemberRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TeamRemoveMemberRequest',
            );

            return api.teamRemoveMember(
                obj,
            );
        }

        if (this.operationId === 'teamUpdate') {
            let obj: HelloSignSDK.TeamUpdateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TeamUpdateRequest',
            );

            return api.teamUpdate(
                obj,
            );
        }

        return null;
    }

    private templateApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.TemplateApi());

        if (this.operationId === 'templateAddUser') {
            let obj: HelloSignSDK.TemplateAddUserRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TemplateAddUserRequest',
            );

            return api.templateAddUser(
                this.parameters['template_id'],
                obj,
            );
        }

        if (this.operationId === 'templateCreateEmbeddedDraft') {
            let obj: HelloSignSDK.TemplateCreateEmbeddedDraftRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TemplateCreateEmbeddedDraftRequest',
            );

            obj.file = this.getFiles('file');

            return api.templateCreateEmbeddedDraft(
                obj,
            );
        }

        if (this.operationId === 'templateDelete') {
            return api.templateDelete(
                this.parameters['template_id'],
            );
        }

        if (this.operationId === 'templateFiles') {
            return api.templateFiles(
                this.parameters['template_id'],
                this.parameters['file_type'] ?? null,
                this.parameters['get_url'] ?? false,
                this.parameters['get_data_uri'] ?? false,
            );
        }

        if (this.operationId === 'templateGet') {
            return api.templateGet(
                this.parameters['template_id'],
            );
        }

        if (this.operationId === 'templateList') {
            return api.templateList(
                this.parameters['account_id'] ?? null,
                this.parameters['page'] ?? 1,
                this.parameters['page_size'] ?? 20,
                this.parameters['query'] ?? null,
            );
        }

        if (this.operationId === 'templateRemoveUser') {
            let obj: HelloSignSDK.TemplateRemoveUserRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TemplateRemoveUserRequest',
            );

            return api.templateRemoveUser(
                this.parameters['template_id'],
                obj,
            );
        }

        if (this.operationId === 'templateUpdateFiles') {
            let obj: HelloSignSDK.TemplateUpdateFilesRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'TemplateUpdateFilesRequest',
            );

            obj.file = this.getFiles('file');

            return api.templateUpdateFiles(
                this.parameters['template_id'],
                obj,
            );
        }

        return null;
    }

    private unclaimedDraftApi(): ApiResponseT | null
    {
        const api = this.getApi(new HelloSignSDK.UnclaimedDraftApi());

        if (this.operationId === 'unclaimedDraftCreate') {
            let obj: HelloSignSDK.UnclaimedDraftCreateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'UnclaimedDraftCreateRequest',
            );

            obj.file = this.getFiles('file');

            return api.unclaimedDraftCreate(
                obj,
            );
        }

        if (this.operationId === 'unclaimedDraftCreateEmbedded') {
            let obj: HelloSignSDK.UnclaimedDraftCreateEmbeddedRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'UnclaimedDraftCreateEmbeddedRequest',
            );

            obj.file = this.getFiles('file');

            return api.unclaimedDraftCreateEmbedded(
                obj,
            );
        }

        if (this.operationId === 'unclaimedDraftCreateEmbeddedWithTemplate') {
            let obj: HelloSignSDK.UnclaimedDraftCreateEmbeddedWithTemplateRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'UnclaimedDraftCreateEmbeddedWithTemplateRequest',
            );

            obj.file = this.getFiles('file');

            return api.unclaimedDraftCreateEmbedded(
                obj,
            );
        }

        if (this.operationId === 'unclaimedDraftEditAndResend') {
            let obj: HelloSignSDK.UnclaimedDraftEditAndResendRequest;
            obj = HelloSignSDK.ObjectSerializer.deserialize(
                this.data,
                'UnclaimedDraftEditAndResendRequest',
            );

            return api.unclaimedDraftEditAndResend(
                this.parameters['signature_request_id'],
                obj,
            );
        }

        return null;
    }
}

const requester = new Requester(
    process.env.AUTH_TYPE as string,
    process.env.AUTH_KEY as string,
    process.env.API_SERVER as string,
    process.env.JSON_DATA as string,
    process.env.DEV_MODE,
);

requester.run();
