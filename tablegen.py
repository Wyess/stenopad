#!/usr/local/bin/python3.11

from shorthand_character import String as ShorthandString
import tomli

with open("waseda_asy.toml", "rb") as f:
    sh_dict = tomli.load(f)

with open("waseda_table.toml", "rb") as f:
    config = tomli.load(f)

base_list = []

for d in config['direction']:
    base_list.extend([f"{d}{o}" for o in config['orientation']])
base_list.extend(config['base'])

primary_list = []
for base in base_list:
    for tail in config['tailtype']:
        key = f"{base}{tail}"
        primary_list.append(key)

secondary_list = []
for dir_s in config['direction']:
    for ori_s in config['orientation']:
        key = f"{dir_s}{ori_s}"
        secondary_list.append(key)

print("<!DOCTYPE html>")
print("<html>")
print("<table border=\"1\">")
print("<thead>")
print("<tr>")
print("<th></th>")
for key2 in secondary_list:
    print(f"<th>{key2}</th>")
print("</tr>")
print("</thead>")
for key in primary_list:
    print("<tr>")
    print(f"<th>{key}</th>")
    for key2 in secondary_list:
        elem = config.get(key, {}).get(key2, {}).get("html", "")
        #print(f"<td>{elem}</td>")
        text = config.get(key, {}).get(key2, {}).get("text", "")
        if text:
            s = ShorthandString(text, sh_dict["waseda"], fixed_viewbox=False)
            svg, time_s = s.create_path_elements(False)
            print(f"<td>{svg}</td>")
        else:
            print(f"<td></td>")
    print("</tr>")
print("</html>")
