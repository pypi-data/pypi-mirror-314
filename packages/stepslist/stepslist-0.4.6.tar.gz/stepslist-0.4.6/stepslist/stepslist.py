from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import markdown

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        in_steps = False
        new_lines = []

        for line in lines:
            if line.strip() == '<steps>':
                in_steps = True
                new_lines.append('<ol class="md-steps">')
            elif line.strip() == '</steps>':
                in_steps = False
                new_lines.append('</ol>')
            elif in_steps:
                # Check for numbered list items (1., 2., etc.)
                if line.strip().startswith(tuple(str(i) + '.' for i in range(1, 10))):
                    # Strip the number with period
                    content = line.strip().split('.', 1)[1].strip()
                    new_lines.append('<li>' + content + '</li>')
                elif line:  # Non-empty line
                    line = f'<p>{line}</p>'  # Wrap paragraph in <p>
                else:  # Empty line
                    line = ''  # Keep empty lines as is
                new_lines.append(line)
            else:
                new_lines.append(line)

        return new_lines

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'steps', 175)

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