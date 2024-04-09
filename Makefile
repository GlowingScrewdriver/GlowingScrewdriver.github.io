# Markdown files
MD_FILES := $(basename $(wildcard *.md))
MD_TARGETS := $(addprefix site/, $(addsuffix .html, $(MD_FILES)))

# Generated files, from custom generator programs
GEN_FILES := $(basename $(wildcard *.gen))
GEN_TARGETS := $(addprefix site/, $(addsuffix .html, $(GEN_FILES)))

.PHONY: site
site: $(MD_TARGETS) $(GEN_TARGETS) site/global.css

$(MD_TARGETS): site/%.html: %.md markdown_w
	markdown_w < $< > $@

$(GEN_TARGETS): site/%.html: %.gen markdown_w
	$</gen | markdown_w > $@

site/global.css: global.css
	cp global.css site/global.css

clean:
	rm -rf site/*
