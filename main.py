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
parser.add_argument("--token", type=str,  help="Slack API Token")
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
    post_infos: list[str] = [f"*Today's Hot Posts of {name} Subreddit*\n"]
    for i, post in enumerate(posts):
        if i == args.n_posts:
            break
        # Fetch the post info.
        title = post.find("a", class_="title").text
        upvotes = post.find("div", class_="score unvoted").text
        post_url = post.find("a", class_="title")["href"]
        # comments = post.find("a", class_="comments").text
        # date = post.find("p", class_="tagline").find("time")["title"]

        # Post may be redirected to a number of url types.
        if not post_url.startswith("http"):
            post_url = "https://old.reddit.com" + post_url

        # Append the post info.
        post_info = f"{i+1:2d}. <{post_url}|{title}> [Upvotes {upvotes}]"
        post_infos.append(post_info)

    # Send the post info to the slack channel.
    try:
        response = client.chat_postMessage(channel=args.channel_id, text="\n".join(post_infos))
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
