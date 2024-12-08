import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class StepsBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^ *!== steps *\n'  # start line, e.g., `!== steps`
    RE_FENCE_END = r'\n *==!\s*$'         # end line, e.g., `==!`

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                # render fenced area inside an ordered list
                ol = etree.SubElement(parent, 'ol')
                ol.set('class', 'md-steps')
                for line in blocks[0:block_num + 1]:
                    match = re.match(r'^\s*\d+\.\s+(.*)', line)
                    if match:
                        li = etree.SubElement(ol, 'li')
                        li.text = match.group(1)
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True
        # No closing marker! Restore and do nothing
        blocks[0] = original_block
        return False

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(StepsBlockProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
!== steps

    1. Step 1

    2. Step 2

==!
"""
    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)