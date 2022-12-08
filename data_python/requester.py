import base64
import json
import os
from metadict import MetaDict

from hellosign_sdk import ApiClient, Configuration, ApiException, apis, models


class Requester(object):
    FILE_UPLOADS_DIR = './../file_uploads'

    def __init__(
            self,
            auth_type: str,
            auth_key: str,
            api_server: str,
            json_data: str = None,
            dev_mode: str = None
    ):
        self._auth_type = auth_type
        self._auth_key = auth_key
        self._api_server = api_server
        self._dev_mode = bool(dev_mode)

        self._operation_id = ''
        self._data = {}
        self._files = {}
        self._parameters = {}

        self._read_json_data(json_data)
        self._api_client = ApiClient(self._get_config())

        if self._dev_mode:
            self._api_client.set_default_header('Cookie', 'XDEBUG_SESSION=xdebug')

    def run(self):
        try:
            response = self._call_from_operation_id()

            data = {
                'body': response[0].to_dict(),
                'status_code': response[1],
                'headers': self._get_response_headers(response[2]),
            }
        except ApiException as e:
            data = {
                'body': e.body.to_dict(),
                'status_code': e.status,
                'headers': self._get_response_headers(e.headers),
            }

        print(json.dumps(data, indent=4))

    def _get_config(self):
        if self._auth_type == 'apikey':
            config = Configuration(
                host=f'https://{self._api_server}/v3',
                username=self._auth_key,
            )
        elif self._auth_type == 'oauth':
            config = Configuration(
                host=f'https://{self._api_server}/v3',
                access_token=self._auth_key,
            )
        else:
            raise RuntimeError('Invalid auth type. Must be "apikey" or "oauth".')

        return config

    def _read_json_data(self, base64_json: str):
        if isinstance(base64_json, str) and len(base64_json):
            json_data = json.loads(base64.b64decode(base64_json))

            if not json_data:
                raise RuntimeError('Invalid base64 JSON data provided.')
        else:
            raise RuntimeError

        if 'operationId' in json_data:
            self._operation_id = json_data['operationId']
        if 'data' in json_data:
            self._data = json_data['data']
        if 'files' in json_data:
            self._files = json_data['files']
        if 'parameters' in json_data:
            self._parameters = json_data['parameters']

    def _call_from_operation_id(self):
        response = self._account_api()
        if response:
            return response

        response = self._api_app_api()
        if response:
            return response

        response = self._bulk_send_job_api()
        if response:
            return response

        response = self._embedded_api()
        if response:
            return response

        response = self._oauth_api()
        if response:
            return response

        response = self._report_api()
        if response:
            return response

        response = self._signature_request_api()
        if response:
            return response

        response = self._team_api()
        if response:
            return response

        response = self._template_api()
        if response:
            return response

        response = self._unclaimed_draft_api()
        if response:
            return response

        raise RuntimeError(f'Invalid operationId: {self._operation_id}')

    @staticmethod
    def _get_response_headers(headers: dict):
        formatted = {}

        for key, value in headers.items():
            formatted[key.lower()] = value

        return formatted

    def _serialize(self, response_type):
        return self._api_client.deserialize(
            response=MetaDict({'data': json.dumps(self._data)}),
            response_type=[response_type],
            _check_type=True,
        )

    def _get_file(self, name: str):
        if name in self._files and len(self._files[name]):
            f = open(f'{self.FILE_UPLOADS_DIR}/{self._files[name]}', 'rb')
            return f

    def _get_files(self, name: str):
        files = []

        if name in self._files and len(self._files[name]):
            for file in self._files[name]:
                f = open(f'{self.FILE_UPLOADS_DIR}/{file}', 'rb')
                files.append(f)

        return files

    def _account_api(self):
        api = apis.AccountApi(self._api_client)

        if self._operation_id == 'accountCreate':
            obj = self._serialize(models.AccountCreateRequest)

            return api.account_create(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'accountGet':
            return api.account_get(
                account_id=self._parameters.get('account_id', None),
                email_address=self._parameters.get('email_address', None),
                _return_http_data_only=False
            )

        if self._operation_id == 'accountUpdate':
            obj = self._serialize(models.AccountUpdateRequest)

            return api.account_update(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'accountVerify':
            obj = self._serialize(models.AccountVerifyRequest)

            return api.account_verify(
                obj,
                _return_http_data_only=False
            )

    def _api_app_api(self):
        api = apis.ApiAppApi(self._api_client)

        if self._operation_id == 'apiAppCreate':
            obj = self._serialize(models.ApiAppCreateRequest)

            obj['custom_logo_file'] = self._get_file('custom_logo_file')

            return api.api_app_create(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'apiAppDelete':
            return api.api_app_delete(
                self._parameters.get('client_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'apiAppGet':
            return api.api_app_get(
                self._parameters.get('client_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'apiAppList':
            return api.api_app_list(
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
                _return_http_data_only=False
            )

        if self._operation_id == 'apiAppUpdate':
            obj = self._serialize(models.ApiAppUpdateRequest)

            obj['custom_logo_file'] = self._get_file('custom_logo_file')

            return api.api_app_update(
                self._parameters.get('client_id'),
                obj,
            )

    def _bulk_send_job_api(self):
        api = apis.BulkSendJobApi(self._api_client)

        if self._operation_id == 'bulkSendJobGet':
            return api.bulk_send_job_get(
                self._parameters.get('bulk_send_job_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'bulkSendJobList':
            return api.bulk_send_job_list(
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
                _return_http_data_only=False
            )

    def _embedded_api(self):
        api = apis.EmbeddedApi(self._api_client)

        if self._operation_id == 'embeddedEditUrl':
            obj = self._serialize(models.EmbeddedEditUrlRequest)

            return api.embedded_edit_url(
                self._parameters.get('template_id'),
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'embeddedSignUrl':
            return api.embedded_sign_url(
                self._parameters.get('signature_id'),
                _return_http_data_only=False
            )

    def _oauth_api(self):
        api = apis.OAuthApi(self._api_client)

        if self._operation_id == 'oauthTokenGenerate':
            obj = self._serialize(models.OAuthTokenGenerateRequest)

            return api.oauth_token_generate(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'oauthTokenRefresh':
            obj = self._serialize(models.OAuthTokenRefreshRequest)

            return api.oauth_token_refresh(
                obj,
                _return_http_data_only=False
            )

    def _report_api(self):
        api = apis.ReportApi(self._api_client)

        if self._operation_id == 'reportCreate':
            obj = self._serialize(models.ReportCreateRequest)

            return api.report_create(
                obj,
                _return_http_data_only=False
            )

    def _signature_request_api(self):
        api = apis.SignatureRequestApi(self._api_client)

        if self._operation_id == 'signatureRequestBulkCreateEmbeddedWithTemplate':
            obj = self._serialize(models.SignatureRequestBulkCreateEmbeddedWithTemplateRequest)

            obj['signer_file'] = self._get_file('signer_file')

            return api.signature_request_bulk_create_embedded_with_template(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestBulkSendWithTemplate':
            obj = self._serialize(models.SignatureRequestBulkSendWithTemplateRequest)

            obj['signer_file'] = self._get_file('signer_file')

            return api.signature_request_bulk_send_with_template(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestCancel':
            return api.signature_request_cancel(
                self._parameters.get('signature_request_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestCreateEmbedded':
            obj = self._serialize(models.SignatureRequestCreateEmbeddedRequest)

            obj['file'] = self._get_files('file')

            return api.signature_request_create_embedded(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestCreateEmbeddedWithTemplate':
            obj = self._serialize(models.SignatureRequestCreateEmbeddedWithTemplateRequest)

            obj['file'] = self._get_files('file')

            return api.signature_request_create_embedded_with_template(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestFilesAsFileUrl':
            return api.signature_request_files_as_file_url(
                self._parameters.get('signature_request_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestGet':
            return api.signature_request_get(
                self._parameters.get('signature_request_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestList':
            return api.signature_request_list(
                account_id=self._parameters.get('account_id', None),
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
                query=self._parameters.get('query', None),
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestReleaseHold':
            return api.signature_request_release_hold(
                self._parameters.get('signature_request_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestRemind':
            obj = self._serialize(models.SignatureRequestRemindRequest)

            return api.signature_request_remind(
                self._parameters.get('signature_request_id'),
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestRemove':
            return api.signature_request_remove(
                self._parameters.get('signature_request_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestSend':
            obj = self._serialize(models.SignatureRequestSendRequest)

            obj['file'] = self._get_files('file')

            return api.signature_request_send(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestSendWithTemplate':
            obj = self._serialize(models.SignatureRequestSendWithTemplateRequest)

            obj['file'] = self._get_files('file')

            return api.signature_request_send_with_template(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'signatureRequestUpdate':
            obj = self._serialize(models.SignatureRequestUpdateRequest)

            return api.signature_request_update(
                self._parameters.get('signature_request_id'),
                obj,
                _return_http_data_only=False
            )

    def _team_api(self):
        api = apis.TeamApi(self._api_client)

        if self._operation_id == 'teamAddMember':
            obj = self._serialize(models.TeamAddMemberRequest)

            return api.team_add_member(
                obj,
                team_id=self._parameters.get('team_id', None),
                _return_http_data_only=False
            )

        if self._operation_id == 'teamCreate':
            obj = self._serialize(models.TeamCreateRequest)

            return api.team_create(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'teamDelete':
            return api.team_delete(
                _return_http_data_only=False
            )

        if self._operation_id == 'teamGet':
            return api.team_get(
                _return_http_data_only=False
            )

        if self._operation_id == 'teamRemoveMember':
            obj = self._serialize(models.TeamRemoveMemberRequest)

            return api.team_update(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'teamUpdate':
            obj = self._serialize(models.TeamUpdateRequest)

            return api.team_update(
                obj,
                _return_http_data_only=False
            )

    def _template_api(self):
        api = apis.TemplateApi(self._api_client)

        if self._operation_id == 'templateAddUser':
            obj = self._serialize(models.TemplateAddUserRequest)

            return api.template_add_user(
                self._parameters.get('template_id', None),
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'templateCreateEmbeddedDraft':
            obj = self._serialize(models.TemplateCreateEmbeddedDraftRequest)

            obj['file'] = self._get_files('file')

            return api.template_create_embedded_draft(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'templateDelete':
            return api.template_delete(
                self._parameters.get('template_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'templateFilesAsFileUrl':
            return api.template_files_as_file_url(
                self._parameters.get('template_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'templateGet':
            return api.template_get(
                self._parameters.get('template_id'),
                _return_http_data_only=False
            )

        if self._operation_id == 'templateList':
            return api.template_list(
                account_id=self._parameters.get('account_id', None),
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
                query=self._parameters.get('query', None),
                _return_http_data_only=False
            )

        if self._operation_id == 'templateRemoveUser':
            obj = self._serialize(models.TemplateRemoveUserRequest)

            return api.template_remove_user(
                self._parameters.get('template_id'),
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'templateUpdateFiles':
            obj = self._serialize(models.TemplateUpdateFilesRequest)

            obj['file'] = self._get_files('file')

            return api.template_update_files(
                self._parameters.get('template_id'),
                obj,
                _return_http_data_only=False
            )

    def _unclaimed_draft_api(self):
        api = apis.UnclaimedDraftApi(self._api_client)

        if self._operation_id == 'unclaimedDraftCreate':
            obj = self._serialize(models.UnclaimedDraftCreateRequest)

            obj['file'] = self._get_files('file')

            return api.unclaimed_draft_create(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'unclaimedDraftCreateEmbedded':
            obj = self._serialize(models.UnclaimedDraftCreateEmbeddedRequest)

            obj['file'] = self._get_files('file')

            return api.unclaimed_draft_create_embedded(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'unclaimedDraftCreateEmbeddedWithTemplate':
            obj = self._serialize(models.UnclaimedDraftCreateEmbeddedWithTemplateRequest)

            obj['file'] = self._get_files('file')

            return api.unclaimed_draft_create_embedded_with_template(
                obj,
                _return_http_data_only=False
            )

        if self._operation_id == 'unclaimedDraftEditAndResend':
            obj = self._serialize(models.UnclaimedDraftEditAndResendRequest)

            return api.unclaimed_draft_edit_and_resend(
                self._parameters.get('signature_request_id'),
                obj,
                _return_http_data_only=False
            )


if __name__ == '__main__':
    requester = Requester(
        os.getenv('AUTH_TYPE'),
        os.getenv('AUTH_KEY'),
        os.getenv('API_SERVER'),
        os.getenv('JSON_DATA'),
        os.getenv('DEV_MODE'),
    )
    requester.run()
