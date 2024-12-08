import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class StepsProcessor(BlockProcessor):
    RE_START = r'^\[steps\]'
    RE_END = r'^\[/steps\]'

    def test(self, parent, block):
        # Check if the block starts with [steps] and ends with [/steps]
        return re.match(self.RE_START, block) and block.strip().endswith('[/steps]')

    def run(self, parent, blocks):
        # Get the entire block
        block = blocks.pop(0)

        # Remove [steps] and [/steps]
        content = re.sub(r"\[steps\](.*?)\[/steps\]", r"\1", block, flags=re.DOTALL).strip()

        # Create an ordered list with class "md-steps"
        ol = etree.Element('ol')
        ol.set('class', 'md-steps')

        # Split content into lines and create list items
        for line in content.splitlines():
            line = line.strip()
            if line:  # Only create <li> if the line is not empty
                li = etree.SubElement(ol, 'li')
                # If the line starts with a number (indicating it's a step), treat it as HTML
                if line[0].isdigit():
                    li.text = line
                else:
                    # If it's not a step line, consider it as a paragraph
                    p = etree.SubElement(li, 'p')
                    p.text = line

        # Append the ordered list to the parent
        parent.append(ol)

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(StepsProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
[steps]

1. Add a default (fallback) email address to `config/_default/params.toml`:

    ```toml title="params.toml"
    # defaultEmail
    defaultEmail = "email@example.com"
    ```

2. Add the following CSS to `assets/scss/common/_custom.scss`:

    ```scss title="_custom.scss"
    span.email b {
      display: none;
    }
    ```

3. Create shortcode file `layouts/shortcodes/email.html` with the following content:

    ```html title="email.html"
    {{- /* Set defaults and get args. */}}
    {{- $address := index .Params 0 | default site.Params.defaultEmail }}

    {{- /* Get parts. */}}
    {{- $addressParts := split $address "@" }}
    {{- $userName := (index $addressParts 0) }}
    {{- $rootDomain := (index $addressParts 1) }}
    {{- $rootDomainParts := split $rootDomain "." }}
    {{- $domainName := (index $rootDomainParts 0) }}
    {{- $topLevelDomain := (index $rootDomainParts 1) }}

    {{- /* Render. */}}
    <span class="email">
      {{- printf "%s@%s<b>.%s</b>.%s" $userName $domainName $domainName $topLevelDomain | safeHTML -}}
    </span>
    ```

    The shortcode gets the email address you provided — using the default email address if you didn’t specify one. Next, it splits the email address in parts — `userName`, `domainName`, and `topLevelDomain` — and renders the HTML.

[/steps]
"""

    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)
