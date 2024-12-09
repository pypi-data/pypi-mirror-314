import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class StepsProcessor(BlockProcessor):
    def test(self, parent, block):
        # Check if the block starts with --steps-- on a new line
        return block.startswith("--steps--\n")

    def run(self, parent, blocks):
        # Get the entire block
        block = blocks.pop(0)

        # Check for the closing block --!steps-- on a new line
        if not block.endswith("--!steps--"):
            return  # Do nothing if --!steps-- is not present

        # Remove --steps-- and --!steps--
        content = re.sub(r"--steps--\n(.*?)\n--!steps--", r"\1", block, flags=re.DOTALL).strip()

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