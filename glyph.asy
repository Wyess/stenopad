import util;
import lower;

//struct Dict {
//    file fout;
//
//    static Dict Dict(string filename) {
//        Dict d = new Dict;
//        d.fout = output(filename);
//        return d;
//    }
//    
//    void add(string word, string charname) {
//        write(this.fout, '<word name="' + word + '">' + charname + '</word>\n');
//    }
//
//    void close() {
//        close(this.fout);
//    }
//}
//
//struct CharSet {
//    file fout;
//
//    static CharSet CharSet(string filename) {
//        CharSet c = new CharSet;
//        c.fout = output(filename);
//        return c;
//    }
//
//    void add(string charname) {
//        write(this.fout, '<xi:include href="waseda_' + lc(charname) + '.xml" />');
//    }
//
//    void close() {
//        close(this.fout);
//    }
//}
//
void create_char_xml(string name, string filename) {
    string[] cmd = {"./char_wizard.pl", name, filename };
    system(cmd);
}

struct Mask {
    path[] p;
    string[] fill;
}

struct Glyph {
    static file fout;

    string name;
    string glyph_name;
    string key;
    string desc;
    pair dz;
    real ascent;
    path[] paths;
    path[] clip_paths;
    path[] mask;
    //Mask[] masks;
    bool mark = false;
    bool space = false;
    bool newline = false;

    //static Glyph Glyph(string name, string key, string desc = "", pair dz(path[] p), real ascent, path[] keyword clip_paths ... path[] paths) {
    static Glyph Glyph(
        string name,
        string key,
        string desc = "",
        pair dz(path[] p),
        real ascent
        ... path[] paths,
        path[] keyword clip_paths = {},
        path[] keyword mask = {},
        string keyword glyph_name = ""
        //Mask[] keyword mask = {}
    ) {
        Glyph g = new Glyph;
        g.name = name;
        g.glyph_name = glyph_name;
        g.key = key;
        g.ascent = ascent;
        g.dz = yscale(-1) * dz(paths);
        g.space = (g.name == "Space");
        g.newline = (g.name == "Newline");
        for (path p : paths) {
            g.paths.append(yscale(-1) * p);
        }
        for (path p : clip_paths) {
            g.clip_paths.append(yscale(-1) * p);
        }
        for (path p : mask) {
        //for (Mask m : mask) {
            g.mask.append(yscale(-1) * p);
            //g.mask.append(new Mask(yscale(-1) * m.p, m.fill));
        }
        return g;
    }

    void writeln(string s = '') {
        write(this.fout, s + '\n');
    }

    static Glyph Position(string name, string key, pair dz) {
        Glyph g = new Glyph;
        g.name = name;
        g.key = key;
        g.ascent = 0;
        g.dz = dz;
        return g;
    }

    static Glyph[] Ligature(
        string[] names,
        string[] keys,
        tailfunc[] dzs,
        real[] ascents
        ... path[] paths
    ) {
        Glyph[] gs;
        return gs;
    }

    void export(string filename = "", bool3 update = default, file dict_fout = null) {
        real left = realMax;
        real right = realMin;
        real top = realMin;;
        real bottom = realMax;

        if (this.paths.length == 0) {
            left = 0;
            right = 0;
            top = 0;
            bottom = 0;
        } else {
            for (path p : this.paths) {
                pair pos_min = min(p);
                pair pos_max = max(p);
                if (pos_min.x < left) {
                    left = pos_min.x;
                }
                if (pos_max.x > right) {
                    right = pos_max.x;
                }

                if (pos_min.y < bottom) {
                    bottom = pos_min.y;
                }
                if (pos_max.y > top) {
                    top = pos_max.y;
                }
            }
        }

        string g = "";
        g += '<glyph key="' + this.key + '" name="' + this.name + '" ' + (this.space ? 'space="true"' : '') + '\n';
        g += '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n';
        g += '  xmlns:xi="http://www.w3.org/2001/XInclude"\n';
        g += '  xsi:noNamespaceSchemaLocation="glyph.xsd">\n';
        g += '  <bbox>\n';
        g += '    <left>'   + format('%f', left) + '</left>\n';
        g += '    <right>'  + format('%f', right) + '</right>\n';
        g += '    <top>'    + format('%f', top) + '</top>\n';
        g += '    <bottom>' + format('%f', -bottom) + '</bottom>\n';
        g += '  </bbox>\n';
        g += '  <dx>' + format('%f', this.dz.x) + '</dx>\n';
        g += '  <dy>' + format('%f', this.dz.y) + '</dy>\n';
        g += '  <ascent>' + format('%f', this.ascent) + '</ascent>\n';

        if (this.paths.length == 0) {
            g += '  <path d="M0 0" />\n';
        } else {
            for (path p : this.paths) {
                string svg_path = path2svgpath(p);
                real path_length = arclength(p);
                g += '  <path d="' + svg_path + '" pathLength="' + format('%f', path_length) + '" />\n';
            }
        }

        g += '</glyph>\n';

        if (filename == "") {
            filename = "waseda_" + lc(this.name) + "_glyphs_asy.xml";
        }

        if (this.key == "default") {
            create_char_xml(this.name, "waseda_" + lc(this.name) + ".xml");
        }

        if (update == default) {
            update = this.key != "default";
        }

        file fout = output(filename, update = update);
        write(fout, g);
        close(fout);
    }

