import yaml
import re

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def sort_entries_by_name(entries):
    return sorted(entries, key=lambda x: x['name'].lower())

def generate_markdown_list(entries, category_name):
    list_content = f"## {category_name}\n\n"
    for entry in entries:
        list_content += f"- {entry['name']}: [{entry['url']}]({entry['url']})\n"
    return list_content

def generate_markdown_table(entries, repos, category):
    table = "| Name | Repository |"
    table += " Issue |" if category == "not_working" else "\n"
    table += "| --- | --- |"
    table += " --- |" if category == "not_working" else "\n"
    markdown_link_pattern = re.compile(r'\[.+\]\(.+\)')

    for entry in entries:
        repo_name = entry.get('repo', 'N/A')
        if markdown_link_pattern.match(repo_name):
            repo_markdown = repo_name
        else:
            repo_url = next((repo['url'] for repo in repos if repo['name'] == repo_name), None)
            repo_markdown = f"[{repo_name}]({repo_url})" if repo_url else repo_name
        row = f"| {entry['name']} | {repo_markdown} |"
        row += f" {entry.get('issue', 'N/A')} |" if category == "not_working" else ""
        table += row + "\n"
    return table

def main():
    data = load_yaml('data.yaml')

    markdown_content = "# iOS 16 Compatible Semi-Jailbreak Tweaks\n\n"
    
    repos = data.get('repos', [])
    markdown_content += generate_markdown_list(repos, "Repos URLs")

    for category in ['tweaks', 'themes', 'needs_testing', 'not_working']:
        markdown_content += f"## {category.title().replace('_', ' ')}\n"
        sorted_entries = sort_entries_by_name(data.get(category, []))
        markdown_content += generate_markdown_table(sorted_entries, repos, category) + "\n"

    markdown_content += "## Credits\n"
    for credit in data.get('credits', []):
        markdown_content += f"- [{credit['name']}]({credit['link']})\n"

    with open('README.md', 'w') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    main()
