## Overview of the Build System

This is the build system for GlowingScrewdriver's Blog. The build is orchestrated
by the Makefile alone, and has minimal dependencies. Care has been taken to use
standardized tools, such as POSIX versions of `awk` and `sh`

All output files are written to site/.

The following types of files are currently processed:
* `<page>.md`: contents piped to `markdown_w` and written to `site/<page>.html`
* `<page>.gen`: output of `<page>.gen/gen` is piped to `markdown_w` and written to `site/<page>.html`

Noteworthy files:
* `markdown_w`: a wrapper around markdown for tasks like setting the document title and linking the stylesheet.
* `index.gen`: generates a landing page that includes a listing of present blog posts.
* `global.css`: common stylesheet for all pages, and is currently the only CSS used throughout the project.
