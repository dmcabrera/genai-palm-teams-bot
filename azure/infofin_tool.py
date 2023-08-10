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

# Imports
import os
from typing import List
import json

import vertexai
from google.cloud import discoveryengine

# Constantes de Search Engine
PROJECT_ID = os.environ['PROJECT_ID']
LOCATION = "us-central1"
SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']
SEARCH_ENGINE_LOCATION = "global"
SEARCH_ENGINE_CONFIG = "default_config"
MODEL_NAME = "text-bison@001"

# Inicializamos el cliente de VertexAI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Tool que realiza una busqueda en la bd
# semantica ocupando discovery_engine
class InfoFinTool(object):

    def __init__(self):
        # Discovery engine client
        self.discovery_engine = discoveryengine.SearchServiceClient()

        # The full resource name of the search engine serving config
        # e.g. projects/{project_id}/locations/{location}
        self.discovery_engine_config = self.discovery_engine.serving_config_path(
            project=PROJECT_ID,
            location=SEARCH_ENGINE_LOCATION,
            data_store=SEARCH_ENGINE_ID,
            serving_config=SEARCH_ENGINE_CONFIG,
        )

    # Search engine function
    def query_engine(self, question) -> List[discoveryengine.SearchResponse.SearchResult]:

        request = discoveryengine.SearchRequest(
            serving_config=self.discovery_engine_config,
            query=question,
            page_size=5,
            content_search_spec={
                "summary_spec": {
                    "summary_result_count": 3
                },
                "snippet_spec": {
                    "max_snippet_count": 0
                },
                "extractive_content_spec": {
                    "max_extractive_answer_count": 3,
                    "max_extractive_segment_count": 1
                }
            }
        )
        response = self.discovery_engine.search(request)

        return response.results

    # Search and parsing
    def query(self, question):

        # Busco en el Search Engine
        search_result = self.query_engine(question)

        for result in search_result:
            print(result)

        # Creo el cntexto y las fuentes de información
        context = "\n".join([json.dumps(
            result.document.derived_struct_data["extractive_segments"][0]["content"]) for result in search_result])
        sources = "\n".join([result.document.derived_struct_data["link"] + " - Página: " +
                             json.dumps(result.document.derived_struct_data["extractive_answers"][0]["pageNumber"]) for result in search_result])

        print("\n" + context)
        print("\n" + sources)

        return context, sources
