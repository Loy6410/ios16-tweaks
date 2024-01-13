import yaml
import re

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def sort_entries_by_name(entries):
    return sorted(entries, key=lambda x: x['name'].lower())

def generate_markdown_list(entries, category_name):
    list_content = f"## {category_name}\n\n"
    sorted_entries = sort_entries_by_name(entries)
    for entry in sorted_entries:
        list_content += f"- [{entry['name']}]({entry['url']})\n"
    return list_content

def generate_markdown_table(entries, repos, category):
    table = "| Name | Repository |"
    table += " Issue |" if category == "not_working" else "\n"
    table += "\n| --- | --- |"
    table += " --- |" if category == "not_working" else "\n"
    
    markdown_link_pattern = re.compile(r'\[.+\]\(.+\)')
    
    for entry in sort_entries_by_name(entries):
        repo_name = entry.get('repo', 'N/A')
        if markdown_link_pattern.match(repo_name):
            repo_markdown = repo_name
        else:
            repo_url = next((repo['url'] for repo in repos if repo['name'] == repo_name), repo_name)
            repo_markdown = f"[{repo_name}]({repo_url})" if repo_url != repo_name else repo_name
        
        if category == "not_working":
            issue_description = entry.get('issue', 'N/A')
            table += f"| {entry['name']} | {repo_markdown} | {issue_description} |\n"
        else:
            table += f"| {entry['name']} | {repo_markdown} |\n"
    
    return table

def main():
    data = load_yaml('data.yaml')

    markdown_content = "# iOS 16 Compatible Semi-Jailbreak Tweaks\n\n"
    
    repos = data.get('repos', [])
    markdown_content += generate_markdown_list(repos, "Repos URLs")

    for category in ['tweaks', 'themes', 'needs_testing', 'not_working']:
        markdown_content += f"## {category.title().replace('_', ' ')}\n"
        markdown_content += generate_markdown_table(data.get(category, []), repos, category) + "\n"

    markdown_content += "## Credits\n"
    for credit in data.get('credits', []):
        markdown_content += f"- [{credit['name']}]({credit['link']})\n"

    with open('README.md', 'w') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    main()
