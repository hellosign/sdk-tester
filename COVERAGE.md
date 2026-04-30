# API Endpoint Coverage

**31/73 endpoints covered (42%)**

## Account (3/4)

- [x] Create Account (`accountCreate`)
- [x] Get Account (`accountGet`)
- [ ] Update Account (`accountUpdate`)
- [x] Verify Account (`accountVerify`)

## Api App (5/5)

- [x] Create API App (`apiAppCreate`)
- [x] Delete API App (`apiAppDelete`)
- [x] Get API App (`apiAppGet`)
- [x] List API Apps (`apiAppList`)
- [x] Update API App (`apiAppUpdate`)

## Bulk Send Job (0/2)

- [ ] Get Bulk Send Job (`bulkSendJobGet`)
- [ ] List Bulk Send Jobs (`bulkSendJobList`)

## Embedded (1/2)

- [ ] Get Embedded Template Edit URL (`embeddedEditUrl`)
- [x] Get Embedded Sign URL (`embeddedSignUrl`)

## Fax (0/5)

- [ ] Delete Fax (`faxDelete`)
- [ ] Download Fax Files (`faxFiles`)
- [ ] Get Fax (`faxGet`)
- [ ] Lists Faxes (`faxList`)
- [ ] Send Fax (`faxSend`)

## Fax Line (0/7)

- [ ] Add Fax Line User (`faxLineAddUser`)
- [ ] Get Available Fax Line Area Codes (`faxLineAreaCodeGet`)
- [ ] Purchase Fax Line (`faxLineCreate`)
- [ ] Delete Fax Line (`faxLineDelete`)
- [ ] Get Fax Line (`faxLineGet`)
- [ ] List Fax Lines (`faxLineList`)
- [ ] Remove Fax Line Access (`faxLineRemoveUser`)

## OAuth (0/2)

- [ ] OAuth Token Generate (`oauthTokenGenerate`)
- [ ] OAuth Token Refresh (`oauthTokenRefresh`)

## Report (0/1)

- [ ] Create Report (`reportCreate`)

## Signature Request (8/20)

- [ ] Embedded Bulk Send with Template (`signatureRequestBulkCreateEmbeddedWithTemplate`)
- [ ] Bulk Send with Template (`signatureRequestBulkSendWithTemplate`)
- [ ] Cancel Incomplete Signature Request (`signatureRequestCancel`)
- [x] Create Embedded Signature Request (`signatureRequestCreateEmbedded`)
- [x] Create Embedded Signature Request with Template (`signatureRequestCreateEmbeddedWithTemplate`)
- [x] Edit Signature Request (`signatureRequestEdit`)
- [x] Edit Embedded Signature Request (`signatureRequestEditEmbedded`)
- [ ] Edit Embedded Signature Request with Template (`signatureRequestEditEmbeddedWithTemplate`)
- [ ] Edit Signature Request With Template (`signatureRequestEditWithTemplate`)
- [ ] Download Files (`signatureRequestFiles`)
- [ ] Download Files as Data Uri (`signatureRequestFilesAsDataUri`)
- [ ] Download Files as File Url (`signatureRequestFilesAsFileUrl`)
- [x] Get Signature Request (`signatureRequestGet`)
- [x] List Signature Requests (`signatureRequestList`)
- [ ] Release On-Hold Signature Request (`signatureRequestReleaseHold`)
- [ ] Send Request Reminder (`signatureRequestRemind`)
- [ ] Remove Signature Request Access (`signatureRequestRemove`)
- [x] Send Signature Request (`signatureRequestSend`)
- [x] Send with Template (`signatureRequestSendWithTemplate`)
- [ ] Update Signature Request (`signatureRequestUpdate`)

## Team (9/10)

- [x] Add User to Team (`teamAddMember`)
- [x] Create Team (`teamCreate`)
- [x] Delete Team (`teamDelete`)
- [x] Get Team (`teamGet`)
- [x] Get Team Info (`teamInfo`)
- [ ] List Team Invites (`teamInvites`)
- [x] List Team Members (`teamMembers`)
- [x] Remove User from Team (`teamRemoveMember`)
- [x] List Sub Teams (`teamSubTeams`)
- [x] Update Team (`teamUpdate`)

## Template (4/11)

- [ ] Add User to Template (`templateAddUser`)
- [x] Create Template (`templateCreate`)
- [ ] Create Embedded Template Draft (`templateCreateEmbeddedDraft`)
- [x] Delete Template (`templateDelete`)
- [ ] Get Template Files (`templateFiles`)
- [ ] Get Template Files as Data Uri (`templateFilesAsDataUri`)
- [ ] Get Template Files as File Url (`templateFilesAsFileUrl`)
- [x] Get Template (`templateGet`)
- [x] List Templates (`templateList`)
- [ ] Remove User from Template (`templateRemoveUser`)
- [ ] Update Template Files (`templateUpdateFiles`)

## Unclaimed Draft (1/4)

- [ ] Create Unclaimed Draft (`unclaimedDraftCreate`)
- [x] Create Embedded Unclaimed Draft (`unclaimedDraftCreateEmbedded`)
- [ ] Create Embedded Unclaimed Draft with Template (`unclaimedDraftCreateEmbeddedWithTemplate`)
- [ ] Edit and Resend Unclaimed Draft (`unclaimedDraftEditAndResend`)
