from pyscript import document
import js
import json
from shorthand_string import String

with open('./waseda.json', 'r', encoding='utf8') as f:
    sdict = json.load(f)

def on_input(evt):
    text = document.getElementById("inputTextArea").value
    document.getElementById("shorthand_svg").innerHTML = String(text, sdict["waseda"])
