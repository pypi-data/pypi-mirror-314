import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.postprocessors import Postprocessor
import xml.etree.ElementTree as etree

class StepsInlineProcessor(Pattern):
    def handleMatch(self, m):
        steps_content = m.group(3)
        ol = etree.Element('ol', {'class': 'md-steps'})
        
        # Process each line in the steps content
        for line in steps_content.strip().splitlines():
            line = line.strip()
            if line:  # Check for non-empty lines
                # Match lines starting with a digit followed by a period
                if line[0].isdigit() and line[1] == '.':
                    li = etree.Element('li')
                    li.text = line[2:].strip()  # Remove the digit and period
                    ol.append(li)
        
        return ol, m.start(0), m.end(0)

class StepsPostProcessor(Postprocessor):
    def run(self, text):
        # Remove remaining <steps> and </steps> tags
        return text.replace('<steps>', '').replace('</steps>', '')

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.add('steps', StepsInlineProcessor(r'<steps>(.*?)</steps>', md), '<not_strong')
        md.postprocessors.register(StepsPostProcessor(), 'remove_steps', 15)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
<steps>

1. Add a default (fallback) email address to `config/_default/params.toml`:
2. Add the following CSS to `assets/scss/common/_custom.scss`:
3. Create shortcode file `layouts/shortcodes/email.html` with the following content:

</steps>
"""

    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)