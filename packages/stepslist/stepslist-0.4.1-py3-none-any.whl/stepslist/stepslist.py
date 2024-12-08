import re
import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree

class StepsBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^ *!== steps *\n'  # start line, e.g., `   !== steps `
    RE_FENCE_END = r'\n *==! *$'           # last non-blank line, e.g., '==!'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        steps = []
        try:
            # Find block with ending fence
            for block_num, block in enumerate(blocks):
                if re.search(self.RE_FENCE_END, block):
                    # remove fence
                    blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                    # Process steps
                    for line in blocks[0:block_num]:
                        match = re.match(r'^\s*(\d+)\.\s*(.*)', line)
                        if match:
                            steps.append(f"<li>{match.group(2).strip()}</li>")
                    # Create ordered list
                    if steps:
                        ol = etree.SubElement(parent, 'ol', {'class': 'md-steps'})
                        for step in steps:
                            ol.append(etree.fromstring(step))
                    # Remove used blocks
                    for i in range(0, block_num + 1):
                        blocks.pop(0)
                    return True
            # No closing marker! Restore and do nothing
            blocks[0] = original_block
            return False
        except Exception as e:
            print(f"An error occurred while processing blocks: {e}")
            # Restore original block in case of error
            blocks[0] = original_block
            return False

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(StepsBlockProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Example usage
if __name__ == "__main__":
    import markdown

    text = """!== steps
1. Step 1
2. Step 2
==!"""

    md = markdown.Markdown(extensions=[StepsExtension()])
    html_output = md.convert(text)
    print(html_output)