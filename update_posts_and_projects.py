from pathlib import Path
from operator import itemgetter
import json
import urllib.request

import feedparser

readme = Path(__file__).parent / "README.md"
projects_url = "https://raw.githubusercontent.com/Tobi-De/pw/main/data/projects.json"


def _extract_date(post):
    date_string = post["published"]
    return date_string.split("T")[0]


def get_latest_posts():
    posts = feedparser.parse("https://oluwatobi.dev/rss.xml/")["entries"]
    posts = sorted(posts, key=itemgetter("published_parsed"), reverse=True)[:6]
    posts_md = [
        f'- [{post["title"]}]({post["link"]}) [{_extract_date(post)}]' for post in posts
    ]
    return "\n" + "\n".join(posts_md) + "\n"


def get_project_description(gh_url):
    project_name = gh_url.split("/")[-1]
    url = f"https://api.github.com/repos/Tobi-De/{project_name}"
    resp = urllib.request.urlopen(url)
    data = json.load(resp)
    return data.get("description")


def get_latest_projects():
    data = urllib.request.urlopen(projects_url).read()
    projects = json.loads(data)
    projects = [project for project in projects if project["featured"]]
    projects = sorted(projects, key=itemgetter("last_updated"), reverse=True)[:6]
    projects_md = []
    for project in projects:
        description = (
            get_project_description(project["github_url"]) or project["description"]
        )
        projects_md.append(
            f'- [{project["name"]}]({project["github_url"]}): {description}'
        )
    return "\n" + "\n".join(projects_md) + "\n"


def update_readme(start_comment, end_comment, new_content):
    text = readme.read_text()
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    new_content = text[:start_index] + new_content + text[end_index:]
    readme.write_text(new_content)


def main():
    update_readme(
        "<!-- BLOG-POST-LIST:START -->",
        "<!-- BLOG-POST-LIST:END -->",
        get_latest_posts(),
    )
    update_readme(
        "<!-- PROJECT-LIST:START -->",
        "<!-- PROJECT-LIST:END -->",
        get_latest_projects(),
    )


if __name__ == "__main__":
    main()
