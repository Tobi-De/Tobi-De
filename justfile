# List all available commands
_default:
    @just --list --unsorted

@server:
    uv run coltrane play

@tailwind-watch:
    uv run tailwindcss -i site/static/css/input.css -o site/static/css/output.css --watch

@record:
    uv run coltrane record --output ../site-output --force


@add-project:
    uv run python scripts/projects.py