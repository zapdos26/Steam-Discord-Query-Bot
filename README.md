[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# Steam-Discord-Query-Bot

This bot's primary function is to query servers that are specified, obtain information about them, and update a Discord embed accordingly.

### How to Setup the Discord Bot
1. Create a Discord bot account. You can find more information on how to create a bot account [here](https://discordpy.readthedocs.io/en/latest/discord.html)
2. Download the program. You can do this by either downloading it as a zip and unzipping it, or running

    `git clone https://github.com/zapdos26/Steam-Discord-Query-Bot.git`
3. Run `pip install -r requirements.txt`
4. Open up `configs/main.json.example` and fill in the necessary information. Save this file as  `main.json`.
5. Run the `discord_bot.py`. 
   - On Windows: `py discord_bot.py`
   - On Mac/Unix: `python discord_bot.py`
   
Congrats! You have set up the bot.

### Add Server to Check
1. Verify you have the `Manage Channel(s)` permission for where you want the Discord embed to be.
2. Run the following !addserver <IP> <Query Port> [appid]
    - Ex: `!addserver 127.0.0.1 1234 346110` would create an embed for the server with IP 127.0.0.1 and Query Port 1234 to the server list. The app id is necessary for the game's icon to show up.

## Credits

### Developers
- [Zapdos26](https://github.com/zapdos26)

### License
**Steam-Discord-Query-Bot** is provided under the [GNU GPLv3 License](https://github.com/zapdos26/Steam-Discord-Query-Bot/blob/master/LICENSE).

### Contact
For any question, comments, or concerns, [create an issue](https://github.com/zapdos26/Steam-Discord-Query-Bot/issues/new) or open a pull request.
