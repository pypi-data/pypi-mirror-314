import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class StepsBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^ *!== steps *\n'  # Start line, e.g., `!== steps`
    RE_FENCE_END = r'\n *==!\s*$'         # End line, e.g., `==!`

    def test(self, parent, block):
        """Test if the block starts with the steps marker."""
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        """Process the block and convert it into an ordered list."""
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # Remove end fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)

                # Create an ordered list element
                ol = etree.SubElement(parent, 'ol')
                ol.set('class', 'md-steps')

                # Process each line in the block
                for line in blocks[0:block_num + 1]:
                    line = line.strip()
                    if re.match(r'^\d+\.\s', line):
                        # Create a list item for lines starting with a number and dot
                        li = etree.SubElement(ol, 'li')
                        li.text = line.split('.', 1)[1].strip()

                # Remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True

        # No closing marker! Restore and do nothing
        blocks[0] = original_block
        return False
    
class StepsExtension(Extension):
    def extendMarkdown(self, md):
        """Register the StepsBlockProcessor with the Markdown parser."""
        md.parser.blockprocessors.register(StepsBlockProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    """Return an instance of the StepsExtension."""
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
!=== steps

    1. Step one

    2. Ste two

==!
"""

    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)