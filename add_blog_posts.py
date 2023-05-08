from pathlib import Path

import feedparser


def get_latest_posts():
    posts = feedparser.parse("https://oluwatobi.dev/rss.xml/")["entries"][:5]
    posts_md = [f'- [{post["title"]}]({post["link"]})' for post in posts]
    return "\n" + "\n".join(posts_md) + "\n"


def main():
    readme = Path(__file__).parent / "README.md"
    text = readme.read_text()
    start_comment = "<!-- BLOG-POST-LIST:START -->"
    end_comment = "<!-- BLOG-POST-LIST:END -->"
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    new_content = text[:start_index] + get_latest_posts() + text[end_index:]
    readme.write_text(new_content)


if __name__ == "__main__":
    main()
