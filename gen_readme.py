#!/bin/python
import json
import datetime

grouped_mods = {}

with open("master/manifest.json", "r", encoding = "UTF-8") as f:
    MANIFEST = json.load(f)
    for mod_guid in MANIFEST["mods"]:
        mod = MANIFEST["mods"][mod_guid]
        mod["guid"] = mod_guid

        if "flags" not in mod or (
            "plugin" not in mod["flags"] and
            "file" not in mod["flags"]
        ):
            mods = grouped_mods.get(mod["category"])
            if mods is None:
                mods = []

            mods.append(mod)
            grouped_mods[mod["category"]] = mods

README = None
with open("gh-pages/.templates/mod-list-template.md", "r", encoding = "UTF-8") as f:
    README = f.read()

now = datetime.datetime.now(tz=datetime.timezone.utc)
README += "Last updated at "
README += f"<time datetime='{now.isoformat()}'>{now.strftime('%d %B %Y, %I:%S')} UTC</time>\n\n"

for group, mods in grouped_mods.items():
    mods = mods.sort(key=lambda mod: mod["name"])

for group, mods in sorted(grouped_mods.items()):
    README += f"\n## {group}\n"
    for mod in mods:
        README += "\n<!--" + mod["guid"] + "-->\n"
        README += "#### "
        README += f"[{mod['name']}]({mod['sourceLocation']})"

        # mod must have versions
        if mod["versions"] is None or len(mod["versions"]) == 0:
            continue

        # mod must have a non-vulnerable version
        all_vulnerable = True
        for key, version in mod["versions"]:
            if version.flags is None:
                all_vulnerable = False
                break
            else:
                vulnerable = False
                for flag in version.flags:
                    if flag.startswith("vulnerability:"):
                        vulnerable = True
                        continue
                if not vulnerable:
                    all_vulnerable = False
                    break
        if all_vulnerable:
            continue

        if len(mod["authors"]) > 0:
            README += " by "
            for author_name, author_data in mod["authors"].items():
                README += f"[{author_name}]({author_data['url']}), "
            # Remove the ", "
            README = README[:-2]

        README += "\n\n"

        README += mod['description'] + "\n"


with open("gh-pages/mods.md", "w", encoding = "UTF-8") as f:
    f.write(README)