    Glyph toml(file fout = null) {
        //this.fout = fout;

        real left = realMax;
        real right = realMin;
        real top = realMin;;
        real bottom = realMax;

        if (this.paths.length == 0) {
            left = 0;
            right = 0;
            top = 0;
            bottom = 0;
        } else {
            for (path p : this.paths) {
                pair pos_min = min(p);
                pair pos_max = max(p);
                if (pos_min.x < left) {
                    left = pos_min.x;
                }
                if (pos_max.x > right) {
                    right = pos_max.x;
                }

                if (pos_min.y < bottom) {
                    bottom = pos_min.y;
                }
                if (pos_max.y > top) {
                    top = pos_max.y;
                }
            }
        }

        string node = 'waseda.character' + '.' + this.name;
        string g = "";

        if (this.key == "default") {
            writeln('[' + node + ']');
            writeln('mark = ' + (this.mark ? 'true' : 'false'));
            writeln('space = ' + (this.space ? 'true' : 'false'));
            writeln('newline = ' + (this.newline ? 'true' : 'false'));
            //writeln('description =' + this.description);
            writeln();
        }
        writeln('[[' + node + '.glyph]]');
        writeln('key = "' + this.key + '"');
        if (this.glyph_name != "") {
            writeln('name = "' + this.glyph_name + '"');
        }
        writeln('left = ' + format('%f', left));
        writeln('right = ' + format('%f', right));
        writeln('top = ' + format('%f', bottom));
        writeln('bottom = ' + format('%f', top));
        writeln('dx = ' + format('%f', dz.x));
        writeln('dy = ' + format('%f', dz.y));
        writeln('ascent = ' + format('%f', ascent));
        writeln();

        if (this.paths.length == 0) {
            writeln('[[' + node + '.glyph.path]]');
            writeln('d = "M0 0"');
            writeln('length = 0');
            writeln();
        } else {
            for (path p : this.paths) {
                string svg_path = path2svgpath(p);
                real path_length = arclength(p);
                writeln('[[' + node + '.glyph.path]]');
                writeln('d = "' + svg_path + '"');
                writeln('length = ' + format('%f', path_length));
                writeln();
            }
        }
        for (path p : this.clip_paths) {
            string svg_path = path2svgpath(p);
            real path_length = arclength(p);
            writeln('[[' + node + '.glyph.clip_path]]');
            writeln('d = "' + svg_path + '"');
            writeln();
        }
        for (path p : this.mask) {
            string svg_path = path2svgpath(p);
            //string svg_path = path2svgpath(m.p);
            //real path_length = arclength(p);
            writeln('[[' + node + '.glyph.mask]]');
            writeln('d = "' + svg_path + '"');
            //writeln('d = "' + svg_path + '"');
            //writeln('fill = "' + m.fill + '"');
            writeln();
        }
        
        if (this.key == 'default') {
            string name = lc(this.name);
            string char = this.name;
            writeln('[waseda.groups.' + name + '.' + char + ']');
            writeln();
        }

        return this;
    }

    Glyph dict(...string[] words) {
        if (this.fout != null) {
            if (words.length == 1) {
                writeln('[waseda.dictionary."' + words[0] + '"]');
                writeln('chars = ["' + this.name + '"]');
                writeln();
            } else if (words.length >= 2) {
                writeln('[waseda.dictionary."' + words[0] + '"]');
                writeln('chars = [');
                for (int i = 1; i < words.length; i += 1) {
                    writeln('    "' + words[i] + '",');
                }
                writeln("]");
            }
        }

        return this;
    }

    Glyph group(string name = "", string char = "") {
        if (name == "") name = lc(this.name);
        if (char == "") char = this.name;
        if (this.fout != null) {
            writeln('[waseda.groups.' + name + '.' + char +']');
            writeln();
        }
        
        return this;
    }
}
