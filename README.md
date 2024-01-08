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
6. Add subreddit names in `.github/workflows/slack-message.yml`.

## Usage
```bash
$ python main.py -h

usage: main.py [-h] [--token TOKEN] [--channel-id CHANNEL_ID] [--subreddit SUBREDDIT]
               [--n-posts N_POSTS]

options:
  -h, --help            show this help message and exit
  --token TOKEN         Slack API Token
  --channel-id CHANNEL_ID
                        Slack Channel ID
  --subreddit SUBREDDIT
                        Subreddit Name
  --n-posts N_POSTS     Max Posts Number
```

## Looks like...
<img width="1143" src="https://github.com/Curt-Park/reddit-posts-to-slack/assets/14961526/14315a30-3285-433c-9a2a-5f4387e5814b">
