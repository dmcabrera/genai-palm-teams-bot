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

import os
from flask import Flask
from flask import request
from flask_cors import CORS

from genai_palm_bot import GenAIPaLMBot

# Main Flask app
app = Flask(__name__)
CORS(app)

# Create the bot
bot = GenAIPaLMBot()

# Chat endpoint
@app.route("/chat", methods=['POST'])
def chat():
    # Get the json request
    request_json = request.get_json("message", silent=True)
    print(request_json)

    # Get the input message
    message = request_json["message"]["text"]
    bot_answer = bot.chat(message)
    print(bot_answer)

    # Return the answer
    response = {
        "answer": bot_answer
    }

    return response

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))