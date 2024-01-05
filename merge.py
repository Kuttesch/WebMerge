import argparse
import os

def embed_files(html_file, css_file, js_file, output_file):
    # Read content from HTML, CSS, and JS files
    with open(html_file, 'r') as html_file:
        html_content = html_file.read()

    with open(css_file, 'r') as css_file:
        css_content = css_file.read()

    with open(js_file, 'r') as js_file:
        js_content = js_file.read()

    # Remove external links to CSS and JS files from HTML
    html_content = html_content.replace(f'<link rel="stylesheet" type="text/css" href="{css_file}">', '')
    html_content = html_content.replace(f'<script type="text/javascript" src="{js_file}"></script>', '')

    # Find the position to insert CSS content in the HTML file
    head_index = html_content.lower().find('</head>')

    if head_index != -1:
        # Insert CSS content into the HTML file
        modified_html = html_content[:head_index] + f'\n<style>{css_content}</style>\n' + html_content[head_index:]
    else:
        # If </head> tag is not found, append the CSS content at the end
        modified_html = html_content + f'\n<style>{css_content}</style>\n'

    # Find the position to insert JS content in the HTML file
    body_index = modified_html.lower().find('</body>')

    if body_index != -1:
        # Insert JS content into the HTML file
        modified_html = modified_html[:body_index] + f'\n<script>{js_content}</script>\n' + modified_html[body_index:]
    else:
        # If </body> tag is not found, append the JS content at the end
        modified_html = modified_html + f'\n<script>{js_content}</script>\n'

    # Write the modified HTML content to the output file
    with open(output_file, 'w') as output_file:
        output_file.write(modified_html)

def main():
    parser = argparse.ArgumentParser(description='Merge HTML, CSS, and JS files into an HTML file.')
    parser.add_argument('source_directory', type=str, help='Source directory containing HTML, CSS, and JS files')
    parser.add_argument('html_file', type=str, help='HTML file name')
    parser.add_argument('css_file', type=str, help='CSS file name')
    parser.add_argument('js_file', type=str, help='JavaScript file name')
    parser.add_argument('output_file', type=str, help='Output HTML file name')
    parser.add_argument('-info', '--info', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit')

    args = parser.parse_args()

    # Construct full paths for files
    source_directory = args.source_directory
    html_file = os.path.join(source_directory, args.html_file)
    css_file = os.path.join(source_directory, args.css_file)
    js_file = os.path.join(source_directory, args.js_file)
    output_file = os.path.join(source_directory, args.output_file)

    # Call the embed_files function with the provided file paths
    embed_files(html_file, css_file, js_file, output_file)

if __name__ == "__main__":
    main()
