import os
import markdown
import re
from pathlib import Path

def convert_mermaid_blocks(html_content):
    # Find all code blocks with language-mermaid class
    pattern = r'<pre><code class="language-mermaid">(.*?)</code></pre>'

    def replace_mermaid(match):
        # Extract the mermaid diagram content and decode HTML entities
        mermaid_content = match.group(1)
        mermaid_content = mermaid_content.replace('&quot;', '"')
        mermaid_content = mermaid_content.replace('&gt;', '>')
        mermaid_content = mermaid_content.replace('&lt;', '<')
        mermaid_content = mermaid_content.replace('&amp;', '&')
        # Create a div with mermaid class
        return f'<div class="mermaid">\n{mermaid_content}\n</div>'

    # Replace all mermaid code blocks
    return re.sub(pattern, replace_mermaid, html_content, flags=re.DOTALL)

def create_html_pages(input_dir):
    # Get list of markdown files
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    md_files.sort()  # Sort files to maintain order

    # CSS styles
    css = """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
        }
        .navigation {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        .nav-link {
            text-decoration: none;
            color: #0366d6;
        }
        .nav-link:hover {
            text-decoration: underline;
        }
        .mermaid {
            text-align: center;
            margin: 20px 0;
        }
    </style>
    """

    # Mermaid.js support
    mermaid_script = """
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
                flowchart: {
                    useMaxWidth: false,
                    htmlLabels: true
                },
                sequence: {
                    useMaxWidth: false,
                    htmlLabels: true,
                    diagramMarginX: 50,
                    diagramMarginY: 10,
                    boxMargin: 10
                }
            });
        });
    </script>
    """

    # Initialize markdown converter with extensions
    md = markdown.Markdown(extensions=['fenced_code', 'tables'])

    # Process each markdown file
    for i, md_file in enumerate(md_files):
        with open(os.path.join(input_dir, md_file), 'r', encoding='utf-8') as f:
            content = f.read()

        # Convert markdown to HTML
        html_content = md.convert(content)

        # Convert Mermaid code blocks to divs
        html_content = convert_mermaid_blocks(html_content)

        # Create navigation links
        prev_link = f'<a class="nav-link" href="{md_files[i-1].replace(".md", ".html")}">&larr; Previous</a>' if i > 0 else ''
        index_link = '<a class="nav-link" href="index.html">Index</a>' if md_file != 'index.md' else ''
        next_link = f'<a class="nav-link" href="{md_files[i+1].replace(".md", ".html")}">Next &rarr;</a>' if i < len(md_files)-1 else ''

        navigation = f"""
        <div class="navigation">
            {prev_link}
            {index_link}
            {next_link}
        </div>
        """

        # Combine everything into final HTML
        final_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{md_file.replace('.md', '').replace('_', ' ').title()}</title>
            {css}
            {mermaid_script}
        </head>
        <body>
            {navigation}
            {html_content}
            {navigation}
        </body>
        </html>
        """

        # Write HTML file
        html_filename = md_file.replace('.md', '.html')
        with open(os.path.join(input_dir, html_filename), 'w', encoding='utf-8') as f:
            f.write(final_html)

if __name__ == "__main__":
    # Get the absolute path to output/pf1
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'output' / 'pf1'

    print(f"Converting markdown files in: {input_dir}")
    create_html_pages(input_dir)
    print("Conversion complete! Open index.html in your browser to start reading.")
