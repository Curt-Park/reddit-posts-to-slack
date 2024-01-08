"""Parse subreddits' hot posts and send the message to Slack."""
import requests
from bs4 import BeautifulSoup

import subreddits


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
    post_infos: list[str] = [f"*Today's Hot Posts in Subreddit {name}*\n"]
    for i, post in enumerate(posts):
        # Fetch the post info.
        title = post.find("a", class_="title").text
        upvotes = post.find("div", class_="score unvoted").text
        comments = post.find("a", class_="comments").text.split()[0]
        post_url = post.find("a", class_="title")["href"]
        # date = post.find("p", class_="tagline").find("time")["title"]

        # Post may be redirected to a number of url types.
        if not post_url.startswith("http"):
            post_url = "https://old.reddit.com" + post_url

        # Append the post info.
        post_info = f"{i+1:2d}. Title: {title} [Upvotes {upvotes}, Comments: {comments}]\n"
        post_info += f">>> URL: {post_url}\n"
        post_infos.append(post_info)
