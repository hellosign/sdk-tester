from string import Template, ascii_lowercase, digits


# HS environments
prod_hs_env_str = 'prod'
staging_hs_env_str = 'staging'
qa_hs_env_str = 'qa'
dev_hs_env_str = 'dev'

client_id = '4443b51c0b42b95db849ce0256821c6f'
staging_hs_internal_guid= 'mQO5ZnhhKmTlBo4ycgCPpRLeUYp13jXT4GHaKgDv'
qa_hs_internal_guid='DrrAe6cOP7A9anqCMU8YOxjzUokh9oHkeWJ5XvYw'
hsapi_get_api_key_url = Template(
    'https://app.$env.com/internalapp.php/account/apiKey?hs_internal_guid=$guid&email_address=$email_address')