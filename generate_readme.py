import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def sort_entries_by_name(entries):
    return sorted(entries, key=lambda x: x['name'].lower())

def generate_markdown_table(entries):
    table = "| Name | Repository |\n| --- | --- |\n"
    for entry in entries:
        table += f"| {entry['name']} | {entry.get('repo', 'N/A')} |\n"
    return table

def main():
    data = load_yaml('data.yaml')

    markdown_content = "# iOS 16 Compatible Semi-Jailbreak Tweaks\n\n"

    for category in ['tweaks', 'themes', 'needs_testing', 'not_working']:
        markdown_content += f"## {category.title().replace('_', ' ')}\n"
        sorted_entries = sort_entries_by_name(data.get(category, []))
        markdown_content += generate_markdown_table(sorted_entries) + "\n"

    markdown_content += "## Credits\n"
    for credit in data.get('credits', []):
        markdown_content += f"- [{credit['name']}]({credit['link']})\n"

    with open('README.md', 'w') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    main()