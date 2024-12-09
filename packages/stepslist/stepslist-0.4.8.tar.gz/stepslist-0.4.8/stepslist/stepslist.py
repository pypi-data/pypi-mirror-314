import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import Postprocessor
import xml.etree.ElementTree as etree
import re

class StepsProcessor(BlockProcessor):
    def test(self, parent, block):
        return block.startswith("<steps>")

    def run(self, parent, blocks):
        # Get the entire block
        block = blocks.pop(0)

        # Remove <steps> and </steps>
        content = re.sub(r"<steps>(.*?)</steps>", r"\1", block, flags=re.DOTALL).strip()

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
        md.postprocessors.register(StepsPostProcessor(), 'steps_post', 15)

class StepsPostProcessor(markdown.postprocessors.PostProcessor):
    def run(self, text):
        # Remove any remaining <steps> and </steps> tags
        return re.sub(r'<steps>|</steps>', '', text)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
<steps>

1. ### Step one:

    Lorem ipsum odor amet, consectetuer adipiscing elit. Ipsum aptent pharetra nostra vestibulum inceptos. Ornare sagittis praesent tellus potenti, aptent habitant efficitur dictum. Massa eget parturient fringilla ac aenean velit 
    
    1. 
        consectetur. _Fringilla faucibus enim risus a aliquet_. Penatibus gravida feugiat dui nullam placerat nam. Molestie curabitur himenaeos mattis fusce per mollis fusce. Facilisis facilisis neque elit class id elit tellus.

    2. 
        Text can be {--deleted--} and replacement text {++added++}. This can also be
        combined into {~~one~>a single~~} operation. {==Highlighting==} is also
        possible {>>and comments can be added inline<<}.

2. ### Step two:

    Sollicitudin ante senectus molestie taciti consequat arcu ipsum. Lectus posuere varius mi metus, nascetur ac scelerisque gravida. Sociosqu sagittis maximus aliquam; tempor a eget tristique. Ultrices eros hendrerit posuere litora maximus elementum, platea dolor. Iaculis aptent ut malesuada netus platea mollis natoque. 
    
    ```
    Magnis dictum risus netus ad suscipit duis dictum luctus. Tempus sapien neque ante nibh litora sem posuere. Accumsan magnis netus nec erat lectus.
    ```

3. ### Step three

    Dapibus **fringilla semper vitae elit** mattis suspendisse molestie class. Et tortor sed lacus molestie lorem consectetur aenean. Primis id ridiculus vehicula dignissim, sit semper non sociosqu. Scelerisque ut egestas natoque aenean cubilia. Iaculis vel `congue est nibh enim risus` vehicula. Penatibus congue `#!python for line in content.splitlines():` sed tincidunt neque. Erat congue at aliquam turpis ut elit turpis dignissim.

</steps>
"""

    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)
