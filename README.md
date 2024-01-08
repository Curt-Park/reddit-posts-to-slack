# Reddit Daily Hot Posts for Slack

This project triggers sending messages to a specific slack channel.
The meesages contain information of the subreddits' hot posts.

## Prerequisites
1. Create [a slack application](https://api.slack.com/apps).
2. Install the application on your slack workspace.
3. In `OAuth & Permissions`, add `chat:write` for `Bot Token Scopes`.
4. Create a new channel and add the application in it.
5. Setup the following secrets for this repo.
- `SLACK_CHANNEL_ID`
- `SLACK_OAUTH_TOKEN`
6. Add subreddit names in `subreddits.py`.
