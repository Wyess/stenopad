#!/usr/local/bin/python3.11

import webview
from shorthand_character import String
import tomli
from datetime import datetime

#from load_xml import Shorthand, load_dict_xml

class Api:
    def __init__(self):
        self.sh_dict = {}
        self.sh = None
        self.load_config()

    def get_shorthand_list(self):
        return {'shorthand_list': list(self.shorthand_list)}

    def text2shorthand(self, text, shorthand, to_animate=False, speed_mm_per_s=25):
        if self.sh_dict is not None:
            svg, time_s = String(text, self.sh_dict['waseda']).create_path_elements(to_animate, speed_mm_per_s)
            return {'message': svg, 'time_s': f"{time_s:0.1f}"}
        else:
            return {'message': '', 'time_s': f"{0:0.1f}"}

    def load_text_file(self):
        file_types = ('Text files (*.txt)', 'All files(*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        try:
            with open(result[0]) as f:
                return {"message": f.read()}
        except TypeError as e:
            pass

    def load_config(self, config_toml='config.toml'):
        with open(config_toml, "rb") as f:
            config = tomli.load(f)
            toml_str = ""
            for shorthand in config['dictionaries']:
                with open(shorthand['filename'], "rb") as sf:
                    toml_str += sf.read().decode()
            self.sh_dict = tomli.loads(toml_str)
            self.shorthand_list = list(self.sh_dict.keys())
            self.sh_dict = tomli.loads(toml_str)
        #self.sh = load_dict_xml("waseda.xml")

            #tree = etree.parse("waseda.xml")
            #tree.xinclude()
            #root = tree.getroot()
            #self.xml_tree = root

    def export_svg(self, svg_str):
        timestamp = datetime.now().strftime("%Y_%m%d_%H%M%S")
        filename = f"out_{timestamp}.svg"

        with open(filename, 'w') as f:
            f.write(svg_str)


html = """
<!DOCTYPE html>
<html>
<head>
<style type="text/css">
    #sh_input {
        width:100%;
    }
    #svg_root {
        width:100%;
    }
</style>
</head>
<body>
<div id='svg'></div>
<textarea id="sh_input" oninput="set_svg()" onkeyup="set_svg()"></textarea>
<button onclick="set_svg(true)">Animate</button>
<button onclick="load_text_file()">Open</button>
<button onclick="reload_dict()">Reload dictionary</button>
<button onclick="export_svg()">Export SVG</button><br/>
<label>Speed [mm/s]</label>
<input id="speed_input" type="number" max="100" min="1" step="1" value="20"/><br>
<label>Time [s]</label>
<input id="time_s" type="number"/> <br>
<select id="shorthand_select">
<!--
<option>waseda</option>
<option>gregg</option>
-->
</select>

<script>
window.addEventListener('pywebviewready', function() {
    pywebview.api.get_shorthand_list().then(function(response) {
        var select = document.getElementById('shorthand_select');
        var shorthand_list = response['shorthand_list'];
        for (var i = 0; i < shorthand_list.length; i++) {
            var opt = document.createElement("option");
            opt.value = shorthand_list[i];
            opt.text = shorthand_list[i];
            select.add(opt);
        }
        var shorthand = shorthand_select.options[shorthand_select.selectedIndex].value;
        pywebview.api.text2shorthand("", shorthand).then(function(response) {
            var svg_div = document.getElementById('svg');
            svg_div.innerHTML = response.message;
        });
    });
});

var select = document.getElementById('shorthand_select');
select.onchange = event => {
    set_svg();
}

function set_svg(to_animate=false) {
    var speed_input = document.getElementById('speed_input');
    var svg_input = document.getElementById('sh_input');
    var time_input = document.getElementById('time_s');
    var speed_mm_per_s = +speed_input.value;
    var shorthand_select = document.getElementById('shorthand_select');
    var shorthand = shorthand_select.options[shorthand_select.selectedIndex].value;

    pywebview.api.text2shorthand(svg_input.value, shorthand, to_animate, speed_mm_per_s).then(function(response) {
        var svg_div = document.getElementById('svg');
        time_input.value = response.time_s;
        svg_div.innerHTML = response.message;
        console.log(response.message);
        var svg_root = document.getElementById('svg_root');
        svg_root.setCurrentTime(0);
    });
}

function load_text_file() {
    var svg_input = document.getElementById('sh_input');
    pywebview.api.load_text_file().then(function(response) {
        svg_input.value = response.message;
    });
    set_svg();
}

function reload_dict() {
    pywebview.api.load_config().then(function() {
        set_svg();
    });
}

function export_svg() {
    var svg = document.getElementById('svg');
    pywebview.api.export_svg(svg.innerHTML).then(function() {});
}


</script>

</body>
</html>

"""
window = webview.create_window('Stenopad', html=html, js_api=Api())
webview.start(debug=True)

