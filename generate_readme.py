import yaml
import re

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def sort_entries_by_name(entries):
    return sorted(entries, key=lambda x: x['name'].lower())

def generate_markdown_table(entries, repos, category):
    headers = "| Name | Compatible | Issue | Description | Repo |"
    header_separator = "| --- | --- | --- | --- | --- |"

    table = headers + "\n" + header_separator + "\n"
    markdown_link_pattern = re.compile(r'\[.+\]\(.+\)')

    for entry in entries:
        repo_name = entry.get('repo', 'N/A')
        if markdown_link_pattern.match(repo_name):
            repo_markdown = repo_name
        else:
            repo_url = next((repo['url'] for repo in repos if repo['name'] == repo_name), None)
            repo_markdown = f"[{repo_name}]({repo_url})" if repo_url else repo_name

        if category == "not_working":
            compatibility = "❌"
            issue = entry.get('issue', 'N/A')
        elif category == "needs_testing":
            compatibility = "⚠️"
            issue = ""
        else:
            compatibility = "✔️" if category == "tweaks" else ""
            issue = ""

        row = f"| {entry['name']} | {compatibility} | {issue} | {entry.get('description', 'N/A')} | {repo_markdown} |"
        table += row + "\n"
    return table

def generate_repository_list(repos):
    sorted_repos = sort_entries_by_name(repos)
    markdown_list = "## Repositories\n"
    for repo in sorted_repos:
        markdown_list += f"- [{repo['name']}]({repo['url']})\n"
    return markdown_list

def main():
    data = load_yaml('data.yaml')

    repos = data.get('repos', [])
    markdown_content = "# iOS 16 Compatible Semi-Jailbreak Tweaks\n\n"

    markdown_content += generate_repository_list(repos) + "\n"

    tweak_entries = sort_entries_by_name(data.get('tweaks', []))
    theme_entries = sort_entries_by_name(data.get('themes', []))
    not_working_entries = sort_entries_by_name(data.get('not_working', []))

    merged_entries = sort_entries_by_name(tweak_entries + theme_entries + not_working_entries)

    markdown_content += "## Compatible Tweaks\n"
    markdown_content += generate_markdown_table(tweak_entries, repos, "tweaks") + "\n"

    markdown_content += "## Compatible Themes\n"
    markdown_content += generate_markdown_table(theme_entries, repos, "themes") + "\n"

    if not_working_entries:
        markdown_content += "## Not Working\n"
        markdown_content += generate_markdown_table(not_working_entries, repos, "not_working") + "\n"

    markdown_content += "## Needs Testing\n"
    markdown_content += generate_markdown_table(sort_entries_by_name(data.get('needs_testing', [])), repos, "needs_testing") + "\n"

    markdown_content += "## Credits\n"
    for credit in data.get('credits', []):
        markdown_content += f"- [{credit['name']}]({credit['link']})\n"

    with open('README.md', 'w') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    main()
