import os
import re
from pathlib import Path
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
import markdown2

def create_html_pages(input_dir):
    # Get Pygments CSS
    pygments_css = HtmlFormatter().get_style_defs('.highlight')

    # Get list of markdown files
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    md_files.sort()  # Sort files to maintain order

    # Process each markdown file
    for i, md_file in enumerate(md_files):
        print(f"\n{'='*50}")
        print(f"Processing {md_file}...")

        file_path = os.path.join(input_dir, md_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Show preview of content
        print(f"First 100 chars of content: {content[:100]}")

        # Fix relative links to point to .html instead of .md
        content = re.sub(r'\]\((.*?)\.md\)', r'](\\1.html)', content)

        # Convert markdown to HTML using markdown2 with extras
        html_content = markdown2.markdown(content, extras=[
            'fenced-code-blocks',
            'tables',
            'code-friendly',
            'break-on-newline',
            'cuddled-lists',
            'markdown-in-html',
            'target-blank-links'
        ])

        print(f"First 100 chars of HTML: {html_content[:100]}")

        # CSS styles with improved code block styling
        css = f"""
        <style>
            {pygments_css}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                color: #24292e;
            }}
            pre {{
                background-color: #f6f8fa;
                padding: 16px;
                border-radius: 6px;
                overflow-x: auto;
                margin: 16px 0;
            }}
            code {{
                background-color: #f6f8fa;
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
                font-size: 85%;
            }}
            .navigation {{
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
                padding: 10px;
                background-color: #f6f8fa;
                border-radius: 6px;
                position: sticky;
                top: 0;
                z-index: 100;
                backdrop-filter: blur(10px);
            }}
            .nav-link {{
                text-decoration: none;
                color: #0366d6;
                padding: 5px 10px;
            }}
            .nav-link:hover {{
                text-decoration: underline;
                background-color: #f1f8ff;
                border-radius: 3px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 24px;
                margin-bottom: 16px;
                font-weight: 600;
                line-height: 1.25;
            }}
            .mermaid {{
                text-align: center;
                margin: 20px 0;
                background-color: white;
                padding: 10px;
                border-radius: 6px;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            blockquote {{
                padding: 0 1em;
                color: #6a737d;
                border-left: 0.25em solid #dfe2e5;
                margin: 0;
            }}
        </style>
        """

        # Mermaid.js support with dark mode detection
        mermaid_script = """
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

            // Configure mermaid
            mermaid.initialize({
                startOnLoad: true,
                theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'default',
                securityLevel: 'loose',
                flowchart: { useMaxWidth: false, htmlLabels: true },
                sequence: {
                    useMaxWidth: false,
                    htmlLabels: true,
                    diagramMarginX: 50,
                    diagramMarginY: 10,
                    boxMargin: 10
                }
            });

            // Listen for dark mode changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                mermaid.initialize({
                    theme: e.matches ? 'dark' : 'default'
                });
            });
        </script>
        """

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
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="color-scheme" content="light dark">
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
        output_path = os.path.join(input_dir, html_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Written to {output_path}")

if __name__ == "__main__":
    # Get the absolute path to output/pf1
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'output' / 'pf1'

    print(f"\nConverting markdown files in: {input_dir}")
    create_html_pages(input_dir)
    print("\nConversion complete! Open index.html in your browser to start reading.")


