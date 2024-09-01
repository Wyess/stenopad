#!/usr/local/bin/python3.11

import tomli
import tomli_w

with open('_waseda_asy.toml', 'rb') as f:
    sh_dict = tomli.load(f)
    for g in sh_dict['waseda']['groups']:
        sh_dict['waseda']['groups'][g] = [item['char'] for item in sh_dict['waseda']['groups'][g]]

    for d in sh_dict['waseda']['dictionary']:
        sh_dict['waseda']['dictionary'][d] = sh_dict['waseda']['dictionary'][d]['chars']

    with open('waseda_asy.toml', 'w', encoding='utf8') as wf:
        print(tomli_w.dumps(sh_dict), file=wf)

