# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

from genai_palm_bot import GenAIPaLMBot

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    # Constructor    
    def __init__(self):
        self.bot = GenAIPaLMBot()

    # On message
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(self.bot.chat(turn_context.activity.text))

    # On members addedd
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hola, bienvenido!")
