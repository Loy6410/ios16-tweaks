import yaml
import re

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def sort_entries_by_name(entries):
    return sorted(entries, key=lambda x: x['name'].lower())

def generate_markdown_table(entries, repos, category):
    if category == "tweaks":
        headers = "| Name | Status | Issue | Repo |"
        header_separator = "| --- | --- | --- | --- |"
    else:
        headers = "| Name | Status | Repo |"
        header_separator = "| --- | --- | --- |"

    table = headers + "\n" + header_separator + "\n"
    markdown_link_pattern = re.compile(r'\[.+\]\(.+\)')

    for entry in entries:
        repo_name = entry.get('repo', 'N/A')
        if markdown_link_pattern.match(repo_name):
            repo_markdown = repo_name
        else:
            repo_url = next((repo['url'] for repo in repos if repo['name'] == repo_name), None)
            repo_markdown = f"[{repo_name}]({repo_url})" if repo_url else repo_name

        status = entry.get('status', '✔️')
        issue = entry.get('issue', '-') if category == "tweaks" else ''

        row = f"| {entry['name']} | {status} | {repo_markdown} |"
        if category == "tweaks":
            row = f"| {entry['name']} | {status} | {issue} | {repo_markdown} |"
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
    markdown_content = "# iOS 16 Compatible Semi-Jailbreak Tweaks and Themes\n\n"
    
    markdown_content += "## Legend\n"
    markdown_content += "- ✔️: Working\n"
    markdown_content += "- ❌: Not Working\n"
    markdown_content += "- ⚠️: Needs Testing\n\n"

    markdown_content += generate_repository_list(repos) + "\n"

    tweak_entries = sort_entries_by_name(data.get('tweaks', []))
    theme_entries = sort_entries_by_name(data.get('themes', []))
    not_working_entries = sort_entries_by_name(data.get('not_working', []))
    needs_testing_entries = sort_entries_by_name(data.get('needs_testing', []))

    for entry in not_working_entries + needs_testing_entries:
        entry['status'] = '❌' if entry in not_working_entries else '⚠️'

    merged_tweak_entries = sort_entries_by_name(tweak_entries + not_working_entries + needs_testing_entries)

    markdown_content += "## Tweaks\n"
    markdown_content += generate_markdown_table(merged_tweak_entries, repos, "tweaks") + "\n"

    markdown_content += "## Themes\n"
    markdown_content += generate_markdown_table(theme_entries, repos, "themes") + "\n"
    
    markdown_content += "## Credits\n"
    for credit in data.get('credits', []):
        markdown_content += f"- [{credit['name']}]({credit['link']})\n"

    with open('README.md', 'w') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    main()