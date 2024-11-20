#!/bin/env python3

import xml.etree.ElementTree as ET
from os import listdir
from marko.ext.gfm import gfm
from argparse import ArgumentParser
from copy import copy

class SiteGenerator:
    def __init__ (self, template_filename: str, pages_dir: str, site_dir: str):
        # Get the list of pages present
        self.pages = (p [:-3] for p in listdir (pages_dir) if p.endswith (".md"))
        self.pages_dir = pages_dir
        self.site_dir = site_dir

        # Set up the template
        with open (template_filename) as tf:
            self.template = ET.fromstring (tf.read ())
        # Find <content /> element and refactor to <div />.
        # This is the "content element" of the template.
        self.template_content = None
        for elem in self.template.iter ():
            if elem.attrib.get ("id") == "content":
                self.template_content = elem
        assert self.template_content is not None, f"Please include a `#content` element in {template_filename}"


    def apply_template (self, src, dst):
        """
        Convert a the markdown from `src` to HTML, insert it into
        the content element of the template, and write the template to `dst`
        """
        content = ET.fromstring ("<div>" + gfm(src.read ()) + "</div>")
        self.template_content.extend (content)
        dst.write (ET.tostring (self.template))
        self.template_content.clear ()


    def gen_pages (self, pagenames = None):
        if pagenames is None: pagenames = self.pages
        for pagename in pagenames:
            src = open (f"{self.pages_dir}/{pagename}.md")
            dst = open (f"{self.site_dir}/{pagename}.html", "wb")
            self.apply_template (src, dst)
            src.close ()
            dst.close ()


def gen_site (pages_dir, site_dir, template_file):
    with open (template_file) as template_f:
        template_xml = template_f.read ()

    for page in listdir (pages_dir):
        if page.endswith (".md"):
            src = f"{pages_dir}/{page}"
            dst = f"{site_dir}/{page [:-3]}.html"
            with open (src) as src_f:
                content = gen_page (src_f.read (), template_xml)
            with open (dst, "wb") as dst_f:
                dst_f.write (content)

if __name__ == "__main__":
    # parser = ArgumentParser ()
    # parser.add_argument ("--pages_dir", default = "pages")
    # parser.add_argument ("--site_dir", default = "site")
    # parser.add_argument ("--template_file", default = "template.html")
    #
    # args = parser.parse_args ()
    # gen_site (args.pages_dir, args.site_dir, args.template_file)

    gen = SiteGenerator ("template.html", "pages", "site")
    gen.gen_pages ()
