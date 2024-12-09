import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class BoxBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^ *!!!! Steps *\n'  # start line, e.g., `!!!! Steps`
    RE_FENCE_END = r'\n *!!!!\s*$'          # last non-blank line, e.g., '!!!!'

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
                
                # Create ordered list with class "md-steps"
                ol = etree.SubElement(parent, 'ol')
                ol.set('class', 'md-steps')

                # Process each line in the blocks to create list items
                for line in blocks[0:block_num]:
                    line = line.strip()
                    if re.match(r'^\d+\.\s', line):  # Check if line starts with a number and a period
                        li = etree.SubElement(ol, 'li')
                        p = etree.SubElement(li, 'p')
                        p.text = line[2:]  # Add text after the number and period

                # Remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # Successfully processed the block

        # No closing marker! Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), 'box', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
!!!! Steps

1. 
  consectetur. Fringilla faucibus enim risus a aliquet. Penatibus gravida feugiat dui nullam placerat nam. Molestie curabitur himenaeos mattis fusce per mollis fusce. Facilisis facilisis neque elit class id elit tellus.

2. 
  fringilla semper vitae elit mattis suspendisse molestie class. Et tortor sed lacus molestie lorem consectetur aenean. Primis id ridiculus vehicula dignissim, sit semper non sociosqu. Scelerisque ut egestas natoqu

!!!!
"""

    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)
