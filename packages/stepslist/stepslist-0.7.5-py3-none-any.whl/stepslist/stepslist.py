import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class BoxBlockProcessor(BlockProcessor):
    # Regular expressions to identify the start and end of the step block
    RE_FENCE_START = r'^--steps--\s*$'
    RE_FENCE_END = r'^\s*--!steps--\s*$'

    def test(self, parent, block):
        # Check if the current block matches the start marker
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        # Store the original block for restoration if needed
        original_block = blocks[0]
        # Remove the start marker from the block
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0]).strip()

        # Iterate through the blocks to find the end marker
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # Remove the end marker from the block
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block).strip()
                # Create a new div element for the step block
                e = etree.SubElement(parent, 'div')
                e.set('class', 'md-steps')
                # Parse the blocks between the start and end markers
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                # Remove the processed blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # Successfully processed the block
        # If no closing marker is found, restore the original block
        blocks[0] = original_block
        return False  # Indicate that the block was not processed

class BoxExtension(Extension):
    def extendMarkdown(self, md):
        # Register the BoxBlockProcessor with the Markdown parser
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), 'box', 175)

def makeExtension(**kwargs):
    # Function to create an instance of the BoxExtension
    return BoxExtension(**kwargs)