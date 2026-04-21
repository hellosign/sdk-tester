import base64
import json
import os

from dropbox_sign import ApiClient, Configuration, ApiException, apis, models as m


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
                'body': response.data.to_dict() if response.data is not None else None,
                'status_code': response.status_code,
                'headers': self._get_response_headers(response.headers or {}),
            }
        except ApiException as e:
            data = {
                'body': self._exception_body(e),
                'status_code': e.status,
                'headers': self._get_response_headers(e.headers or {}),
            }

        print(json.dumps(data, indent=4))

    @staticmethod
    def _exception_body(exc: ApiException):
        if getattr(exc, 'data', None) is not None and hasattr(exc.data, 'to_dict'):
            return exc.data.to_dict()
        body = getattr(exc, 'body', None)
        if isinstance(body, (bytes, bytearray)):
            try:
                body = body.decode('utf-8')
            except UnicodeDecodeError:
                return None
        if isinstance(body, str) and body:
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {'raw': body}
        return None

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
    def _get_response_headers(headers):
        formatted = {}

        if not headers:
            return formatted

        items = headers.items() if hasattr(headers, 'items') else headers
        for key, value in items:
            formatted[key.lower()] = value

        return formatted

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
            obj = m.AccountCreateRequest.init(self._data)

            return api.account_create_with_http_info(obj)

        if self._operation_id == 'accountGet':
            return api.account_get_with_http_info(
                account_id=self._parameters.get('account_id', None),
                email_address=self._parameters.get('email_address', None),
            )

        if self._operation_id == 'accountUpdate':
            obj = m.AccountUpdateRequest.init(self._data)

            return api.account_update_with_http_info(obj)

        if self._operation_id == 'accountVerify':
            obj = m.AccountVerifyRequest.init(self._data)

            return api.account_verify_with_http_info(obj)

    def _api_app_api(self):
        api = apis.ApiAppApi(self._api_client)

        if self._operation_id == 'apiAppCreate':
            obj = m.ApiAppCreateRequest.init(self._data)
            obj.custom_logo_file = self._get_file('custom_logo_file')

            return api.api_app_create_with_http_info(obj)

        if self._operation_id == 'apiAppDelete':
            return api.api_app_delete_with_http_info(
                self._parameters.get('client_id'),
            )

        if self._operation_id == 'apiAppGet':
            return api.api_app_get_with_http_info(
                self._parameters.get('client_id'),
            )

        if self._operation_id == 'apiAppList':
            return api.api_app_list_with_http_info(
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
            )

        if self._operation_id == 'apiAppUpdate':
            obj = m.ApiAppUpdateRequest.init(self._data)
            obj.custom_logo_file = self._get_file('custom_logo_file')

            return api.api_app_update_with_http_info(
                self._parameters.get('client_id'),
                obj,
            )

    def _bulk_send_job_api(self):
        api = apis.BulkSendJobApi(self._api_client)

        if self._operation_id == 'bulkSendJobGet':
            return api.bulk_send_job_get_with_http_info(
                self._parameters.get('bulk_send_job_id'),
            )

        if self._operation_id == 'bulkSendJobList':
            return api.bulk_send_job_list_with_http_info(
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
            )

    def _embedded_api(self):
        api = apis.EmbeddedApi(self._api_client)

        if self._operation_id == 'embeddedEditUrl':
            obj = m.EmbeddedEditUrlRequest.init(self._data)

            return api.embedded_edit_url_with_http_info(
                self._parameters.get('template_id'),
                obj,
            )

        if self._operation_id == 'embeddedSignUrl':
            return api.embedded_sign_url_with_http_info(
                self._parameters.get('signature_id'),
            )

    def _oauth_api(self):
        api = apis.OAuthApi(self._api_client)

        if self._operation_id == 'oauthTokenGenerate':
            obj = m.OAuthTokenGenerateRequest.init(self._data)

            return api.oauth_token_generate_with_http_info(obj)

        if self._operation_id == 'oauthTokenRefresh':
            obj = m.OAuthTokenRefreshRequest.init(self._data)

            return api.oauth_token_refresh_with_http_info(obj)

    def _report_api(self):
        api = apis.ReportApi(self._api_client)

        if self._operation_id == 'reportCreate':
            obj = m.ReportCreateRequest.init(self._data)

            return api.report_create_with_http_info(obj)

    def _signature_request_api(self):
        api = apis.SignatureRequestApi(self._api_client)

        if self._operation_id == 'signatureRequestBulkCreateEmbeddedWithTemplate':
            obj = m.SignatureRequestBulkCreateEmbeddedWithTemplateRequest.init(self._data)
            obj.signer_file = self._get_file('signer_file')

            return api.signature_request_bulk_create_embedded_with_template_with_http_info(obj)

        if self._operation_id == 'signatureRequestBulkSendWithTemplate':
            obj = m.SignatureRequestBulkSendWithTemplateRequest.init(self._data)
            obj.signer_file = self._get_file('signer_file')

            return api.signature_request_bulk_send_with_template_with_http_info(obj)

        if self._operation_id == 'signatureRequestCancel':
            return api.signature_request_cancel_with_http_info(
                self._parameters.get('signature_request_id'),
            )

        if self._operation_id == 'signatureRequestCreateEmbedded':
            obj = m.SignatureRequestCreateEmbeddedRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.signature_request_create_embedded_with_http_info(obj)

        if self._operation_id == 'signatureRequestCreateEmbeddedWithTemplate':
            obj = m.SignatureRequestCreateEmbeddedWithTemplateRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.signature_request_create_embedded_with_template_with_http_info(obj)

        if self._operation_id == 'signatureRequestFilesAsFileUrl':
            return api.signature_request_files_as_file_url_with_http_info(
                self._parameters.get('signature_request_id'),
            )

        if self._operation_id == 'signatureRequestGet':
            return api.signature_request_get_with_http_info(
                self._parameters.get('signature_request_id'),
            )

        if self._operation_id == 'signatureRequestList':
            return api.signature_request_list_with_http_info(
                account_id=self._parameters.get('account_id', None),
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
                query=self._parameters.get('query', None),
            )

        if self._operation_id == 'signatureRequestReleaseHold':
            return api.signature_request_release_hold_with_http_info(
                self._parameters.get('signature_request_id'),
            )

        if self._operation_id == 'signatureRequestRemind':
            obj = m.SignatureRequestRemindRequest.init(self._data)

            return api.signature_request_remind_with_http_info(
                self._parameters.get('signature_request_id'),
                obj,
            )

        if self._operation_id == 'signatureRequestRemove':
            return api.signature_request_remove_with_http_info(
                self._parameters.get('signature_request_id'),
            )

        if self._operation_id == 'signatureRequestSend':
            obj = m.SignatureRequestSendRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.signature_request_send_with_http_info(obj)

        if self._operation_id == 'signatureRequestSendWithTemplate':
            obj = m.SignatureRequestSendWithTemplateRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.signature_request_send_with_template_with_http_info(obj)

        if self._operation_id == 'signatureRequestUpdate':
            obj = m.SignatureRequestUpdateRequest.init(self._data)

            return api.signature_request_update_with_http_info(
                self._parameters.get('signature_request_id'),
                obj,
            )

    def _team_api(self):
        api = apis.TeamApi(self._api_client)

        if self._operation_id == 'teamAddMember':
            obj = m.TeamAddMemberRequest.init(self._data)

            return api.team_add_member_with_http_info(
                obj,
                team_id=self._parameters.get('team_id', None),
            )

        if self._operation_id == 'teamCreate':
            obj = m.TeamCreateRequest.init(self._data)

            return api.team_create_with_http_info(obj)

        if self._operation_id == 'teamDelete':
            return api.team_delete_with_http_info()

        if self._operation_id == 'teamGet':
            return api.team_get_with_http_info()

        if self._operation_id == 'teamRemoveMember':
            obj = m.TeamRemoveMemberRequest.init(self._data)

            return api.team_update_with_http_info(obj)

        if self._operation_id == 'teamUpdate':
            obj = m.TeamUpdateRequest.init(self._data)

            return api.team_update_with_http_info(obj)

    def _template_api(self):
        api = apis.TemplateApi(self._api_client)

        if self._operation_id == 'templateAddUser':
            obj = m.TemplateAddUserRequest.init(self._data)

            return api.template_add_user_with_http_info(
                self._parameters.get('template_id', None),
                obj,
            )

        if self._operation_id == 'templateCreateEmbeddedDraft':
            obj = m.TemplateCreateEmbeddedDraftRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.template_create_embedded_draft_with_http_info(obj)

        if self._operation_id == 'templateDelete':
            return api.template_delete_with_http_info(
                self._parameters.get('template_id'),
            )

        if self._operation_id == 'templateFilesAsFileUrl':
            return api.template_files_as_file_url_with_http_info(
                self._parameters.get('template_id'),
            )

        if self._operation_id == 'templateGet':
            return api.template_get_with_http_info(
                self._parameters.get('template_id'),
            )

        if self._operation_id == 'templateList':
            return api.template_list_with_http_info(
                account_id=self._parameters.get('account_id', None),
                page=self._parameters.get('page', 1),
                page_size=self._parameters.get('page_size', 20),
                query=self._parameters.get('query', None),
            )

        if self._operation_id == 'templateRemoveUser':
            obj = m.TemplateRemoveUserRequest.init(self._data)

            return api.template_remove_user_with_http_info(
                self._parameters.get('template_id'),
                obj,
            )

        if self._operation_id == 'templateUpdateFiles':
            obj = m.TemplateUpdateFilesRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.template_update_files_with_http_info(
                self._parameters.get('template_id'),
                obj,
            )

    def _unclaimed_draft_api(self):
        api = apis.UnclaimedDraftApi(self._api_client)

        if self._operation_id == 'unclaimedDraftCreate':
            obj = m.UnclaimedDraftCreateRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.unclaimed_draft_create_with_http_info(obj)

        if self._operation_id == 'unclaimedDraftCreateEmbedded':
            obj = m.UnclaimedDraftCreateEmbeddedRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.unclaimed_draft_create_embedded_with_http_info(obj)

        if self._operation_id == 'unclaimedDraftCreateEmbeddedWithTemplate':
            obj = m.UnclaimedDraftCreateEmbeddedWithTemplateRequest.init(self._data)
            obj.files = self._get_files('files')

            return api.unclaimed_draft_create_embedded_with_template_with_http_info(obj)

        if self._operation_id == 'unclaimedDraftEditAndResend':
            obj = m.UnclaimedDraftEditAndResendRequest.init(self._data)

            return api.unclaimed_draft_edit_and_resend_with_http_info(
                self._parameters.get('signature_request_id'),
                obj,
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
