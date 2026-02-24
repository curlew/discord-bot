<div align="center">

# Discord Bot

[![Pylint](https://img.shields.io/github/actions/workflow/status/curlew/discord-bot/pylint.yml?label=pylint&style=flat-square&logo=github)](https://github.com/curlew/discord-bot/actions/workflows/pylint.yml)
![Latest tag](https://img.shields.io/github/v/tag/curlew/discord-bot?logo=github&style=flat-square)
[![License](https://img.shields.io/github/license/curlew/discord-bot?style=flat-square)](https://github.com/curlew/discord-bot/blob/main/LICENSE)

Container-based Discord bot using discord.py and PostgreSQL.

</div>

## Setup
1. [Install Docker Compose](https://docs.docker.com/compose/install).
2. [Create a Discord application](https://discord.com/developers/applications).
3. Add a bot user to the application. Under *Privileged Gateway Intents*, enable **server members intent** and **message content intent**.
4. Configure secrets:
    ```bash
    $ cp .env-sample .env
    $ vim .env # set TOKEN and POSTGRES_PASSWORD
    $ chmod 600 .env
    ```
5. Build and start the bot:
    ```bash
    $ docker compose up -d
    ```
6. Register the bot's application commands after adding it to a server, with the `-sync` command. See `-help sync`.

## Commands

Parameters in square brackets are optional.
Some app commands (slash commands) vary slightly from their text command equivalents.
The prefix for text commands is `-` (e.g. `-help`).

### General

| Command             | Description                                        |
|---------------------|----------------------------------------------------|
| `-serverinfo`       | Get information about the server.                  |
| `-userinfo [@user]` | Get information about `@user` (default: yourself). |
| `-uptime`           | Show how long the bot has been online for.         |

### Moderation

| Command                 | Description                                              |
|-------------------------|----------------------------------------------------------|
| `-autorole`             | Show the server's current autorole.                      |
| `-autorole set @role`   | Automatically assign `@role` to new server members.      |
| `-autorole off`         | Disable the server's autorole.                           |
| `-ban @user [reason]`   | Ban `@user`.                                             |
| `-kick @user [reason]`  | Kick `@user`.                                            |
| `-purge number`         | Bulk delete the newest `number` messages in the channel. |
| `-unban @user [reason]` | Unban `@user`.                                           |

### Meta

These commands are only available to the bot's owner.

| Command         | Description                                              |
|-----------------|----------------------------------------------------------|
| `-sync [guild]` | Sync application commands globally (or only to `guild`). |
