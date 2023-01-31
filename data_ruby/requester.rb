require 'base64'
require 'json'
require 'dropbox-sign'

class Requester
  FILE_UPLOADS_DIR = __dir__ + '/../file_uploads'

  attr_accessor :auth_type

  attr_accessor :auth_key

  attr_accessor :data

  attr_accessor :dev_mode

  attr_accessor :files

  attr_accessor :header_params

  attr_accessor :operation_id

  attr_accessor :parameters

  attr_accessor :api_server

  def initialize(
    auth_type = '',
    auth_key = '',
    api_server = '',
    json_data = '',
    dev_mode = nil
  )
    self.auth_type = auth_type.downcase
    self.auth_key = auth_key
    self.api_server = api_server
    self.dev_mode = self.to_boolean(dev_mode)

    self.read_json_data(json_data)
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
    rescue Dropbox::Sign::ApiError => e
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
    config = Dropbox::Sign::Configuration.new
    config.host = self.api_server

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

    Dropbox::Sign::ApiClient.new(config)
  end

  def read_json_data(base64_json)
    if base64_json.is_a?(String) && !base64_json.to_s.strip.empty?
      begin
        json = JSON.parse(Base64.decode64(base64_json), :symbolize_names => true)
      rescue StandardError
        raise 'Invalid base64 JSON data provided.'
      end
    else
      raise 'No valid JSON data provided.'
    end

    self.operation_id = json[:operationId]
    self.data = json[:data] || {}
    self.files = JSON.parse(json[:files].to_json, :symbolize_names => false) || {}
    self.parameters = JSON.parse(json[:parameters].to_json, :symbolize_names => false) || {}
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
      File.new(FILE_UPLOADS_DIR + '/' + self.files[name], 'r')
    end
  end

  def get_files(name)
    if name.is_a?(String) && self.files.key?(name) && self.files[name].length > 0
      files = []

      self.files[name].each do |file|
        files.append(File.new(FILE_UPLOADS_DIR + '/' + file, 'r'))
      end

      files
    end
  end

  def account_api
    api_client = self.get_client
    api = Dropbox::Sign::AccountApi.new(api_client)

    if self.operation_id === 'accountCreate'
      obj = Dropbox::Sign::AccountCreateRequest.init(self.data)

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
          email_address: self.parameters['email_address'] || nil,
        }
      )
    end

    if self.operation_id === 'accountUpdate'
      obj = Dropbox::Sign::AccountUpdateRequest.init(self.data)

      return api.account_update_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'accountVerify'
      obj = Dropbox::Sign::AccountVerifyRequest.init(self.data)

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
    api = Dropbox::Sign::ApiAppApi.new(api_client)

    if self.operation_id === 'apiAppCreate'
      obj = Dropbox::Sign::ApiAppCreateRequest.init(self.data)
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
      obj = Dropbox::Sign::ApiAppUpdateRequest.init(self.data)
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
    api = Dropbox::Sign::BulkSendJobApi.new(api_client)

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
    api = Dropbox::Sign::EmbeddedApi.new(api_client)

    if self.operation_id === 'embeddedEditUrl'
      obj = Dropbox::Sign::EmbeddedEditUrlRequest.init(self.data)

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
    api = Dropbox::Sign::OAuthApi.new(api_client)

    if self.operation_id === 'oauthTokenGenerate'
      obj = Dropbox::Sign::OAuthTokenGenerateRequest.init(self.data)

      return api.oauth_token_generate_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'oauthTokenRefresh'
      obj = Dropbox::Sign::OAuthTokenRefreshRequest.init(self.data)

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
    api = Dropbox::Sign::ReportApi.new(api_client)

    if self.operation_id === 'reportCreate'
      obj = Dropbox::Sign::ReportCreateRequest.init(self.data)

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
    api = Dropbox::Sign::SignatureRequestApi.new(api_client)

    if self.operation_id === 'signatureRequestBulkCreateEmbeddedWithTemplate'
      obj = Dropbox::Sign::SignatureRequestBulkCreateEmbeddedWithTemplateRequest.init(self.data)

      obj.signer_file = self.get_file('signer_file')

      return api.signature_request_bulk_create_embedded_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestBulkSendWithTemplate'
      obj = Dropbox::Sign::SignatureRequestBulkSendWithTemplateRequest.init(self.data)

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
      obj = Dropbox::Sign::SignatureRequestCreateEmbeddedRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.signature_request_create_embedded_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestCreateEmbeddedWithTemplate'
      obj = Dropbox::Sign::SignatureRequestCreateEmbeddedWithTemplateRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.signature_request_create_embedded_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestFilesAsFileUrl'
      return api.signature_request_files_as_file_url_with_http_info(
        self.parameters['signature_request_id'],
        {
          header_params: self.header_params
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
      obj = Dropbox::Sign::SignatureRequestRemindRequest.init(self.data)

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
      obj = Dropbox::Sign::SignatureRequestSendRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.signature_request_send_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestSendWithTemplate'
      obj = Dropbox::Sign::SignatureRequestSendWithTemplateRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.signature_request_send_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'signatureRequestUpdate'
      obj = Dropbox::Sign::SignatureRequestUpdateRequest.init(self.data)

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
    api = Dropbox::Sign::TeamApi.new(api_client)

    if self.operation_id === 'teamAddMember'
      obj = Dropbox::Sign::TeamAddMemberRequest.init(self.data)

      return api.team_add_member_with_http_info(
        obj,
        {
          header_params: self.header_params,
          team_id: self.parameters['team_id'],
        }
      )
    end

    if self.operation_id === 'teamCreate'
      obj = Dropbox::Sign::TeamCreateRequest.init(self.data)

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
      obj = Dropbox::Sign::TeamRemoveMemberRequest.init(self.data)

      return api.team_remove_member_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'teamUpdate'
      obj = Dropbox::Sign::TeamUpdateRequest.init(self.data)

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
    api = Dropbox::Sign::TemplateApi.new(api_client)

    if self.operation_id === 'templateAddUser'
      obj = Dropbox::Sign::TemplateAddUserRequest.init(self.data)

      return api.template_add_user_with_http_info(
        self.parameters['template_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateCreateEmbeddedDraft'
      obj = Dropbox::Sign::TemplateCreateEmbeddedDraftRequest.init(self.data)
      obj.files = self.get_files('files')

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

    if self.operation_id === 'templateFilesAsFileUrl'
      return api.template_files_as_file_url_with_http_info(
        self.parameters['template_id'],
        {
          header_params: self.header_params
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
      obj = Dropbox::Sign::TemplateRemoveUserRequest.init(self.data)

      return api.template_remove_user_with_http_info(
        self.parameters['template_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'templateUpdateFiles'
      obj = Dropbox::Sign::TemplateUpdateFilesRequest.init(self.data)
      obj.files = self.get_files('files')

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
    api = Dropbox::Sign::UnclaimedDraftApi.new(api_client)

    if self.operation_id === 'unclaimedDraftCreate'
      obj = Dropbox::Sign::UnclaimedDraftCreateRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.unclaimed_draft_create_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'unclaimedDraftCreateEmbedded'
      obj = Dropbox::Sign::UnclaimedDraftCreateEmbeddedRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.unclaimed_draft_create_embedded_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'unclaimedDraftCreateEmbeddedWithTemplate'
      obj = Dropbox::Sign::UnclaimedDraftCreateEmbeddedWithTemplateRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.unclaimed_draft_create_embedded_with_template_with_http_info(
        obj,
        {
          header_params: self.header_params,
        }
      )
    end

    if self.operation_id === 'unclaimedDraftEditAndResend'
      obj = Dropbox::Sign::UnclaimedDraftEditAndResendRequest.init(self.data)
      obj.files = self.get_files('files')

      return api.unclaimed_draft_edit_and_resend_with_http_info(
        self.parameters['signature_request_id'],
        obj,
        {
          header_params: self.header_params,
        }
      )
    end
  end

  def to_boolean(s)
    (s == true || s == 'true' || s == 1)
  end
end

requester = Requester.new(
  ENV['AUTH_TYPE'] || '',
  ENV['AUTH_KEY'] || '',
  ENV['API_SERVER'] || '',
  ENV['JSON_DATA'] || '',
  ENV['DEV_MODE'] || false,
)

requester.run
