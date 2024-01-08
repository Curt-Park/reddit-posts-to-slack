"""Parse subreddits' hot posts and send the message to Slack.

- Author: Curt Park
- Contact: www.jwpark.co.kr@gmail.com
"""
import argparse

import requests
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import subreddits

parser = argparse.ArgumentParser()
parser.add_argument("--token", type=str, help="Slack API Token")
parser.add_argument("--channel-id", type=str, help="Slack Channel ID")
parser.add_argument("--n-posts", type=int, default=20, help="Max Posts Number")
args = parser.parse_args()

client = WebClient(token=args.token)


# Read every subreddit's hot posts.
for name in subreddits.names:
    # Get the webpage.
    url = f"https://old.reddit.com/r/{name}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the webpage.
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", class_="thing")

    # Get the important information from all posts.
    post_infos: list[tuple[int, str]] = []
    for i, post in enumerate(posts):
        # Skip promotion.
        promotion = post.find("p", class_="tagline").text.startswith("promoted")
        if promotion:
            continue

        # Fetch the post info.
        title = post.find("a", class_="title").text
        upvotes = post.find("div", class_="score unvoted").text
        upvotes = upvotes.isdigit() and int(upvotes) or 0
        post_url = post.find("a", class_="title")["href"]

        # Post may be redirected to a number of url types.
        if not post_url.startswith("http"):
            post_url = "https://old.reddit.com" + post_url

        # Append the post info.
        post_info = f"<{post_url}|{title}> [Upvotes {upvotes}]"
        post_infos.append((upvotes, post_info))

    # Sort by upvotes.
    post_infos = [
        f"{len(post_infos)-i}. {s}" for i, (_, s) in enumerate(sorted(post_infos))
    ]
    # Add the title.
    post_infos.append(f"*Today's Hot Posts of {name} Subreddit*\n")
    # Show `n_posts` at most.
    post_infos = post_infos[::-1][: args.n_posts + 1]

    # Send the post info to the slack channel.
    try:
        text = "\n".join(post_infos)
        response = client.chat_postMessage(channel=args.channel_id, text=text)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
