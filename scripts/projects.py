import argparse
import json
import os
import urllib.request
from pathlib import Path
from typing import TypedDict

project_file_path = Path("site/data/projects.json")


def get_github_token():
    if not Path(".env").exists():
        return os.getenv("GH_API_TOKEN")
    content = Path(".env").read_text()
    for line in content.splitlines():
        if line.startswith("GH_API_TOKEN="):
            return line.split("=")[1]


GITHUB_API_TOKEN = get_github_token()
OPEN_SOURCE = "Open Source"


class Project(TypedDict):
    last_updated: str
    name: str
    description: str
    stack: str
    company: str
    web_url: str
    github_url: str
    featured: bool
    active: bool
    private: bool


def github_api_request(path: str) -> dict:
    url = f"https://api.github.com/{path}"
    headers = {"Authorization": f"Bearer {GITHUB_API_TOKEN}"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    return json.load(response)


def update_dates(_):
    with open(project_file_path) as file:
        projects: list[Project] = json.load(file)

    need_update = [
        project
        for project in projects
        if project.get("active") and project.get("company") == OPEN_SOURCE
    ]

    for project in need_update:
        github_url = project.get("github_url")
        repo_name = github_url.split("/")[-1]
        commits = github_api_request(f"repos/Tobi-De/{repo_name}/commits")
        last_update = commits[0]["commit"]["author"]["date"]
        last_update_date = last_update.split("T")[0]
        if project.get("last_updated") != last_update_date:
            print(f"Updating {project['name']}")
            project["last_updated"] = last_update_date

    with open(project_file_path, "w") as file:
        json.dump(projects, file)


def add_project(args):
    project_name = args.project_name
    dry_run = args.dry_run

    try:
        github_project = github_api_request(f"repos/Tobi-De/{project_name}")
    except urllib.error.HTTPError:
        print(f"Project {project_name} does not exist or maybe GH_API_TOKEN is not set")
        exit(1)

    with open(project_file_path, "r") as file:
        projects = json.load(file)

    web_url = github_project.get("homepage") or input("Enter web url: ")
    if not web_url:
        web_url = github_project["html_url"]
    featured = input("Is this project featured? (y/n): ") == "y"
    stack = input("Enter stack: ")

    project = {
        "last_updated": github_project["pushed_at"].split("T")[0],
        "name": project_name,
        "description": github_project["description"],
        "stack": stack,
        "company": OPEN_SOURCE,
        "web_url": web_url,
        "github_url": github_project["html_url"],
        "featured": featured,
        "active": True,
        "private": False,
    }

    projects.append(project)

    if dry_run:
        from pprint import pprint

        pprint(project)
        exit(0)

    with open(project_file_path, "w") as file:
        json.dump(projects, file)


def main():
    parser = argparse.ArgumentParser(description="Make update to my projects")
    subparsers = parser.add_subparsers(dest="command")

    update_dates_parser = subparsers.add_parser(
        "update-dates", help="Update dates command"
    )
    update_dates_parser.set_defaults(func=update_dates)

    add_project_parser = subparsers.add_parser(
        "add-project", help="Add project command"
    )
    add_project_parser.add_argument(
        "project_name", type=str, help="Name of the project"
    )
    add_project_parser.add_argument("--dry-run", action="store_true", help="Dry run")
    add_project_parser.set_defaults(func=add_project)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("possible commands")
        print("python -m projects add-project <project_name> --dry-run")
        print("python -m projects update-dates")


if __name__ == "__main__":
    main()
