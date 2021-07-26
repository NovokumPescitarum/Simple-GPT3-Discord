import discord
import openai

TOKEN = '<Discord-Bot-Token>'
client = discord.Client()
openai.api_key = 'Openai-API-Key'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.author != client.user:
        async with message.channel.typing():
            msg = message.content
            ## GPT-J API Prompt
            mySummary = """
            The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
            
            Human: Hello, who are you?
            AI: I am an AI created by OpenAI. How can I help you today?
            Human: """

            ##Open the memory
            a_file = open("AIknowledge", "r")
            lines = a_file.readlines()
            last_lines = lines[-10:]
            context = str(mySummary) + str("\n") + str(''.join(last_lines)) + str(msg) + str("\n") + str("AI:")
            a_file.close()
            #Run GPT-3
            response = openai.Completion.create(
                engine="davinci",
                temperature=0.9,
                max_tokens=100,
                top_p=1,
                prompt = context,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n"]
            )
            # Print out results for further processing
            desired = response.choices[0].text
            memory = open('AIknowledge', mode='a', newline="")
            memory.write(str(msg) + str("\nAI:") + str(desired) + str("Human: "))
            memory.close()
            await message.channel.send(desired)


client.run(TOKEN)
