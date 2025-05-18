import os
import requests
import svgwrite

USER = "erzer12"
OUTPUT = "top-langs.svg"

def get_langs():
    repos = []
    page = 1
    while True:
        r = requests.get(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}")
        data = r.json()
        if not data or "message" in data:
            break
        repos.extend(data)
        page += 1
    lang_totals = {}
    for repo in repos:
        if repo["fork"]:
            continue
        langs = requests.get(repo["languages_url"]).json()
        for lang, count in langs.items():
            lang_totals[lang] = lang_totals.get(lang, 0) + count
    return lang_totals

def make_svg(lang_totals):
    dwg = svgwrite.Drawing(OUTPUT, size=("500px", "200px"), profile='tiny')
    sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    total = sum(x[1] for x in sorted_langs) or 1
    y = 40
    for lang, count in sorted_langs:
        percent = count / total * 100
        width = percent * 4
        dwg.add(dwg.rect(insert=(150, y-20), size=(width, 20), fill="#58A6FF"))
        dwg.add(dwg.text(f"{lang} ({percent:.1f}%)", insert=(10, y-5), font_size="18px", fill="#fff"))
        y += 35
    dwg.add(dwg.text("Top Languages", insert=(10, 25), font_size="22px", fill="#fff"))
    dwg.save()

if __name__ == "__main__":
    langs = get_langs()
    if langs:
        make_svg(langs)
