from text_parser import parse_text
#from more_itertools import ( pairwise, split_after, partitions)
import math
import logging
import random
from character import Character


logger = logging.getLogger(__name__)

def split_after(iterable, pred):
    buf = []
    for item in iterable:
        buf.append(item)
        if pred(item):
            yield buf
            buf = []
    if buf:
        yield buf

def pairwise(iterable):
    iterator = iter(iterable)
    a = next(iterator, None)

    for b in iterator:
        yield a, b
        a = b

class Context:
    def __init__(self, x=0, y=0, ref_line=0, right=0, margin=5):
        self.x = x
        self.y = y
        self.ref_line = ref_line
        self.right = right
        self.margin = margin

class Line:
    def __init__(self, chars=None):
        self.chars = chars if chars else []

    @property
    def clauses(self):
        return split_after(self.chars, lambda c: c.is_space)

class Bbox:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.width = right - left
        self.height = bottom - top

    def __mul__(self, scale):
        return Bbox(
            self.left * scale,
            self.right * scale,
            self.top * scale,
            self.bottom * scale,
        )

    def __str__(self):
        return f"{self.left} {self.top} {self.width} {self.height}"

class String:
    def __init__(self, text, sh=None):
        self.text = text
        self.sh = sh
        self.chars = self.get_chars(text)
        self.connect()
        self.select_glyphs()
        bbox = self.layout()
        self.svg_template = f"""<svg
            id="svg_root"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            version="1.1"
            viewBox="{bbox}"
            width="{bbox.width}mm"
            height="{bbox.height}mm"
            preserveAspectRatio="xMinYMin meet"
            data-text=""
            transform="scale(1 1)"
            transform-origin="0 0"
            style="fill: none; stroke: rgb(0, 0, 0); stroke-width: 0.425197; stroke-linecap: round; stroke-linejoin: round; stroke-miterlimit: 4; stroke-opacity: 1; background-color: #f0e68c;" >
            <rect x="{bbox.left}" y="{bbox.top}" width="100%" height="100%" fill="rgb(255 255 255)" />
            {{}}</svg>"""

    #def get_chars(self, text):
    #    chars = []
    #    for word in parse_text(text):
    #        for parts in partitions(word):
    #            subwords = ["".join(part) for part in parts]
    #            if all([subword in self.sh.dictionary for subword in subwords]):
    #                for subword in subwords:
    #                    for char_name in self.sh.dictionary[subword]:
    #                        chars.append(Character(char_name, self.sh))
    #                break
    #        else:
    #            chars.append(Character('Null', self.sh))
    #    return chars
    def get_chars(self, text):
        chars = []
        for word in parse_text(text, self.sh['dictionary']):

            chars.append(Character(word, self.sh))
        return chars

    def connect(self):
        base = None
        idx = 0
        for char in self.chars:
            char.prev = base
            if char.is_marker:
                continue
            elif base:
                base.next = char
            base = char
            char.idx = idx

    def __str__(self):
        return self.create_path_elements()[0]

    def __repr__(self):
        return f"String({'self.text'})"

    def __split(self):
        return [Line(char_list) for char_list in split_after(self.chars, lambda c: c.is_newline)]

    def set_position(self, cntx, char):
        if char.prev is None:
            cntx.x = max(cntx.right - char.left, 0)
            cntx.y = max(cntx.ref_line - char.ascent, 0)

        char.set_pos(cntx.x, cntx.y)
        if char.is_space:
            try:
                cntx.x = cntx.right + char.dx - char.next.left
            except (IndexError, AttributeError):
                cntx.x += char.dx
            try:
                cntx.y = cntx.ref_line + char.dy - char.next.ascent
            except (IndexError, AttributeError):
                cntx.y = cntx.ref_line + char.dy
            cntx.right = cntx.x
        elif char.is_newline:
            try:
                cntx.right = cntx.margin - char.next.left
            except (IndexError, AttributeError):
                pass
            cntx.ref_line += char.dy
            cntx.x = cntx.right
            try:
                cntx.y = cntx.ref_line - char.next.ascent
            except (IndexError, AttributeError):
                cntx.y = cntx.ref_line

        elif char.is_marker:
            try:
                char.set_pos(char.prev.x, char.prev.y)
            except AttributeError:
                pass
        else:
            cntx.x, cntx.y = char.exit
            cntx.right = max(cntx.right, char.x + char.right)

    def correct_left_and_top(self, lines, margin=5):
        for line in lines:
            left_min = min([char.x + char.left for char in line.chars])
            xoffset = margin - left_min if left_min < 0 else 0
            for char in line.chars:
                char.set_pos(char.x + xoffset, char.y)

        top_min = min([char.y + char.top for char in self.chars])
        yoffset = margin - top_min if top_min < 0 else 0
        for char in self.chars:
            char.set_pos(char.x, char.y + yoffset)

    def correct_inter_line(self, lines, margin=5):
        for upper_line, lower_line in pairwise(lines):
            bottom = max([char.y + char.bottom for char in upper_line.chars], default=0)
            top = min([char.y + char.top for char in lower_line.chars], default=bottom)
            if bottom <= top:
                continue
            yoffset = bottom - top + margin
            for char in lower_line.chars:
                char.set_pos(char.x, char.y + yoffset)

    def correct_inter_clause(self, lines, margin=0):
        for line in lines:
            for left_clause, right_clause in pairwise(line.clauses):
                left_clause_right = max([char.x + char.right for char in left_clause], default=0)
                right_clause_left = min([char.x + char.left for char in right_clause], default=left_clause_right)
                if left_clause_right <= right_clause_left:
                    continue
                xoffset = left_clause_right - right_clause_left + margin
                for char in right_clause:
                    char.set_pos(char.x + xoffset, char.y)

    def layout(self, right=5, ref_line=20, margin=5):
        if len(self.chars) == 0:
            return BBox(0, 0, 0, 0)

        cntx = Context(ref_line=ref_line, right=right)

        for char in self.chars:
            self.set_position(cntx, char)

        lines = self.__split()
        self.correct_inter_line(lines, margin=margin)
        self.correct_inter_clause(lines, margin=0)
        self.correct_left_and_top(lines, margin=margin)

        left = math.floor(min([char.x + char.left for char in self.chars])) - margin
        right = math.ceil(max([char.x + char.right for char in self.chars])) + margin
        top = math.floor(min([char.y + char.top for char in self.chars])) - margin
        bottom = math.ceil(max([char.y + char.bottom for char in self.chars])) + margin

        return Bbox(left, right, top, bottom)

    def create_svg(self, to_animate=False, speed_mm_per_s=20, to_generate_keyframe=False, target_s=0):
        marker_buf = []
        char_buf = []
        for char in self.chars:
            if char.is_marker:
                marker_buf.append(char)
            elif char.is_space or char.is_newline:
                char_buf.append(char)
                char_buf.extend(marker_buf)
                marker_buf = []
            else:
                char_buf.append(char)
        char_buf.extend(marker_buf)

        paths = []
        time_s = 0
        for char in char_buf:
            elem, time_s = char.create_path_element(time_s=time_s, to_animate=to_animate, speed_mm_per_s=speed_mm_per_s, to_generate_keyframe=to_generate_keyframe, target_s=target_s)
            #if char.is_space:
            #    time_s += 0.01
            #elif char.is_newline:
            #    time_s += 0.1
            #elif char.is_marker:
            #    time_s += 0.1
            paths.append(elem)

        return self.svg_template.format("".join(paths)), time_s

    def create_key_frames(self, speed_mm_per_s=20, framerate=24):
        total_length = sum((length for c in self.chars for length in c.lengths))
        total_time_s = total_length / speed_mm_per_s
        total_frames = math.ceil(framerate * total_time_s)
        frames = []
        for frame_num in range(total_frames + 4):
            time_s = frame_num * total_time_s / total_frames 
            frames.append(self.create_svg(to_animate=False, speed_mm_per_s=speed_mm_per_s, to_generate_keyframe=True, target_s=time_s)[0])
        return frames

    def select_glyphs(self):
        char_names = [char.name for char in self.chars]
        new_char_names = [char.select_glyph() for char in self.chars]
        count = 0

        while new_char_names != char_names:
            char_names = new_char_names
            new_char_names = [char.select_glyph() for char in self.chars]
            assert count < 10, "Too many iterations in select_glyphs()"
            count += 1

