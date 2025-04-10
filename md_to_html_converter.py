import os
import re
from pathlib import Path
from pygments.formatters import HtmlFormatter
import markdown2

def create_html_pages(input_dir):
    """Convert markdown files to HTML in the same directory"""
    # Get Pygments CSS
    pygments_css = HtmlFormatter().get_style_defs('.highlight')

    # Get list of markdown files and sort properly
    input_dir = Path(input_dir)
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]

    # Custom sort: put index.md first, then sort numerically
    md_files = sorted(md_files, key=lambda x: (
        "0" if x == "index.md" else  # Make index.md come first
        x.split('_')[0] if '_' in x else x  # Sort others by their numeric prefix
    ))

    for i, md_file in enumerate(md_files):
        print(f"\nProcessing {md_file}...")

        # Read markdown content
        with open(input_dir / md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace .md links with .html in the content
        content = re.sub(r'\((.*?)\.md\)', r'(\1.html)', content)

        # Convert to HTML
        html_content = markdown2.markdown(content, extras=[
            'fenced-code-blocks',
            'tables',
            'code-friendly',
            'break-on-newline',
            'cuddled-lists',
            'markdown-in-html',
            'target-blank-links'
        ])

        # Create navigation links
        if md_file == 'index.md':
            # Index page: only show Next
            prev_link = ''
            index_link = ''
            next_link = f'<a class="nav-link" href="{md_files[1].replace(".md", ".html")}">Next &rarr;</a>' if len(md_files) > 1 else ''
        else:
            # For all other pages
            prev_file = md_files[i-1]
            next_file = md_files[i+1] if i < len(md_files)-1 else None

            prev_link = f'<a class="nav-link" href="{prev_file.replace(".md", ".html")}">&larr; Previous</a>'
            index_link = '<a class="nav-link" href="index.html">Index</a>'
            next_link = f'<a class="nav-link" href="{next_file.replace(".md", ".html")}">Next &rarr;</a>' if next_file else ''

        # Write HTML file to same directory
        html_filename = md_file.replace('.md', '.html')
        output_path = input_dir / html_filename

        # Create a more readable title
        if md_file == 'index.md':
            title = 'Tutorial Index'
        else:
            # Remove numeric prefix and underscores, capitalize
            title = ' '.join(md_file.split('_')[1:]).replace('.md', '').title()

        final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
        {pygments_css}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        .navigation {{
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            padding: 10px;
            background-color: #f6f8fa;
            border-radius: 6px;
        }}
        .nav-link {{
            text-decoration: none;
            color: #0366d6;
            padding: 5px 10px;
        }}
        .nav-link:hover {{
            background-color: #0366d6;
            color: white;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="navigation">
        {prev_link}
        {index_link}
        {next_link}
    </div>
    {html_content}
    <div class="navigation">
        {prev_link}
        {index_link}
        {next_link}
    </div>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Written to {output_path}")

if __name__ == "__main__":
    # Use the existing output/pf1 directory
    input_dir = Path("output/pf1")

    print(f"\nConverting markdown files in: {input_dir}")
    create_html_pages(input_dir)
    print("\nConversion complete! Open index.html in your browser to start reading.")


