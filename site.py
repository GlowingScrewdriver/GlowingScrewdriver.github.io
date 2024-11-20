#!/bin/env python3

import xml.etree.ElementTree as ET
from os import listdir
from marko.ext.gfm import gfm
from argparse import ArgumentParser
from copy import copy
from io import BytesIO

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
        the content element of the template, and write the template to `dst`.
        Title of the page is returned.
        """
        if isinstance (src, str):
            content_str = src
        else:
            content_str = src.read ()

        content = ET.fromstring ("<div>" + gfm(content_str) + "</div>")
        title = content.find ("h1").text # First <h1> is taken to hold the page title.
        self.template_content.extend (content)
        dst.write (ET.tostring (self.template))
        self.template_content.clear ()
        return title

    def gen_pages (self, index_filename = "index.html", pagenames = None):
        """
        Generate site pages (HTML) from all page sources (Markdown).
        Also outputs a site index
        """
        site_index = []  # [(Title, path) ... ]
        if pagenames is None: pagenames = self.pages
        for pagename in pagenames:
            src = open (f"{self.pages_dir}/{pagename}.md")
            dst = open (f"{self.site_dir}/{pagename}.html", "wb")
            title = self.apply_template (src, dst)
            site_index.append ((title, f"{pagename}.html"))
            src.close ()
            dst.close ()

        index_page = "# Blog posts\n" + "\n".join((
            f"* [{title}]({path})"
            for title, path in site_index
        ))
        with open (f"{self.site_dir}/{index_filename}", "wb") as index_file:
            self.apply_template (index_page, index_file)

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
