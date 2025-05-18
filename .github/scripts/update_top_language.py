import os
import requests

REPO = "erzer12/erzer12"
README = "README.md"
BADGE_START = "<!-- TOP_LANGUAGE_BADGE_START -->"
BADGE_END = "<!-- TOP_LANGUAGE_BADGE_END -->"

def get_top_language():
    api_url = f"https://api.github.com/repos/{REPO}/languages"
    headers = {}
    token = os.environ.get('GITHUB_TOKEN', '')
    if token:
        headers['Authorization'] = f'token {token}'
    resp = requests.get(api_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return "None"
    return max(data, key=data.get)

def update_readme(top_language):
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    badge_markdown = f"![Top Language](https://img.shields.io/badge/top%20language-{top_language}-blue?style=for-the-badge)"
    new_section = f"{BADGE_START}\n{badge_markdown}\n{BADGE_END}"

    if BADGE_START in content and BADGE_END in content:
        start = content.index(BADGE_START)
        end = content.index(BADGE_END) + len(BADGE_END)
        content = content[:start] + new_section + content[end:]
    else:
        content = new_section + "\n\n" + content

    with open(README, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    top_language = get_top_language()
    update_readme(top_language)
