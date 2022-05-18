# Tomimi Bot
A simple discord bot made using [hikari](https://github.com/hikari-py/hikari/) and [lightbulb](https://github.com/tandemdude/hikari-lightbulb).
Currently, you can use it to play wordle.

## Using the bot

```
git clone https://github.com/serupt/Tomimi-Bot.git
cd Tomimi-Bot
pip install -r requirements.txt
```

Make an .env file with the following
```
TOKEN = bot token
GUILD_IDS = server guild id
LAVA_HOST = "lavalink" if running in docker, else "127.0.0.1"
LAVA_PW = password in the lavalink/application.yml
```

## Run using docker
```
docker-compose up -d
```
## Run without docker
For music, you need lavalink server 
```
cd lavalink
java -jar Lavalink.jar
```
Run bot with 
```
python3 -m tomimibot
```

