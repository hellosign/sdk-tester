import ApiTester

def test_signature_request_send():
    json_data= {
  "operationId": "signatureRequestSend",
  "parameters": {},
  "data": {
    "cc_email_addresses": [
      "lawyer@hellosign.com",
      "lawyer@example.com"
    ],
    "message": "Please sign this NDA and then we can discuss more. Let me know if you\nhave any questions.",
    "signers": [
      {
        "email_address": "s1@example.com",
        "name": "Signer 1",
        "order": 0,
        "sms_phone_number": "+14155550100",
        "sms_phone_number_type": "delivery"
      }
    ],
    "subject": "The NDA we talked about",
    "test_mode": True,
    "title": "NDA with Acme Co."
  },
  "files": {
    "file": [
      "pdf-sample.pdf",
      "pdf-sample-2.pdf"
    ]
  }
}