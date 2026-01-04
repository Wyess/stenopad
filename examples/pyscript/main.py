from pyscript import document
import js
import tomli
from shorthand_character import String

with open("./waseda_asy.toml", "rb") as f:
    config = tomli.load(f)

def on_input(evt):
    text = document.getElementById("inputTextArea").value
    document.getElementById("shorthand_svg").innerHTML = String(text, config["waseda"])
