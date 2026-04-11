SRC = data
DST = src

PY += $(DST)/glyph_selector_lark.py
PY += $(DST)/path_expression_lark.py
PY += $(DST)/text_grammer_lark.py

LARK = python3 -m lark.tools.standalone --maybe_placeholders

all: $(PY)

$(DST)/%_lark.py: $(SRC)/%.lark
	$(LARK) $< > $@

.PHONY: all
