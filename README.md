# Discord Notification Bot 🤖

A feature-rich Discord bot that handles notifications, user information, and server management. Perfect for communities that need a reliable way to manage member communications and server information.

## Features 

- **Notification System**
  - Direct message notifications to specific users
  - Mass notification system for opted-in users
  - Opt-in/opt-out functionality for users

- **User Management**
  - Detailed user information command
  - Server statistics tracking
  - Welcome messages for new server joins

- **Server Tools**
  - Ping command to check bot latency
  - Embedded messages for clean formatting
  - Command cooldown system to prevent spam

## Prerequisites 📋

Before running the bot, make sure you have:

- Python (v3.8 or higher)
- A Discord Bot Token
- Required Python packages (see below)

## Installation 🚀

1. Clone the repository
```bash
git clone [your-repository-url]
cd discord-notification-bot
```

2. Set up a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your bot token:
```env
BOT_TOKEN=your_discord_bot_token_here
```

5. Start the bot:
```bash
python main.py
```

## Commands 🎮

| Command | Description | Permission |
|---------|-------------|------------|
| `!help` | Shows all available commands | Everyone |
| `!optin` | Opt in to receive notifications | Everyone |
| `!optout` | Opt out of notifications | Everyone |
| `!notify @user message` | Send a DM to specific user | Admin only |
| `!notifyall message` | Send a DM to all opted-in users | Admin only |
| `!ping` | Check bot's response time | Everyone |
| `!userinfo @user` | Get information about a user | Everyone |

## Setting Up the Bot 🛠️

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the Bot section and create a bot
4. Get your bot token
5. Enable necessary intents:
   - GUILDS
   - GUILD_MESSAGES
   - DIRECT_MESSAGES
   - MESSAGE_CONTENT
   - GUILD_MEMBERS

## Required Permissions 🗌

The bot needs the following permissions to function properly:
- Read Messages/View Channels
- Send Messages
- Send Messages in Threads
- Embed Links
- Read Message History
- Add Reactions

## Demo Video 🎥

Watch a demo of the bot in action:
https://github.com/user-attachments/assets/9ac24541-a8b5-4287-8148-624d9839f554
