import fs from 'fs';
import * as DropboxSign from '@dropbox/sign';

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

type ApiResponseT = Promise<DropboxSign.returnTypeT<any>>
    | Promise<DropboxSign.returnTypeI>;

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
                body: response.response.data,
                status_code: response.response.status,
                headers: response.response.headers,
            }, null, 4));

            process.exit(0);
        }).catch(e => {
            if (e instanceof DropboxSign.HttpError) {
                console.log(JSON.stringify({
                    body: e.response.data,
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

    private getFile(name: string): DropboxSign.RequestFile | undefined
    {
        if (this.files.hasOwnProperty(name)) {
            return fs.createReadStream(
                `${this.FILE_UPLOADS_DIR}/${this.files[name]}`
            );
        }

        return undefined;
    }

    private getFiles(name: string): DropboxSign.RequestFile[] | undefined
    {
        if (this.files.hasOwnProperty(name)) {
            let files: DropboxSign.RequestFile[] = [];

            for (let file of this.files[name]) {
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
        const api = this.getApi(new DropboxSign.AccountApi());

        if (this.operationId === 'accountCreate') {
            const obj = DropboxSign.AccountCreateRequest.init(this.data);

            return api.accountCreate(
                obj,
            );
        }

        if (this.operationId === 'accountGet') {
            return api.accountGet(
                this.parameters['account_id'] ?? null,
                this.parameters['email_address'] ?? null
            );
        }

        if (this.operationId === 'accountUpdate') {
            const obj = DropboxSign.AccountUpdateRequest.init(this.data);

            return api.accountUpdate(
                obj,
            );
        }

        if (this.operationId === 'accountVerify') {
            const obj = DropboxSign.AccountVerifyRequest.init(this.data);

            return api.accountVerify(
                obj,
            );
        }

        return null;
    }

    private apiAppApi(): ApiResponseT | null
    {
        const api = this.getApi(new DropboxSign.ApiAppApi());

        if (this.operationId === 'apiAppCreate') {
            const obj = DropboxSign.ApiAppCreateRequest.init(this.data);
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
            const obj = DropboxSign.ApiAppUpdateRequest.init(this.data);
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
        const api = this.getApi(new DropboxSign.BulkSendJobApi());

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
        const api = this.getApi(new DropboxSign.EmbeddedApi());

        if (this.operationId === 'embeddedEditUrl') {
            const obj = DropboxSign.EmbeddedEditUrlRequest.init(this.data);

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
        const api = this.getApi(new DropboxSign.OAuthApi());

        if (this.operationId === 'oauthTokenGenerate') {
            const obj = DropboxSign.OAuthTokenGenerateRequest.init(this.data);

            return api.oauthTokenGenerate(
                obj,
            );
        }

        if (this.operationId === 'oauthTokenRefresh') {
            const obj = DropboxSign.OAuthTokenRefreshRequest.init(this.data);

            return api.oauthTokenRefresh(
                obj,
            );
        }

        return null;
    }

    private reportApi(): ApiResponseT | null
    {
        const api = this.getApi(new DropboxSign.ReportApi());

        if (this.operationId === 'reportCreate') {
            const obj = DropboxSign.ReportCreateRequest.init(this.data);

            return api.reportCreate(
                obj,
            );
        }

        return null;
    }

    private signatureRequestApi(): ApiResponseT | null
    {
        const api = this.getApi(new DropboxSign.SignatureRequestApi());

        if (this.operationId === 'signatureRequestBulkCreateEmbeddedWithTemplate') {
            const obj = DropboxSign.SignatureRequestBulkCreateEmbeddedWithTemplateRequest.init(this.data);
            obj.signerFile = this.getFile('signer_file');

            return api.signatureRequestBulkCreateEmbeddedWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestBulkSendWithTemplate') {
            const obj = DropboxSign.SignatureRequestBulkSendWithTemplateRequest.init(this.data);
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
            const obj = DropboxSign.SignatureRequestCreateEmbeddedRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.signatureRequestCreateEmbedded(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestCreateEmbeddedWithTemplate') {
            const obj = DropboxSign.SignatureRequestCreateEmbeddedWithTemplateRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.signatureRequestCreateEmbeddedWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestFilesAsFileUrl') {
            return api.signatureRequestFilesAsFileUrl(
                this.parameters['signature_request_id']
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
            const obj = DropboxSign.SignatureRequestRemindRequest.init(this.data);

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
            const obj = DropboxSign.SignatureRequestSendRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.signatureRequestSend(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestSendWithTemplate') {
            const obj = DropboxSign.SignatureRequestSendWithTemplateRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.signatureRequestSendWithTemplate(
                obj,
            );
        }

        if (this.operationId === 'signatureRequestUpdate') {
            const obj = DropboxSign.SignatureRequestUpdateRequest.init(this.data);

            return api.signatureRequestUpdate(
                this.parameters['signature_request_id'],
                obj,
            );
        }

        return null;
    }

    private teamApi(): ApiResponseT | null
    {
        const api = this.getApi(new DropboxSign.TeamApi());

        if (this.operationId === 'teamAddMember') {
            const obj = DropboxSign.TeamAddMemberRequest.init(this.data);

            return api.teamAddMember(
                obj,
                this.parameters['team_id'] ?? null,
            );
        }

        if (this.operationId === 'teamCreate') {
            const obj = DropboxSign.TeamCreateRequest.init(this.data);

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
            const obj = DropboxSign.TeamRemoveMemberRequest.init(this.data);

            return api.teamRemoveMember(
                obj,
            );
        }

        if (this.operationId === 'teamUpdate') {
            const obj = DropboxSign.TeamUpdateRequest.init(this.data);

            return api.teamUpdate(
                obj,
            );
        }

        return null;
    }

    private templateApi(): ApiResponseT | null
    {
        const api = this.getApi(new DropboxSign.TemplateApi());

        if (this.operationId === 'templateAddUser') {
            const obj = DropboxSign.TemplateAddUserRequest.init(this.data);

            return api.templateAddUser(
                this.parameters['template_id'],
                obj,
            );
        }

        if (this.operationId === 'templateCreateEmbeddedDraft') {
            const obj = DropboxSign.TemplateCreateEmbeddedDraftRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.templateCreateEmbeddedDraft(
                obj,
            );
        }

        if (this.operationId === 'templateDelete') {
            return api.templateDelete(
                this.parameters['template_id'],
            );
        }

        if (this.operationId === 'templateFilesAsFileUrl') {
            return api.templateFilesAsFileUrl(
                this.parameters['template_id']
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
            const obj = DropboxSign.TemplateRemoveUserRequest.init(this.data);

            return api.templateRemoveUser(
                this.parameters['template_id'],
                obj,
            );
        }

        if (this.operationId === 'templateUpdateFiles') {
            const obj = DropboxSign.TemplateUpdateFilesRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.templateUpdateFiles(
                this.parameters['template_id'],
                obj,
            );
        }

        return null;
    }

    private unclaimedDraftApi(): ApiResponseT | null
    {
        const api = this.getApi(new DropboxSign.UnclaimedDraftApi());

        if (this.operationId === 'unclaimedDraftCreate') {
            const obj = DropboxSign.UnclaimedDraftCreateRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.unclaimedDraftCreate(
                obj,
            );
        }

        if (this.operationId === 'unclaimedDraftCreateEmbedded') {
            const obj = DropboxSign.UnclaimedDraftCreateEmbeddedRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.unclaimedDraftCreateEmbedded(
                obj,
            );
        }

        if (this.operationId === 'unclaimedDraftCreateEmbeddedWithTemplate') {
            const obj = DropboxSign.UnclaimedDraftCreateEmbeddedWithTemplateRequest.init(this.data);
            obj.files = this.getFiles('files');

            return api.unclaimedDraftCreateEmbedded(
                obj,
            );
        }

        if (this.operationId === 'unclaimedDraftEditAndResend') {
            const obj = DropboxSign.UnclaimedDraftEditAndResendRequest.init(this.data);

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
