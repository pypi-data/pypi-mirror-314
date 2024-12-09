"""
SepsList.

Use custom Fencing blocks to create a custom ordered list.
"""
import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class BoxBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^--steps-- \n' # start line, e.g., `--steps--`
    RE_FENCE_END = r'\n--!steps--\s*$'  # last non-blank line, e.g, '--!steps--\n'

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
                # Render fenced area inside a new ordered list
                e = etree.SubElement(parent, 'ol', {'class': 'md-steps'})
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                # Remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # Indicate successful processing
        # No closing marker! Restore and do nothing
        blocks[0] = original_block
        return False  # Indicate failure to process

class BoxExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), 'box', 175)

def makeExtension(**kwargs):
    return BoxExtension(**kwargs)