## Posts API

API consists of such endpoints:

1. `api/users/` for user creating.
2. `api/users/auth` for user authentication using JWT.
3. `api/posts/` for a post creating.
4. `api/posts/likes/<post-id>` for a post liking.
5. `api/users/activity/` for monitoring user activity.
6. `/api/analytics/` for likes analytics.

Also, for testing purposes was created a bot.
To start the bot, run `python bot.py`.
The bot configuration is situated in `bot_config.json` file.
