# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import os
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Crun base url
CRUN_GENAI_SERVICE_URL = os.environ['CRUN_GENAI_SERVICE_URL']

class GenAIPaLMBot(object):

    # Constructor
    def __init__(self):
        # Set the target audience based on the crun service url
        target_audience = CRUN_GENAI_SERVICE_URL

        # Create an authorized session with the crun service
        sa_file_name = os.environ["CRUN_GENAI_SERVICE_SA"]
        creds = service_account.IDTokenCredentials.from_service_account_file(
            sa_file_name, target_audience=target_audience)
        self.authed_session = AuthorizedSession(creds)

    # Chat
    def chat(self, message):

        # Create the json request
        print("Human: " + message)
        request = {
            "message" : {"text" : message}
        }

        # Invoke the crun service
        base_url = CRUN_GENAI_SERVICE_URL
        url = base_url + '/chat'
        response =  self.authed_session.post(url=url, json=request)
        response_json = json.loads(response.text)

        # Return the answer        
        if response.status_code == 200:
            
            answer = response_json["answer"].encode('utf-32', errors='backslashreplace').decode('utf-32', errors='ignore')
            print("Bot: " + answer)
            return answer
        
        # Return the error
        else:
            return "Ha ocurrido un error al invocar el bot de GenAI.\n" +\
                "Status code: " + str(response.status_code)