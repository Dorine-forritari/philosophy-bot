import discord
import os
import random
from replit import db
from staying_alive import staying_alive


client = discord.Client()

# These are keywords that the bot responds to with a random philosophy quote. 
key_words = ["how", "life", "meaning", "philosophy"]

# These are special keywords that always generate a quote about Sisyphus. I added this piece of code for I., who loves this quote. 
struggle = ["struggle", "why try"]

# This is a base list of quotes that the bot replies with in response to the keywords. They can't be removed by users. 
phil_quotes = ["'The unexamined life is not worth living.' -Socrates",
"'Life must be understood backward. But it must be lived forward.' -Søren Kierkegaard",
"'Things alter for the worse spontaneously, if they be not altered for the better designedly.' -Francis Bacon",
"'Is man merely a mistake of God's? Or God merely a mistake of man's?' -Friedrich Nietzsche",
"'I would never die for my beliefs because I might be wrong.' -Bertrand Russell",
"'Happiness is not an ideal of reason but of imagination.' –Immanuel Kant"]

# This is the Sisyphus quote, in response to the 'struggle' keywords.
sisyphus = "One must imagine Sisyphus happy."

# With this function a quote can be added to the database.
def update_quotes(quote):
  if "quotes" in db.keys():
    quotes = db["quotes"]
    quotes.append(quote)
    db["quotes"] = quotes
  else:
    db["quotes"] = [quote]

# With this function a quote is deleted from the database.
def delete_quote(index):
  quotes = db["quotes"]
  if len(quotes) > index:
    del quotes[index]
    db["quotes"] = quotes

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

# This is to make sure the bot doesn't respond to his own messages.
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = (message.content).lower()

  all_quotes = phil_quotes
  if "quotes" in db.keys():
    all_quotes = all_quotes + db["quotes"]
  
  # To let the bot send randomly picked quotes in response to keywords.
  if any(word in msg for word in key_words):
    await message.channel.send(random.choice(all_quotes))
  if any(word in msg for word in struggle):
    await message.channel.send(sisyphus)

  # This lets the users in Discord add new quotes.
  if msg.startswith("$new"):
    quote = msg.split("$new ", 1)[1]
    update_quotes(quote)
    await message.channel.send("New philosophy quote added.")

  # This lets the users in Discord delete quotes. Quotes from the base list cannot be deleted by users. After deleting a quote the bot shows the list of remaining quotes. 
  if msg.startswith("$del"):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_quote(index)
      quotes = db["quotes"]
    await message.channel.send(quotes)

  # With this request the user can get a list of the quotes in the database.
  if msg.startswith("$list"):
    await message.channel.send(all_quotes)

  # To get a 'hello' greeting from the bot.
  if msg.startswith("$hello"):
    await message.channel.send("Hello!")

# This function makes sure the bot stays active, even when the repl.it browser is closed. 
staying_alive()

client.run(os.getenv("TOKEN"))