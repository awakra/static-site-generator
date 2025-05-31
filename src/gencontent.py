import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages for all markdown files in a directory.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory for generated HTML files
    """
    
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(from_path):
            if entry.endswith('.md'):
                html_filename = entry[:-3] + '.html' 
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                generate_page(from_path, template_path, dest_path)
        
        else:
            subdirectory_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(from_path, template_path, subdirectory_dest)