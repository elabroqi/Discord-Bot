import random
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import openai 

openai.api_key = "your-openai-api-key"

# Todo: load token from .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# Todo: Bot Setup
# intents: permissions the bot needs to see and respond to messages
intents: Intents = Intents.default() #intents of type intents
# no quality assuarnce
intents.message_content = True # NOQA #Allows bot to see messages
intents.members = True  # NOQA # Enables access to member events
intents.presences = True # NOQA  # Enables access to presence updates
client: Client = Client(intents=intents)


# Todo: message functionality
async def send_message(message: Message, user_message: str) -> None:  # returns nothing since this is only meant to execute code (similar to void)
    # first check if there is a user message, if no user message than intents was not handled properly
    if not user_message:
        print('(Message was empty because intents were not enabled ')
        return

    # messages the user back to their private inbox
    if is_private := user_message[0] == '?': # ? triggers private message functionality // assigning is_private is either going to be true or false
        user_message = user_message[1:] #splices the users message to not include the ?

    try:
        response: str = get_response(user_message)
        # send the message to author if is_private is true else send to current channel
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# handling when the bot goes online (to know the bot is running)
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    # to make sure the bot doesn't endlessly respond to itself
    if message.author == client.user:
        return

    username: str = str(message.author)  #getting the username
    channel: str = str(message.channel)  #getting the channel message was sent from
    user_message: str = message.content

    print(f'[{channel}] {username}: "{user_message}"')

    if "gerbot roulette" in message.content.lower():
        result = random.randint(1, 6)
        if result == 1:
            await message.channel.send(f"{message.author.mention} bit the bullet!")
        else:
            await message.channel.send(f"{message.author.mention} did not bite the bullet (your number: {result})")
        return

    if "bot" in message.content.lower():  # Only respond if "bot" is mentioned
        messages = [msg async for msg in message.channel.history(limit=5)]
        chat_context = ""
        for msg in reversed(messages):
            chat_context += f"{msg.author.display_name}: {msg.content}\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"The following is a casual conversation in a Discord chat:\n{chat_context}\nRespond briefly and naturally, like a member of this group:",
            max_tokens=50,
            temperature=0.7,
        )
        bot_response = response["choices"][0]["text"].strip()
        if bot_response:
            await message.channel.send(bot_response)


# main entry point to run our code
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()