import discord
import genshin
from time import sleep
import tokens


# TOKEN needs to be the Discord bot's token, channel_id is the Discord channel id you want the bot to talk in
TOKEN = tokens.genshin_token
channel_id = tokens.general_id
client = discord.Client()
gm = "Good Morning"
gn = "Good Night"

# TODO: Implement an argument parser, give the user more control over what voice line they want.


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channel = client.get_channel(channel_id)
    phrase = gm
    # Phrase needs to match the voice line you want to send from the Wiki. gm and gn correlate to Good Morning/Night
    # Or you can customise it to something else such as "Hello" or "After the Rain"
    while True:
        try:
            char, vl, image = genshin.get_random_voiceline_and_image(phrase)
            await client.user.edit(username=char)
            await client.user.edit(avatar=image)
            await channel.send(vl)
            break
        except:
            # Unclean sleep implementation, I just want the whole process to rerun if it fails before sending the msg
            # Need to change it to work with discords limit on changing name/picture X times every Y hours
            sleep(1)


def main():
    client.run(TOKEN)
    return 0


if __name__ == "__main__":
    main()
