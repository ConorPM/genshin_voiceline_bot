import pandas as pd
import random
import requests
import io
from io import BytesIO
from PIL import Image


def get_characters():
    dfs = pd.read_html("https://genshin-impact.fandom.com/wiki/Characters/List")
    df = dfs[0]
    genshin_characters = list()
    for i in df.Name:
        genshin_characters.append(i)
    return genshin_characters


def get_voiceline(character):
    link = "https://genshin-impact.fandom.com/wiki/{}/Voicelines".format(character)
    dfs = pd.read_html(link)
    df = dfs[2]
    if character == "Fischl":
        voice_df = df.loc[df['Title'] == "Good Morning: Greet Fischl"]
    else:
        voice_df = df.loc[df['Title'] == "Good Morning"]
    voice_string = (voice_df.iloc[0]["Official Transcription"])
    voiceline = voice_string.split(".ogg ")[1]
    return voiceline


def get_specific_voiceline(character, phrase):
    link = "https://genshin-impact.fandom.com/wiki/{}/Voicelines".format(character)
    print(link)
    dfs = pd.read_html(link)
    df = dfs[2]
    if phrase == "Good Morning":
        if character == "Fischl":
            voice_df = df.loc[df['Title'] == "Good Morning: Greet Fischl"]
        else:
            voice_df = df.loc[df['Title'] == "Good Morning"]
    else:
        voice_df = df.loc[df['Title'] == phrase]
    voice_string = (voice_df.iloc[0]["Official Transcription"])
    voiceline = voice_string.split(".ogg ")[1]
    return voiceline


# def get_all_voicelines():
#     chars = get_characters()
#     chars.remove("Traveler")
#     voicelines = list()
#     for c in chars:
#         character = c.replace(" ", "_")
#         print(character)
#         voicelines.append(get_voiceline(character))
#     return voicelines


def get_random_voiceline(phrase):
    char = get_random_character().replace(" ", "_")
    print("getting voiceline for character: {}".format(char))
    vl = get_specific_voiceline(char, phrase)
    return char, vl


def get_random_voiceline_and_image(phrase):
    character = get_random_character()
    char_formatted = character.replace(" ", "_")
    print("getting voiceline for character: {}".format(char_formatted))
    vl = get_specific_voiceline(char_formatted, phrase)
    image = get_image(character)
    print("Returning stuff")
    return char_formatted, vl, image


def get_random_character():
    chars = get_characters()
    chars.remove("Traveler")
    char = random.choice(chars)
    return char


def image_to_byte_array(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def split_surname(character):
    # firstname refers to their given name, since the names are chinese this is the second name (Kamisato Ayaka becomes Ayaka)
    if character.find(" ") != -1 and character != "Hu Tao":
        character_firstname = character.split(" ")[1]
    else:
        character_firstname = character
    return character_firstname


def get_image(character):
    char = split_surname(character)
    url = "https://rerollcdn.com/GENSHIN/Characters/{}.png".format(char)
    print(url)
    img = Image.open(requests.get(url, stream=True).raw)
    return image_to_byte_array(img)

