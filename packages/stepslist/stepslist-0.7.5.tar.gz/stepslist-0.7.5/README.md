<div align="center">

StepsList
=========================================

[![PyPI](https://img.shields.io/pypi/v/stepslist)](https://pypi.org/project/stepslist/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stepslist)
[![License](https://img.shields.io/github/license/a3bagged/stepslist-extension)](https://github.com/A3Bagged/stepslist-extension/blob/main/LICENSE.md)


**Extension for [Python-Markdown](https://python-markdown.github.io/): to be used on [Mkdocs](https://github.com/mkdocs/mkdocs) and [Material for Mkdocs](https://github.com/squidfunk/mkdocs-material)**


This Python package provides a custom Markdown extension that allows users to define step blocks in their Markdown documents. The extension recognizes specific markers and formats the enclosed content for better readability.

</div>

## Features
- Define step blocks using `--steps--` and `--!steps--` markers.
- Automatically wraps the content in a `<div>` with a class for custom styling.
- Easy integration with the existing Markdown parser.

## Installation
To use this extension, ensure you have the markdown library installed. You can install it using pip:
```bash
pip install markdown
```

You can install this package using pip:

```bash
pip install stepslist
```

## Usage
To use this extension, add it to your MkDocs configuration file (`mkdocs.yml`):

```
markdown_extensions:
  - stepslist
```
Now, you can use the `--steps--` `--!steps--` tag in your Markdown files:

> [!IMPORTANT]
> Note that you will need blank lines between the tags and your list otherwise it will not work!

### Markdown

```
--steps--

1. Step one
2. Step two
3. Step three

--!steps--
```
### Output example
This will be rendered as an ordered list within a div that you can style:

```
<div class="md-steps">
  <ol>
    <li>Step one</li>
    <li>Step two</li>
    <li>Step three</li>
  </ol>
</div>
```

### Styling
To style in `CSS` you need the following selectors:
You can also style the `::before` and `::after` pseudo elements.  
It's recommended to keep the `.md-steps` styling for the div itself unchanged unless you need to
```
.md-steps ol {
  /* Styling goes here */
}

.md-steps>ol>li {
  /* Styling goes here */
}

/* Optional */
.md-steps>ol>li::before {
  /* Styling goes here */
}

.md-steps>ol>li::after {
  /* Styling goes here */
}
```

<div align="center">

_If you like this extension consider buying me a :coffee:[coffee](https://ko-fi.com/cvanliere)._

</div>