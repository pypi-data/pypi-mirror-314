# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides the auth middleware.
"""

IAM_AUTH = "IAMAuthorization"
IDAAS_AUTH = "IDaaSAuthorization"
IAM_SESSION = "IAMSession"
IDAAS_SESSION = "IDaaSSession"

ORG_ID = "OrgID"
USER_ID = "UserID"
USER_NAME = "UserName"
USER_ROLE = "UserRole"
PROJECT_ID = "ProjectID"

IAM_SESSION_ID = "bce-sessionid"
IAM_DEFAULT_PROJECT_ID = "iam"

IDAAS_SESSION_ID = "idaas-sessionid"
IDAAS_PROJECT_NAME = "idaas-project-name"

AUTH_MODE = "AuthMode"


ERROR_CODE_UNAUTHORIZED = "Unauthorized"
ERROR_CODE_SIGNATURE_DOES_NOT_MATCH = "SignatureDoesNotMatch"

ERROR_MESSAGE_SIGNATURE_NOT_FOUND = "The request signature is missing."
ERROR_MESSAGE_SIGNATURE_DOES_NOT_MATCH = (
    "The request signature we calculated does not match the signature you provided. "
    "Check your Secret Access Key and signing method. Consult the service documentation for details."
)
