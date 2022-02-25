import random
from typing import Optional

import hikari
import lightbulb
import asyncio

popular_words = open("tomimibot/extensions/wordle/dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("tomimibot/extensions/wordle/dict-valid.txt"))

plugin_wordle = lightbulb.Plugin("Wordle")

EMOJI_CODES = {
    "green": {
        'a': '<:1f1e6:944696204430811177>',
        'b': '<:1f1e7:944696204481167390>',
        'c': '<:1f1e8:944696204200144918>',
        'd': '<:1f1e9:944696204305002547>',
        'e': '<:1f1ea:944696204590186496>',
        'f': '<:1f1eb:944696204053348363>',
        'g': '<:1f1ec:944696204586000485>',
        'h': '<:1f1ed:944696204418228346>',
        'i': '<:1f1ee:944696204263039078>',
        'j': '<:1f1ef:944696204497932358>',
        'k': '<:1f1f0:944696204586008627>',
        'l': '<:1f1f1:944696204527288360>',
        'm': '<:1f1f2:944696204539867136>',
        'n': '<:1f1f3:944696204510519377>',
        'o': '<:1f1f4:944696204485341284>',
        'p': '<:1f1f5:944696204472754217>',
        'q': '<:1f1f6:944696204531499028>',
        'r': '<:1f1f7:944696204422414398>',
        's': '<:1f1f8:944696204367892563>',
        't': '<:1f1f9:944696204443418634>',
        'u': '<:1f1fa:944696204451782666>',
        'v': '<:1f1fb:944696204577607731>',
        'w': '<:1f1fc:944696204497920020>',
        'x': '<:1f1fd:944696204208504883>',
        'y': '<:1f1fe:944696337050509373>',
        'z': '<:1f1ff:944696337331519568>',
    },
    "yellow": {
        'a': '<:1f1e6:944696369799651418>',
        'b': '<:1f1e7:944696369849991198>',
        'c': '<:1f1e8:944696369770270741>',
        'd': '<:1f1e9:944696369745133608>',
        'e': '<:1f1ea:944696369749307412>',
        'f': '<:1f1eb:944696369870946344>',
        'g': '<:1f1ec:944696369556365453>',
        'h': '<:1f1ed:944696369686388757>',
        'i': '<:1f1ee:944696369875140678>',
        'j': '<:1f1ef:944696369774465074>',
        'k': '<:1f1f0:944696369753518180>',
        'l': '<:1f1f1:944696369862549554>',
        'm': '<:1f1f2:944696369749327922>',
        'n': '<:1f1f3:944696369501859911>',
        'o': '<:1f1f4:944696369921290250>',
        'p': '<:1f1f5:944696369917079583>',
        'q': '<:1f1f6:944696369841586257>',
        'r': '<:1f1f7:944696369883545680>',
        's': '<:1f1f8:944696369862541372>',
        't': '<:1f1f9:944696369791250453>',
        'u': '<:1f1fa:944696369891930152>',
        'v': '<:1f1fb:944696369774460948>',
        'w': '<:1f1fc:944696369371807753>',
        'x': '<:1f1fd:944696369388589097>',
        'y': '<:1f1fe:944696369812222033>',
        'z': '<:1f1ff:944696369787052062>',
    },
    "gray": {
        'a': '<:1f1e6:944696076533907466>',
        'b': '<:1f1e7:944696076361924638>',
        'c': '<:1f1e8:944696076361953300>',
        'd': '<:1f1e9:944696076353564722>',
        'e': '<:1f1ea:944696076374511766>',
        'f': '<:1f1eb:944696076374540298>',
        'g': '<:1f1ec:944696076382928896>',
        'h': '<:1f1ed:944696076454211654>',
        'i': '<:1f1ee:944696076223512587>',
        'j': '<:1f1ef:944696076466790470>',
        'k': '<:1f1f0:944696076441616394>',
        'l': '<:1f1f1:944696076420653176>',
        'm': '<:1f1f2:944696076403900517>',
        'n': '<:1f1f3:944696076663939162>',
        'o': '<:1f1f4:944696076366118984>',
        'p': '<:1f1f5:944696076412264468>',
        'q': '<:1f1f6:944696076009611275>',
        'r': '<:1f1f7:944696076512932000>',
        's': '<:1f1f8:944696076366151760>',
        't': '<:1f1f9:944696076429041695>',
        'u': '<:1f1fa:944696076127043655>',
        'v': '<:1f1fb:944696076387102780>',
        'w': '<:1f1fc:944696076215148596>',
        'x': '<:1f1fd:944696076357746768>',
        'y': '<:1f1fe:944696076475191306>',
        'z': '<:1f1ff:944696076156436521>',
    },
}

def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: hikari.User) -> hikari.Embed:
    puzzle_id = random_puzzle_id()
    embed = hikari.Embed(title=f'{user.username}\'s Wordle Game', description = "\n".join([generate_blanks()] * 6))
    embed.set_author(name=user.username,icon=user.avatar_url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /wordle!\n"
        "To guess, reply to this message with a word."
    )
    return embed

def update_embed(embed: hikari.Embed, guess: str) -> hikari.Embed:
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed



def is_valid_word(word: str) -> bool:
    return word in all_words


def random_puzzle_id() -> int:
    return random.randint(0, len(popular_words) - 1)


def is_game_over(embed: hikari.Embed) -> bool:
    return "\n\n" in embed.description

async def process_message_as_guess(bot: lightbulb.BotApp, event: hikari.GuildMessageCreateEvent) -> bool:
    # get the message replied to
    ref = event.message
    
    if not ref or not isinstance(ref.referenced_message, hikari.Message):
        return False
    
    parent = ref.referenced_message

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.get_me().id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = event.message.content.lower()
    

    # check that the user is the one playing
    if ((embed.author.name)!=(event.message.author.username)):
        reply = (f'This game was started by {embed.author.name}. Start a new game with /wordle')
        msg = await event.message.respond(reply)
        await event.message.delete()
        await asyncio.sleep(2)
        await msg.delete()
        return False


    # check that the game is not over
    if is_game_over(embed):
        msg = await event.message.respond("The game is already over. Start a new game with /wordle")
        await event.message.delete()
        await asyncio.sleep(2)
        await msg.delete()
        return False

    # check that a single word is in the message
    if len(event.message.content.split()) > 1:
        msg = await event.message.respond("That is not a valid word.")
        await event.message.delete()
        await asyncio.sleep(2)
        await msg.delete()
        return False

    # check that the word is valid
    if not is_valid_word(guess):
        msg = await event.message.respond("That is not a valid word.")
        await event.message.delete()
        await asyncio.sleep(2)
        await msg.delete()
        return False

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)
    await event.message.delete()

    return True


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin_wordle)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin_wordle)