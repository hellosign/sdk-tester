require 'base64'
require 'json'
require 'hello_sign'

class Requester
  LOCAL_FILE = __dir__ + '/../data.json'

  FILE_UPLOADS_DIR = __dir__ + '/../file_uploads'

  attr_accessor :auth_type

  attr_accessor :auth_key

  attr_accessor :data

  attr_accessor :dev_mode

  attr_accessor :files

  attr_accessor :header_params

  attr_accessor :operation_id

  attr_accessor :parameters

  attr_accessor :server

  def initialize(
    auth_type = '',
    auth_key = '',
    server = '',
    json_source = nil,
    dev_mode = nil
  )
    self.auth_type = auth_type.downcase
    self.auth_key = auth_key
    self.server = server
    self.dev_mode = dev_mode

    self.read_json_data(json_source)
  end

  def run
    begin
      body, status_code, headers = call_from_operation_id

      response = {
        body: body.to_body,
        status_code: status_code,
        headers: get_response_headers(headers),
      }

      puts JSON.pretty_generate(response)
    rescue HelloSign::ApiError => e
      response = {
        body: e.response_body.to_body,
        status_code: e.code,
        headers: get_response_headers(e.response_headers),
      }

      puts JSON.pretty_generate(response)
    end
  end

  private

  def get_client
    config = HelloSign::Configuration.new
    config.host = self.server

    if self.auth_type === 'apikey'
      config.username = self.auth_key
    elsif self.auth_type === 'oauth'
      config.access_token = self.auth_key
    else
      raise 'Invalid auth type. Must be "apikey" or "oauth".'
    end

    self.header_params = {}

    if self.dev_mode
      self.header_params = {"Cookie" => 'XDEBUG_SESSION=xdebug'}
    end

    HelloSign::ApiClient.new(config)
  end

  def read_json_data(base64_json)
    if base64_json.is_a?(String) && !base64_json.to_s.strip.empty?
      begin
        json = JSON.parse(Base64.decode64(base64_json), :symbolize_names => true)
      rescue StandardError
        raise 'Invalid base64 JSON data provided.'
      end
    elsif File.exist? LOCAL_FILE
      begin
        json = JSON.parse(File.read(LOCAL_FILE), :symbolize_names => true)
      rescue StandardError
        raise 'Invalid JSON file provided.'
      end
    else
      raise 'No valid JSON data provided.'
    end

    self.operation_id = json[:operationId]
    self.data = json[:data] || {}
    self.files = json[:files] || {}
    self.parameters = json[:parameters] || {}
  end

  def call_from_operation_id
    response = self.account_api
    if response
      return response
    end

    response = self.api_app_api
    if response
      return response
    end

    response = self.bulk_send_job_api
    if response
      return response
    end

    response = self.embedded_api
    if response
      return response
    end

    response = self.oauth_api
    if response
      return response
    end

    response = self.report_api
    if response
      return response
    end

    response = self.signature_request_api
    if response
      return response
    end

    response = self.team_api
    if response
      return response
    end

    response = self.template_api
    if response
      return response
    end

    response = self.unclaimed_draft_api
    if response
      return response
    end

    raise 'Invalid operation_id ' + self.operation_id
  end

  def get_response_headers(headers)
    formatted = {}

    headers.each do |k, v|
      formatted[k.downcase] = v
    end

    formatted
  end

  def get_file(name)
    if name.is_a?(String) && self.files.key?(name)
      File.open(FILE_UPLOADS_DIR + '/' + self.files[name], 'r')
    end
  end

  def get_files(name)
    if name.is_a?(String) && self.files.key?(name) && self.files[name].length > 0
      files = []

      self.files[name].each do |file|
        files.append(File.open(FILE_UPLOADS_DIR + '/' + file), 'w')
      end

      files
    end
  end

  def account_api
    api_client = self.get_client
    api = HelloSign::AccountApi.new(api_client)

    if self.operation_id === 'accountCreate'
      obj = api_client.convert_to_type(
        self.data,
        HelloSign::AccountCreateRequest.to_s
      ) || HelloSign::AccountCreateRequest.new

      return api.account_create_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'accountGet'
      return api.account_get_with_http_info(
        {
          header_params: self.header_params,
          account_id: self.parameters['account_id'] || nil,
        }
      )
    end

    if self.operation_id === 'accountUpdate'
      obj = api_client.convert_to_type(
        self.data,
        HelloSign::AccountUpdateRequest.to_s
      ) || HelloSign::AccountUpdateRequest.new

      return api.account_update_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'accountVerify'
      obj = api_client.convert_to_type(
        self.data,
        HelloSign::AccountVerifyRequest.to_s
      ) || HelloSign::AccountVerifyRequest.new

      return api.account_verify_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def api_app_api
    api_client = self.get_client
    api = HelloSign::ApiAppApi.new(api_client)

    if self.operation_id === 'apiAppCreate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::ApiAppCreateRequest.to_s
      ) || HelloSign::ApiAppCreateRequest.new

      obj.custom_logo_file = self.get_file('custom_logo_file')

      return api.api_app_create_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'apiAppDelete'
      return api.api_app_delete_with_http_info(
        self.parameters['client_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'apiAppGet'
      return api.api_app_get_with_http_info(
        self.parameters['client_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'apiAppList'
      return api.api_app_list_with_http_info(
        {
          header_params: self.header_params,
          page: self.parameters['page'] || 1,
          page_size: self.parameters['page_size'] || 20,
        }
      )
    end

    if self.operation_id === 'apiAppUpdate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::ApiAppUpdateRequest.to_s
      ) || HelloSign::ApiAppUpdateRequest.new

      obj.custom_logo_file = self.get_file('custom_logo_file')

      return api.api_app_update_with_http_info(
        self.parameters['client_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def bulk_send_job_api
    api_client = self.get_client
    api = HelloSign::BulkSendJobApi.new(api_client)

    if self.operation_id === 'bulkSendJobGet'
      return api.bulk_send_job_get_with_http_info(
        self.parameters['bulk_send_job_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'bulkSendJobList'
      return api.bulk_send_job_list_with_http_info(
        {
          header_params: self.header_params,
          page: self.parameters['page'] || 1,
          page_size: self.parameters['page_size'] || 20,
        }
      )
    end
  end

  def embedded_api
    api_client = self.get_client
    api = HelloSign::EmbeddedApi.new(api_client)

    if self.operation_id === 'embeddedEditUrl'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::EmbeddedEditUrlRequest.to_s
      ) || HelloSign::EmbeddedEditUrlRequest.new

      return api.embedded_edit_url_with_http_info(
        self.parameters['template_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'embeddedSignUrl'
      return api.embedded_sign_url_with_http_info(
        self.parameters['signature_id'],
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def oauth_api
    api_client = self.get_client
    api = HelloSign::OAuthApi.new(api_client)

    if self.operation_id === 'oauthTokenGenerate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::OAuthTokenGenerateRequest.to_s
      ) || HelloSign::OAuthTokenGenerateRequest.new

      return api.oauth_token_generate_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'oauthTokenRefresh'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::OAuthTokenRefreshRequest.to_s
      ) || HelloSign::OAuthTokenRefreshRequest.new

      return api.oauth_token_refresh_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def report_api
    api_client = self.get_client
    api = HelloSign::ReportApi.new(api_client)

    if self.operation_id === 'reportCreate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::ReportCreateRequest.to_s
      ) || HelloSign::ReportCreateRequest.new

      return api.report_create_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def signature_request_api
    api_client = self.get_client
    api = HelloSign::SignatureRequestApi.new(api_client)

    if self.operation_id === 'signatureRequestBulkCreateEmbeddedWithTemplate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestBulkCreateEmbeddedWithTemplateRequest.to_s
      ) || HelloSign::SignatureRequestBulkCreateEmbeddedWithTemplateRequest.new

      obj.signer_file = self.get_file('signer_file')

      return api.signature_request_bulk_create_embedded_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestBulkSendWithTemplate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestBulkSendWithTemplateRequest.to_s
      ) || HelloSign::SignatureRequestBulkSendWithTemplateRequest.new

      obj.signer_file = self.get_file('signer_file')

      return api.signature_request_bulk_send_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestCancel'
      return api.signature_request_cancel_with_http_info(
        self.parameters['signature_request_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestCreateEmbedded'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestCreateEmbeddedRequest.to_s
      ) || HelloSign::SignatureRequestCreateEmbeddedRequest.new

      obj.file = self.get_files('file')

      return api.signature_request_create_embedded_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestCreateEmbeddedWithTemplate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestCreateEmbeddedWithTemplateRequest.to_s
      ) || HelloSign::SignatureRequestCreateEmbeddedWithTemplateRequest.new

      obj.file = self.get_files('file')

      return api.signature_request_create_embedded_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestFiles'
      return api.signature_request_files_with_http_info(
        self.parameters['signature_request_id'],
        {
          header_params: self.header_params,
          file_type: self.parameters['file_type'] || 'pdf',
          get_url: self.parameters['get_url'] || false,
          get_data_uri: self.parameters['get_data_uri'] || false,
        }
      )
    end

    if self.operation_id === 'signatureRequestGet'
      return api.signature_request_get_with_http_info(
        self.parameters['signature_request_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestList'
      return api.signature_request_list_with_http_info(
        {
          header_params: self.header_params,
          account_id: self.parameters['account_id'] || nil,
          page: self.parameters['page'] || 1,
          page_size: self.parameters['page_size'] || 20,
          query: self.parameters['query'] || nil,
        }
      )
    end

    if self.operation_id === 'signatureRequestReleaseHold'
      return api.signature_request_release_hold_with_http_info(
        self.parameters['signature_request_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestRemind'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestRemindRequest.to_s
      ) || HelloSign::SignatureRequestRemindRequest.new

      return api.signature_request_remind_with_http_info(
        self.parameters['signature_request_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestRemove'
      return api.signature_request_remove_with_http_info(
        self.parameters['signature_request_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestSend'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestSendRequest.to_s
      ) || HelloSign::SignatureRequestSendRequest.new

      obj.file = self.get_files('file')

      return api.signature_request_send_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestSendWithTemplate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestSendWithTemplateRequest.to_s
      ) || HelloSign::SignatureRequestSendWithTemplateRequest.new

      obj.file = self.get_files('file')

      return api.signature_request_send_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestUpdate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::SignatureRequestUpdateRequest.to_s
      ) || HelloSign::SignatureRequestUpdateRequest.new

      return api.signature_request_update_with_http_info(
        self.parameters['signature_request_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def team_api
    api_client = self.get_client
    api = HelloSign::TeamApi.new(api_client)

    if self.operation_id === 'teamAddMember'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TeamAddMemberRequest.to_s
      ) || HelloSign::TeamAddMemberRequest.new

      return api.team_add_member_with_http_info(
        obj,
        {
          header_params: self.header_params,
          team_id: self.parameters['team_id'],
        }
      )
    end

    if self.operation_id === 'teamCreate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TeamCreateRequest.to_s
      ) || HelloSign::TeamCreateRequest.new

      return api.team_create_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'teamDelete'
      return api.team_delete_with_http_info(
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'teamGet'
      return api.team_get_with_http_info(
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'teamRemoveMember'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TeamRemoveMemberRequest.to_s
      ) || HelloSign::TeamRemoveMemberRequest.new

      return api.team_remove_member_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'teamUpdate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TeamUpdateRequest.to_s
      ) || HelloSign::TeamUpdateRequest.new

      return api.team_update_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def template_api
    api_client = self.get_client
    api = HelloSign::TemplateApi.new(api_client)

    if self.operation_id === 'templateAddUser'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TemplateAddUserRequest.to_s
      ) || HelloSign::TemplateAddUserRequest.new

      return api.template_add_user_with_http_info(
        self.parameters['template_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateCreateEmbeddedDraft'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TemplateCreateEmbeddedDraftRequest.to_s
      ) || HelloSign::TemplateCreateEmbeddedDraftRequest.new

      obj.file = self.get_files('file')

      return api.template_create_embedded_draft_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateDelete'
      return api.template_delete_with_http_info(
        self.parameters['template_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateFiles'
      return api.template_files_with_http_info(
        self.parameters['template_id'],
        {
          header_params: self.header_params,
          file_type: self.parameters['file_type'] || nil,
          get_url: self.parameters['get_url'] || false,
          get_data_uri: self.parameters['get_data_uri'] || false,
        }
      )
    end

    if self.operation_id === 'templateGet'
      return api.template_get_with_http_info(
        self.parameters['template_id'],
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateList'
      return api.template_list_with_http_info(
        {
          header_params: self.header_params,
          account_id: self.parameters['account_id'] || nil,
          page: self.parameters['page'] || 1,
          page_size: self.parameters['page_size'] || 20,
          query: self.parameters['query'] || nil,
        }
      )
    end

    if self.operation_id === 'templateRemoveUser'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TemplateRemoveUserRequest.to_s
      ) || HelloSign::TemplateRemoveUserRequest.new

      return api.template_remove_user_with_http_info(
        self.parameters['template_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateUpdateFiles'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::TemplateUpdateFilesRequest.to_s
      ) || HelloSign::TemplateUpdateFilesRequest.new

      obj.file = self.get_files('file')

      return api.template_update_files_with_http_info(
        self.parameters['template_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def unclaimed_draft_api
    api_client = self.get_client
    api = HelloSign::UnclaimedDraftApi.new(api_client)

    if self.operation_id === 'unclaimedDraftCreate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::UnclaimedDraftCreateRequest.to_s
      ) || HelloSign::UnclaimedDraftCreateRequest.new

      obj.file = self.get_files('file')

      return api.unclaimed_draft_create_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'unclaimedDraftCreateEmbedded'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::UnclaimedDraftCreateEmbeddedRequest.to_s
      ) || HelloSign::UnclaimedDraftCreateEmbeddedRequest.new

      obj.file = self.get_files('file')

      return api.unclaimed_draft_create_embedded_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'unclaimedDraftCreateEmbeddedWithTemplate'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::UnclaimedDraftCreateEmbeddedWithTemplateRequest.to_s
      ) || HelloSign::UnclaimedDraftCreateEmbeddedWithTemplateRequest.new

      obj.file = self.get_files('file')

      return api.unclaimed_draft_create_embedded_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'unclaimedDraftEditAndResend'
      obj = api_client.convert_to_type(
        self.data.transform_keys(&:to_sym),
        HelloSign::UnclaimedDraftEditAndResendRequest.to_s
      ) || HelloSign::UnclaimedDraftEditAndResendRequest.new

      obj.file = self.get_files('file')

      return api.unclaimed_draft_edit_and_resend_with_http_info(
        self.parameters['signature_request_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end
end

requester = Requester.new(
  ENV['AUTH_TYPE'] || '',
  ENV['AUTH_KEY'] || '',
  ENV['SERVER'] || '',
  ENV['JSON_STRING'],
  ENV['DEV_MODE'],
)

requester.run
