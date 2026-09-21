#!/usr/bin/env python3

import re

_model_re = re.compile(r"""
    (?P<head>(?:c[lr]1)?)
    (?P<body_pre>(?:[uo])?)
    (?P<body>
        (
            ([sn][ew]|[news])[rl]?
            (?P<body_main_len>(3|4|8|16|25))
        )+
    )
    (?P<tail>(
        c[lr](1|4|8)
      | o([sn][ew]|[news])[rl]4
    )?)
    (?P<flick>f?)
    |
    (?P<circle>(?:c[lr]1)?)
""", re.VERBOSE)

def model2tags(model: str):
    tags = []
    tags.append(f"@model_{model}")
    if m := _model_re.match(model):
        model_wo_num = re.sub(r"\d", "", model)
        tags.append(f"@model_{model_wo_num}")

        head = m.group("head") or ""
        body = m.group("body_pre") + m.group("body")
        body_parts = re.split(r"(?<=\d)(?=\D)", body)

        tail = m.group("tail") or ""
        flick = m.group("flick")

        tags.append(f"@head_{head}{body_parts[0]}")
        body_part0_wo_num = re.sub(r'\d+', '', head + body_parts[0])
        tags.append(f"@head_{body_part0_wo_num}")

        tags.append(f"@tail_{body_parts[-1]}{tail}{flick}")
        body_parts_last_wo_num = re.sub(r'\d+', '', f"{body_parts[-1]}{tail}{flick}")
        tags.append(f"@tail_{body_parts_last_wo_num}")
    else:
        raise RuntimeError(f"{model} does not match")
    return tags

if __name__ == '__main__':
    models = [
        "ner8",
        "e8",
        "cl1el4",
        "uswl4",
        "ne8",
        "nel8",
        "uswl4",
        "e8cl1",
        "oswl4",
        "swl4swr4",
        "e8f",
        "ne8f",
        "e8cl1",
        "e8nw4",
    ]

    for model in models:
        tags = model2tags(model)
        print(tags)
