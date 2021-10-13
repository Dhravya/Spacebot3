import json, random, requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import discord

def get_prefix(bot,message): ##first we define get_prefix
    with open('otherfiles/data/db/database.json', 'r') as f: ##we open and read the prefixes.json, assuming it's in the same file
        db = json.load(f) #load the json as prefixes
    try:
        return db["servers"][message.guild.id]["settings"]["prefix"]
    except:
        return '.'

def random_percentage():
    f = random.randint(0, 100)
    g = random.randint(0, 100)
    return str(f) + "." + str(g)

class Votelink(discord.ui.View):
    def __init__(self):
        super().__init__()

        url = f"https://top.gg/bot/881862674051391499"
        self.add_item(discord.ui.Button(label="Click Here to vote", url=url))


voteembed = discord.Embed(
    title="This feature is for voters only!",
    description="Yes, it sucks. But because I earn nothing through the bot itself, voting is the only way to support me!! so.. please vote... :point_right::point_left:",
).set_footer(text="If you think that this command should not be for voters only,\nPlease use the .suggestdev command and let me know.")

MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ", ": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
}

def encrypt(message):
    cipher = ""
    for letter in message:
        if letter != " ":

            # Looks up the dictionary and adds the
            # correspponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + " "
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += " "

    return cipher


def decrypt(message):

    # extra space added at the end to access the
    # last morse code
    message += " "

    decipher = ""
    citext = ""
    for letter in message:

        # checks for space
        if letter != " ":

            # counter to keep track of space
            i = 0

            # storing morse code of a single character
            citext += letter

        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1

            # if i = 2 that indicates a new word
            if i == 2:

                # adding space to separate words
                decipher += " "
            else:

                # accessing the keys using their values (reverse of encryption)
                decipher += list(MORSE_CODE_DICT.keys())[
                    list(MORSE_CODE_DICT.values()).index(citext)
                ]
                citext = ""

    return decipher


def synonyms(term):
    response = requests.get("https://www.thesaurus.com/browse/{}".format(term))
    soup = BeautifulSoup(response.text, "lxml")
    soup.find("section", {"class": "css-191l5o0-ClassicContentCard e1qo4u830"})
    return [
        span.text
        for span in soup.findAll("a", {"class": "css-r5sw71-ItemAnchor etbu2a31"})
    ]


class MissingRequiredArgument(Exception):
    pass


class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        # we need to quote the query string to make a valid url. Discord will raise an error if it isn't valid.
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label="Click Here", url=url))



class Invite(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="Click Here",
                url="https://discord.com/api/oauth2/authorize?client_id=881862674051391499&permissions=0&scope=bot",
            )
        )

