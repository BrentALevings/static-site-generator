import os
import markdown_blocks

def extract_title(markdown: str):
    rows = markdown.split("\n")
    for row in rows:
        if row.startswith("# ") and row.count("#") == 1:
            return row.strip("#").strip()
    else:
        raise Exception("No h1 header found!")
    
def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_blocks.markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path) , exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path: str, template_path: str, dest_dir_path: str, basepath: str):
    for obj in os.listdir(dir_path):
        # print(obj)
        if obj.endswith(".md"):
            generate_page(os.path.join(dir_path, obj), template_path, os.path.join(dest_dir_path, obj.replace(".md", ".html")), basepath)
        else:
            generate_pages_recursive(os.path.join(dir_path, obj), template_path, os.path.join(dest_dir_path, obj), basepath)
        